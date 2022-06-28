class ClientError(Exception):
    pass


class SocksError(ClientError):
    pass


class UnknownAuthMethod(SocksError):
    pass


class InvalidServerReply(SocksError):
    pass


class SocksConnectionError(SocksError):
    pass


class InvalidServerVersion(SocksError):
    pass


class NoAcceptableAuthMethods(SocksError):
    pass


class LoginAuthenticationFailed(SocksError):
    pass


class ConnectionError(ClientError):
    def __init__(self, message, request=None):
        self.message = (str(message))
        self.request = request


class NoConnection(ConnectionError):
    pass


class ConnectionUrlNotFound(ConnectionError):
    pass


class ConnectionInternalProblem(ConnectionError):
    pass


class RequestError(ClientError):
    def __init__(self, message, request=None, det=None) -> None:
        self.message = str(message)
        self.request = request
        self.det = det


class CancelledError(RequestError):
    pass


class StopHandler(ClientError):
    pass
