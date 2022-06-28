import os
import typing
import aiohttp
import traceback
from ..crypto import Crypto
from ..structs import UpdateStruct
from ..gadgets import errors, methods


class Connection(object):
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
            if callable(callback):
                try:
                    await callback(len(file), index + chunk)

                except errors.CancelledError:
                    return None

                except Exception:
                    pass

        result = await respond.json()
        status = result['status']
        status_det = result['status_det']
        if status == 'OK' and status_det == 'OK':
            return UpdateStruct('UploadFile', {
                'mime': mime,
                'size': len(file),
                'dc_id': dc_id,
                'file_id': id,
                'file_name': file_name,
                'access_hash_rec': result['data']['access_hash_rec']})

        raise errors.RequestError(result, det=status_det)

    async def execute(self, request):
        try:
            method_urls = [request.url]

        except AttributeError:
            method_urls = (await self._dcs()).default_api_urls

        if not method_urls:
            raise errors.ConnectionUrlNotFound(
                'It seems that the client could not'
                ' get the list of Rubika api\'s.'
                ' Please wait and try again.',
                request=request)

        if self._client._auth is None:
            self._client._auth = Crypto.secret(length=32)

        if self._client._key is None:
            self._client._key = Crypto.passphrase(self._client._auth)

        try:
            data = {'input': request.input}
        except AttributeError:
            data = request.data

        method = type(request).__name__
        data['client'] = self._client._platform
        data['method'] = method[0].lower() + method[1:]

        try:
            encrypt = request.encrypt

        except AttributeError:
            encrypt = True

        if encrypt is True:
            data = {'data_enc': Crypto.encrypt(data, key=self._client._key)}

        try:
            if request.tmp_session:
                data['tmp_session'] = self._client._auth

        except AttributeError:
            data['auth'] = self._client._auth

        if 'api_version' not in data:
            data['api_version'] = self._client.configuire['api_version']

        for _ in range(self._client._request_retries):
            for url in method_urls:
                try:
                    async with self._connection.options(url) as res:
                        if res.status != 200:
                            break

                    async with self._connection.post(url, json=data) as res:
                        if res.status != 200:
                            break
                        result = await res.json()
                        if result.get('data_enc'):
                            result = Crypto.decrypt(result['data_enc'],
                                                    key=self._client._key)
                        status = result['status']
                        status_det = result['status_det']
                        if status == 'OK' and status_det == 'OK':
                            return UpdateStruct(method,
                                                data=result['data'])
                        raise errors.RequestError(result,
                                                  det=status_det,
                                                  request=request)
                except aiohttp.ServerTimeoutError:
                    pass

        # if not response
        raise errors.ConnectionInternalProblem(
            'Rubika server has an internal problem', request=request)

    async def download(self, dc_id, file_id,
                       access_hash, chunk=131072, callback=None):
        url = (await self._dcs()).storages[dc_id]
        headers = {
            'file-id': file_id,
            'auth': self._client._auth,
            'access-hash-rec': access_hash}
        async with self._connection.post(url, headers=headers) as result:
            res = b''
            total = result.headers.get('total_length', None)
            async for chunk in result.content.iter_chunked(chunk):
                res += chunk
                if callable(callback):
                    try:
                        await callback(total, len(res))

                    except errors.CancelledError:
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
                async for message in wss:
                    try:
                        result = message.json()
                        if result.get('data_enc'):
                            result = Crypto.decrypt(
                                result['data_enc'], key=self._client._key)
                            _user_guid = result.pop('user_guid')
                            for name, value in result.items():
                                # convert to custom name
                                name = ''.join([
                                    c.title() for c in name.split('_')])

                                if not isinstance(value, list):
                                    continue

                                for update in value:
                                    update['_client'] = self._client
                                    update['user_guid'] = _user_guid
                                    _handlers = self._client._handlers
                                    for func, handler in _handlers.items():
                                        try:
                                            # if handler is class
                                            if isinstance(handler, type):
                                                handler = handler()

                                            # set update
                                            handler = handler(name, update)
                                            # if handler name == custom name

                                            if type(handler).__name__ != name:
                                                continue
                                            # call analyze property
                                            if handler and not handler.analyze:
                                                continue

                                            await func(handler)

                                        except errors.StopHandler:
                                            break

                                        except Exception:
                                            print(traceback.format_exc())
                    except Exception:
                        print(traceback.format_exc())
