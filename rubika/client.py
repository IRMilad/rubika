import os
import logging
from .crypto import Crypto
from .structs import Struct
from . import __name__ as logger_name
from .network import Connection, Proxies
from .gadgets import exceptions, methods, thumbnail
from .sessions import StringSession, SQLiteSession


class Client:
    configuire = {
        'package': 'web.rubika.ir',
        'platform': 'Web',
        'app_name': 'Main',
        'user_agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko)'
                       'Chrome/102.0.0.0 Safari/537.36'),
        'api_version': '5',
        'app_version': '4.0.7'
    }

    def __init__(self,
                 session,
                 proxy=None,
                 logger=None,
                 timeout=20,
                 lang_code='fa',
                 user_agent=None,
                 request_retries=5, *args, **kwargs):

        """_Client_
            Args:
                session_name (`str` | `rubika.sessions.StringSession`):
                    The file name of the session file that is used
                    if there is a string Given (may be a complete path)
                    or it could be a string session
                    [rubika.sessions.StringSession]

                proxy (` rubika.network.Proxies `, optional): To set up a proxy

                user_agent (`str`, optional):
                    Client uses the web version, You can set the usr-user_agent

                timeout (`int` | `float`, optional):
                    To set the timeout `` default( `20 seconds` )``

                logger (`logging.Logger`, optional):
                    Logger base for use.

                lang_code(`str`, optional):
                    To set the lang_code `` default( `fa` ) ``
        """

        if isinstance(session, StringSession):
            session = StringSession(session)

        elif isinstance(session, str):
            session = SQLiteSession(session)

        else:
            raise TypeError('The given session must be a '
                            'str or [rubika.sessions.StringSession]')

        if not isinstance(logger, logging.Logger):
            logger = logging.getLogger(logger_name)

        if proxy and not isinstance(proxy, Proxies):
            raise TypeError(
                'The given proxy must be a [rubika.network.Proxies]')

        self._dcs = None
        self._key = None
        self._auth = None
        self._guid = None
        self._proxy = proxy
        self._logger = logger
        self._timeout = timeout
        self._session = session
        self._handlers = {}
        self._request_retries = request_retries
        self._user_agent = user_agent or self.configuire['user_agent']
        self._platform = {
            'package': kwargs.get('package', self.configuire['package']),
            'platform': kwargs.get('platform', self.configuire['platform']),
            'app_name': kwargs.get('app_name', self.configuire['app_name']),
            'app_version': kwargs.get('app_version',
                                      self.configuire['app_version']),
            'lang_code': lang_code}

    async def __call__(self, request: object):
        try:
            result = await self._connection.execute(request)

            # update session
            if result.__name__ == 'signIn' and result.status == 'OK':
                self._key = Crypto.passphrase(result.auth)
                self._auth = result.auth
                self._session.insert(
                    auth=self._auth,
                    guid=result.user.user_guid,
                    user_agent=self._user_agent,
                    phone_number=result.user.phone)

                await self(
                    methods.authorisations.RegisterDevice(
                        self._user_agent,
                        lang_code=self._platform['lang_code'],
                        app_version=self._platform['app_version'])
                )

            return result

        except AttributeError:
            raise exceptions.NoConnection(
                'You must first connect the Client'
                ' with the *.connect() method')

    async def __aenter__(self):
        return await self.start(phone_number=None)

    async def __aexit__(self, *args, **kwargs):
        return await self.disconnect()

    async def start(self, phone_number: str, *args, **kwargs):
        if not hasattr(self, '_connection'):
            await self.connect()

        try:
            self._logger.info('user info', extra={'data': await self.get_me()})

        except exceptions.NotRegistrred:
            self._logger.debug('user not registrred')
            if phone_number is None:
                phone_number = input('phone number > ')

            result = await self(
                methods.authorisations.SendCode(
                    phone_number=phone_number, *args, **kwargs))

            if result.status == 'SendPassKey':
                while True:
                    pass_key = input(f'password [{result.hint_pass_key}] > ')
                    result = await self(
                        methods.authorisations.SendCode(
                            phone_number=phone_number,
                            pass_key=pass_key, *args, **kwargs))

                    if result.status == 'OK':
                        break

            while True:
                phone_code = input('code > ')
                result = await self(
                    methods.authorisations.SignIn(
                        phone_code=phone_code,
                        phone_number=phone_number,
                        phone_code_hash=result.phone_code_hash,
                        *args, **kwargs))

                if result.status == 'OK':
                    break

        return self

    async def connect(self):
        self._connection = Connection(client=self)
        information = self._session.information()
        self._logger.info(f'the session information was read {information}')
        if information:
            self._auth = information[1]
            self._guid = information[2]
            if information[3] != self._user_agent:
                self._logger.warn('you can not change the user_agent after logging')
            self._user_agent = information[3]

        return self

    async def disconnect(self):
        try:
            await self._connection.close()
            self._logger.info(f'the client was disconnected')

        except AttributeError:
            raise exceptions.NoConnection(
                'You must first connect the Client'
                ' with the *.connect() method')

    async def run_until_disconnected(self):
        return await self._connection.receive_updates()

    # handler methods

    def on(self, handler):
        def MetaHandler(func):
            self.add_handler(func, handler)
            return func
        return MetaHandler

    def add_handler(self, func, handler):
        self._handlers[func] = handler

    def remove_handler(self, func):
        try:
            self._handlers.pop(func)
        except KeyError:
            pass

    # async methods

    async def get_me(self, *args, **kwargs):
        return await self(methods.users.GetUserInfo(self._guid))

    async def upload(self, file, *args, **kwargs):
        return await self._connection.upload_file(file=file, *args, **kwargs)

    async def send_message(self,
                           object_guid: str,
                           message=None,
                           reply_to_message_id: str = None,
                           file_inline=None,
                           type: str = methods.messages.File,
                           thumb: bool = True, *args, **kwargs):
        """_send message_

        Args:
            object_guid (str):
                _object guid_

            message (Any, optional):
                _message or cation or sticker_ . Defaults to None.

            reply_to_message_id (str, optional):
                _reply to message id_. Defaults to None.

            file_inline (typing.Union[pathlib.Path, bytes], optional):
                _file_. Defaults to None.

            type (str, optional):
                _file type_. Defaults to methods.messages.File.(
                    methods.messages.Gif,
                    methods.messages.Image,
                    methods.messages.Voice,
                    methods.messages.Music,
                    methods.messages.Video
                )

            thumb (bool, optional):
                if value is "True",
                    the lib will try to build the thumb ( require cv2 )
                if value is thumbnail.Thumbnail, to set custom
                Defaults to True.
        """

        if object_guid.lower() in ['me', 'self', 'cloud']:
            object_guid = self._guid

        if file_inline is not None:
            if not isinstance(file_inline, Struct):
                if isinstance(file_inline, str):
                    with open(file_inline, 'rb') as file:
                        kwargs['file_name'] = kwargs.get(
                            'file_name', os.path.basename(file_inline))
                        file_inline = file.read()

                if thumb is True:
                    if type == methods.messages.Image:
                        thumb = thumbnail.MakeThumbnail(file_inline)

                    elif type in [methods.messages.Gif, methods.messages.Video]:
                        thumb = thumbnail.MakeThumbnail.from_video(file_inline)

                # the problem will be fixed in the next version #debug
                # to avoid getting InputError
                # values are not checked in Rubika (optional)
                file_inline = await self.upload(file_inline, *args, **kwargs)
                file_inline['type'] = type
                file_inline['time'] = kwargs.get('time', 1)
                file_inline['width'] = kwargs.get('width', 200)
                file_inline['height'] = kwargs.get('height', 200)
                file_inline['music_performer'] = kwargs.get('performer', '')

                if isinstance(thumb, thumbnail.Thumbnail):
                    file_inline['time'] = thumb.seconds
                    file_inline['width'] = thumb.width
                    file_inline['height'] = thumb.height
                    if thumb.image is not None:
                        file_inline['thumb_inline'] = thumb.to_base64()

        return await self(
            methods.messages.SendMessage(
                object_guid,
                message=message,
                file_inline=file_inline,
                reply_to_message_id=reply_to_message_id))

    async def download_file_inline(self, file_inline, file: str = None, *args, **kwargs):
        result = await self._connection.download(
            file_inline.dc_id,
            file_inline.file_id,
            file_inline.access_hash_rec)

        if isinstance(file, str):
            with open(file, 'wb+') as _file:
                _file.write(result)
                return file

        return result
