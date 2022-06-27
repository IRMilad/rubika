import typing
import logging
import warnings
from .crypto import Crypto
from .gadgets import errors, methods
from .network import Connection, Proxies
from .sessions import StringSession, SQLiteSession


class Client(object):
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
                 session: str,
                 user_agent: str = None,
                 proxy: Proxies = None,
                 logger: logging.Logger = None,
                 timeout: int = 20,
                 lang_code: str = 'fa',
                 request_retries: int = 5,
                 **kwargs
                 ):

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
            logger = logging.getLogger('rubika')

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
            if result._ == 'SignIn' and result.status == 'OK':
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
            raise errors.NoConnection('You must first connect the Client'
                                      ' with the *.connect() method')

    async def __aenter__(self):
        return await self.connect()

    async def __aexit__(self, *args, **kwargs):
        return await self.disconnect()

    async def start(self, phone_number: str, **kwargs):
        if not hasattr(self, '_connection'):
            await self.connect()

        try:
            return await self(methods.users.GetUserInfo(self._guid))

        except (AttributeError, errors.ClientError):
            result = await self(
                methods.authorisations.SendCode(
                    phone_number=phone_number, **kwargs)
            )

            if result.status == 'SendPassKey':
                while True:
                    pass_key = input(f'password [{result.hint_pass_key}] > ')
                    result = await self(
                        methods.authorisations.SendCode(
                            phone_number=phone_number,
                            pass_key=pass_key, **kwargs)
                    )

                    if result.status == 'OK':
                        break
            while True:
                phone_code = input('code > ')
                result = await self(
                    methods.authorisations.SignIn(
                        phone_code=phone_code,
                        phone_number=phone_number,
                        phone_code_hash=result.phone_code_hash)
                )

                if result.status == 'OK':
                    break
            return result.user

    async def connect(self):
        self._connection = Connection(client=self)
        information = self._session.information()
        if information:
            self._auth = information[1]
            self._guid = information[2]
            if information[3] != self._user_agent:
                warnings.warn(
                    'You can not change the user-user_agent after logging')
            self._user_agent = information[3]

        return self

    async def disconnect(self):
        try:
            return await self._connection.close()

        except AttributeError:
            raise errors.NoConnection('You must first connect the Client'
                                      ' with the *.connect() method')

    async def run_until_disconnected(self):
        return await self._connection.receive_updates()

    async def upload(self, file: typing.Union[str, bytes],
                     mime: str = None, file_name: str = None,
                     chunk: int = 131072, callback=None, *args, **kwargs):

        return self._connection.upload_file(
            file=file, mime=mime,
            file_name=file_name, chunk=chunk, callback=callback)

    def on(self, event: object):
        def handler(func):
            self.add_handler(func, event)
            return func
        return handler

    def add_handler(self, func, event: object):
        self._handlers[func] = event

    def remove_handler(self, func):
        try:
            self._handlers.pop(func)
        except KeyError:
            pass

    async def download_media(self, media: object, file: str = None):
        result = await self._connection.download(
            media.dc_id,
            media.file_id,
            media.access_hash_rec)

        if isinstance(file, str):
            with open(file, 'wb+') as f:
                f.write(result)
                return f

        return result
