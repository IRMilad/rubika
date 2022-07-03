import os
import typing
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
                methods.authorisations.GetDCs()
            )

        return self._client._dcs

    async def close(self):
        await self._connection.close()

    async def upload_file(self, file: typing.Union[str, bytes],
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
        respond = await self.execute(
            methods.messages.RequestSendFile(
                mime=mime,
                size=len(file),
                file_name=file_name)
        )
        self._client._logger.info('upload file (%s)', respond)
    
        id = respond.id
        dc_id = respond.dc_id
        total = int(len(file) / chunk + 1)
        upload_url = respond.upload_url
        access_hash_send = respond.access_hash_send
        for part, index in enumerate(range(0, len(file), chunk), start=1):
            data = file[index: index + chunk]
            respond = await self._connection.post(
                upload_url,
                headers={
                    'auth': self._client._auth,
                    'file-id': id,
                    'total-part': str(total),
                    'part-number': str(part),
                    'chunk-size': str(len(data)),
                    'access-hash-send': access_hash_send
                },
                data=data
            )
            self._client._logger.info('upload chunk (%s)', respond)
            if callable(callback):
                try:
                    await callback(len(file), index + chunk)

                except exceptions.CancelledError:
                    self._client._logger.info('upload cancelled')
                    return None

                except Exception:
                    pass

        result = await respond.json()
        status = result['status']
        status_det = result['status_det']
        if status == 'OK' and status_det == 'OK':
            return results('UploadFile', {
                'mime': mime,
                'size': len(file),
                'dc_id': dc_id,
                'file_id': id,
                'file_name': file_name,
                'access_hash_rec': result['data']['access_hash_rec']})

        self._client._logger.debug('upload failed (%s)', result)
        raise exceptions(status_det)(result, result=result)

    async def execute(self, request: dict):
        self._client._logger.info('execute method (%s)', request)
        method_urls = request.pop('urls')
        if method_urls is None:
            method_urls = (await self._dcs()).default_api_urls

        if not method_urls:
            raise exceptions.UrlNotFound(
                'It seems that the client could not'
                ' get the list of Rubika api\'s.'
                ' Please wait and try again.',
                result=result)
        
        method = request['method']
        tmp_session = request.pop('tmp_session')
        if self._client._auth is None:
            self._client._auth = Crypto.secret(length=32)
            self._client._logger.info('create auth secret [%s]', self._client._auth)

        if self._client._key is None:
            self._client._key = Crypto.passphrase(self._client._auth)
            self._client._logger.info('create key passphrase [%s]', self._client._key)

        request['client'] = self._client._platform
        if request.get('encrypt') is True:
            request = {'data_enc': Crypto.encrypt(request, key=self._client._key)}


        request['tmp_session' if tmp_session else 'auth'] = self._client._auth

        if 'api_version' not in request:
            request['api_version'] = self._client.configuire['api_version']

        for level in range(self._client._request_retries):
            for url in method_urls:
                try:
                    async with self._connection.options(url) as res:
                        if res.status != 200:
                            self._client._logger.debug(
                                '#{%d} options request failed (%s)[%d] (%s)',
                                level, url, res.status, request)

                    async with self._connection.post(url, json=request) as res:
                        if res.status != 200:
                            self._client._logger.debug(
                                '#{%d} post request failed (%s)[%d] (%s)',
                                level, url, res.status, request)
                            continue

                        result = await res.json()
                        if result.get('data_enc'):
                            result = Crypto.decrypt(result['data_enc'],
                                                    key=self._client._key)
                        status = result['status']
                        status_det = result['status_det']
                        if status == 'OK' and status_det == 'OK':
                            self._client._logger.info(
                                '#{%d} post result (%s)[%d] (%s)',
                                level, url, res.status, request)
                            result['data']['_client'] = self._client
                            return results(method, update=result['data'])
                        
                        self._client._logger.warning(
                                '#{%d} post request failed (%s)[%d] (%s)',
                                level, url, res.status, result)
                        raise exceptions(status_det)(result, request=request)

                except aiohttp.ServerTimeoutError:
                    self._client._logger.warning(
                        '#{%d} server timeout (%s) (%s)', level, url, request)
                    pass

        self._client._logger.warning(
            'rubika server has an internal problem (%s)', request)
    
        raise exceptions.InternalProblem(
            'rubika server has an internal problem', request=request)

    async def download(self, dc_id, file_id,
                       access_hash, chunk=131072, callback=None):
        url = (await self._dcs()).storages[dc_id]
        headers = {
            'file-id': file_id,
            'auth': self._client._auth,
            'access-hash-rec': access_hash}
        self._client._logger.debug(
            'download media (%s) (%s) (chunk %d)', headers, url, chunk)
        async with self._connection.post(url, headers=headers) as res:
            if res.status != 200:
                self._client._logger.debug(
                    'download media failed (%s) (%s)[%d]', headers, url, res.status)
    
            result = b''
            total = res.headers.get('total_length', None)
            self._client._logger.info(
                'download media (%s) (%s) (chunk %d) (size %d)', headers, url, chunk, total)
    
            async for chunk in res.content.iter_chunked(chunk):
                result += chunk
                if callable(callback):
                    try:
                        await callback(total, len(res))

                    except exceptions.CancelledError:
                        self._client._logger.info(
                            'download media cancelled (%s) (%s)', headers, url)
                        return None

                    except Exception:
                        pass
            return res

    async def receive_updates(self):
        default_sockets = (await self._dcs()).default_sockets
        for url in default_sockets:
            async with self._connection.ws_connect(url) as wss:
                await wss.send_json({
                    'method': 'handShake',
                    'auth': self._client._auth,
                    'api_version': self._client.configuire['api_version']})
                self._client._logger.info('start receiving updates [%s]', url)
                async for message in wss:
                    try:
                        result = message.json()
                        if not result.get('data_enc'):
                            self._client._logger.debug(
                                f'the data_enc key was not found in the dictionary [{result}]')
                            continue
                        result = Crypto.decrypt(result['data_enc'],
                                                key=self._client._key)
                        self._client._logger.info('aes key [%s]', self._client._key)
                        user_guid = result.pop('user_guid')
                        for key, package in result.items():
                            if not isinstance(package, list):
                                continue

                            for update in package:
                                update['_client'] = self._client
                                update['user_guid'] = user_guid
                                handlers = self._client._handlers.copy()
                                self._client._logger.info(f'update {update}')
                                for func, handler in handlers.items():
                                    try:
                                        # if handler is empty filters
                                        if isinstance(handler, type):
                                            handler = handler()

                                        if handler.__name__ != capitalize(key):
                                            continue

                                        # analyze handlers
                                        if not await handler(update=update):
                                            continue
                                        
                                        self._client._logger.info('called handler [%s]', func.__name__)
                                        await func(handler)

                                    except exceptions.StopHandler:
                                        self._client._logger.info('stop handling from [%s]', func.__name__)
                                        break

                                    except Exception:
                                        self._client._logger.warning('handler [%s] raised an exception', func.__name__, exc_info=True)
                    except Exception:
                        self._client._logger.warning('websocket raised an exception', exc_info=True)
