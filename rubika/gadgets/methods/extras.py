
class ExtraValues:
    pass


class GetObjectByUsername(object):
    def __init__(self, username: str, *args, **kwargs):
        """_GetObjectByUsername_

        Args:
            username (str):
                _username_
        """

        self.input = {'username': username}


class GetLinkFromAppUrl(object):
    def __init__(self, app_url: str, *args, **kwargs):
        """_GetLinkFromAppUrl_

        Args:
            app_url (str):
                _app url_
        """

        self.input = {'app_url': app_url}