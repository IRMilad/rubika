import os
import asyncio
import aiohttp
from ..crypto import Crypto
from ..structs import results
from ..gadgets import exceptions, methods


def capitalize(text):
    return ''.join([
        c.title() for c in text.split('_')])


class Connection:
    """Internal class"""

    def __init__(self, client):
        self._client = client
        self._connection = aiohttp.ClientSession(
            connector=self._client._proxy,
            headers={'user-agent': self._client._user_agent},
            timeout=aiohttp.ClientTimeout(total=self._client._timeout))

    async def _dcs(self):
        if not self._client._dcs:
            self._client._dcs = await self.execute(
                methods.authorisations.GetDCs())

        return self._client._dcs

    async def close(self):
        await self._connection.close()

    async def upload_file(self, file,
                          mime: str = None, file_name: str = None,
                          chunk: int = 131072, callback=None, *args, **kwargs):
        if isinstance(file, str):
            if not os.path.exists(file):
                raise ValueError('file not found in the given path')
            if file_name is None:
                file_name = os.path.basename(file)

            with open(file, 'rb') as file:
                file = file.read()

        elif not isinstance(file, bytes):
            raise TypeError('file arg value must be file path or bytes')

        if file_name is None:
            raise ValueError('the file_name is not set')

        if mime is None:
            mime = file_name.split('.')[-1]

        result = await self.execute(
            methods.messages.RequestSendFile(
                mime=mime, size=len(file), file_name=file_name))

        id = result.id
        index = 0
        dc_id = result.dc_id
        total = int(len(file) / chunk + 1)
        upload_url = result.upload_url
        access_hash_send = result.access_hash_send

        while index < total:
            data = file[index * chunk: index * chunk + chunk]
            try:
                result = await self._connection.post(
                    upload_url,
                    headers={
                        'auth': self._client._auth,
                        'file-id': id,
                        'total-part': str(total),
                        'part-number': str(index + 1),
                        'chunk-size': str(len(data)),
                        'access-hash-send': access_hash_send
                    },
                    data=data
                )
                result = await result.json()
                if callable(callback):
                    try:
                        await callback(len(file), index * chunk)

                    except exceptions.CancelledError:
                        return None

                    except Exception:
                        pass

                index += 1
            except Exception:
                pass

        status = result['status']
        status_det = result['status_det']
        if status == 'OK' and status_det == 'OK':
            result = {
                'mime': mime,
                'size': len(file),
                'dc_id': dc_id,
                'file_id': id,
                'file_name': file_name,
                'access_hash_rec': result['data']['access_hash_rec']
            }

            return results('UploadFile', result)

        self._client._logger.debug('upload failed', extra={'data': result})
        raise exceptions(status_det)(result, request=result)

    async def execute(self, request: dict):
        if not isinstance(request, dict):
            request = request()

        self._client._logger.info('execute method', extra={'data': request})
        method_urls = request.pop('urls')
        if method_urls is None:
            method_urls = (await self._dcs()).default_api_urls

        if not method_urls:
            raise exceptions.UrlNotFound(
                'It seems that the client could not'
                ' get the list of Rubika api\'s.'
                ' Please wait and try again.',
                request=request)

        method = request['method']
        tmp_session = request.pop('tmp_session')
        if self._client._auth is None:
            self._client._auth = Crypto.secret(length=32)
            self._client._logger.info(
                'create auth secret', extra={'data': self._client._auth})

        if self._client._key is None:
            self._client._key = Crypto.passphrase(self._client._auth)
            self._client._logger.info(
                'create key passphrase', extra={'data': self._client._key})

        request['client'] = self._client._platform
        if request.get('encrypt') is True:
            request = {'data_enc': Crypto.encrypt(request, key=self._client._key)}

        request['tmp_session' if tmp_session else 'auth'] = self._client._auth

        if 'api_version' not in request:
            request['api_version'] = self._client.configuire['api_version']

        for _ in range(self._client._request_retries):
            for url in method_urls:
                try:
                    async with self._connection.options(url) as result:
                        if result.status != 200:
                            continue

                    async with self._connection.post(url, json=request) as result:
                        if result.status != 200:
                            continue

                        result = await result.json()
                        if result.get('data_enc'):
                            result = Crypto.decrypt(result['data_enc'],
                                                    key=self._client._key)
                        status = result['status']
                        status_det = result['status_det']
                        if status == 'OK' and status_det == 'OK':
                            result['data']['_client'] = self._client
                            return results(method, update=result['data'])

                        self._client._logger.warning(
                            'request status '
                            + capitalize(status_det), extra={'data': request})

                        raise exceptions(status_det)(result, request=request)

                except aiohttp.ServerTimeoutError:
                    pass

        raise exceptions.InternalProblem(
            'rubika server has an internal problem', request=request)

    async def download(self, dc_id, file_id,
                       access_hash, chunk=131072, callback=None):
        url = (await self._dcs()).storages[str(dc_id)]
        headers = {
            'file-id': str(file_id),
            'auth': self._client._auth,
            'access-hash-rec': access_hash}
        async with self._connection.post(url, headers=headers) as result:
            if result.status != 200:
                raise exceptions.InternalProblem(
                    'the server is not responding')

            data = b''
            total = int(result.headers.get('total_length', None))

            async for chunk in result.content.iter_chunked(chunk):
                data += chunk
                if callable(callback):
                    try:
                        await callback(total, len(data))

                    except exceptions.CancelledError:
                        self._client._logger.info(
                            'download media cancelled (%s) (%s)', headers, url)
                        return None

                    except Exception:
                        pass

            return data

    async def handel_update(self, name, update):
        handlers = self._client._handlers.copy()
        for func, handler in handlers.items():
            try:
                # if handler is empty filters
                if isinstance(handler, type):
                    handler = handler()

                if handler.__name__ != capitalize(name):
                    continue

                # analyze handlers
                if not await handler(update=update):
                    continue

                await func(handler)

            except exceptions.StopHandler:
                break

            except Exception:
                self._client._logger.error(
                    'handler raised an exception',
                    extra={'data': update}, exc_info=True)

    async def receive_updates(self):
        default_sockets = (await self._dcs()).default_sockets
        for url in default_sockets:
            async with self._connection.ws_connect(url) as wss:
                await wss.send_json({
                    'method': 'handShake',
                    'auth': self._client._auth,
                    'api_version': self._client.configuire['api_version']})
                self._client._logger.info(
                    'start receiving updates', extra={'data': url})
                async for message in wss:
                    try:
                        result = message.json()
                        if not result.get('data_enc'):
                            self._client._logger.debug(
                                'the data_enc key was not found',
                                extra={'data': result})
                            continue

                        result = Crypto.decrypt(result['data_enc'],
                                                key=self._client._key)
                        user_guid = result.pop('user_guid')
                        for name, package in result.items():
                            if not isinstance(package, list):
                                continue

                            for update in package:
                                update['_client'] = self._client
                                update['user_guid'] = user_guid
                                asyncio.create_task(
                                    self.handel_update(name, update))

                    except Exception:
                        self._client._logger.error(
                            'websocket raised an exception',
                            extra={'data': url}, exc_info=True)
