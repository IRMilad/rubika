class UserValues(object):
    Block = 'Block'
    Unblock = 'Unblock'


class GetUserInfo(object):
    def __init__(self, user_guid: str, *args, **kwaegs):
        """_GetUserInfo_

        Args:
            user_guid (str):
                _user guid_
        """

        self.input = {'user_guid': user_guid}


class SetBlockUser(object):
    def __init__(self, user_guid: str,
                 action: str = UserValues.Block, *args, **kwargs):
        """_SetBlockUser_

        Args:
            user_guid (str):
                _user guid_
            action (str, optional):
                _description_. Defaults to UserValues.Block.
        """

        self.input = {'user_guid': user_guid, 'action': action}



class SearchGlobalObjects(object):
    def __init__(self, search_text: str, *args, **kwargs):
        """_SearchGlobalObjects_

        Args:
            search_text (str):
                _search text_
        """

        self.input = {'search_text': search_text}


class DeleteUserChat(object):
    def __init__(self, user_guid: str,
                 last_deleted_message_id: str = None, *args, **kwargs):
        """_DeleteUserChat_

        Args:
            user_guid (str):
                _use guid_
            last_deleted_message_id (str, optional):
                _last deleted message id_. Defaults to None.
        """

        self.input = {'user_guid': user_guid,
                      'last_deleted_message_id': last_deleted_message_id}


class CheckUserUsername(object):
    def __init__(self, username: str, *args, **kwargs):
        """_CheckUserUsername_

        Args:
            username (str):
                _username_
        """

        self.input = {'username': username}


class UploadAvatar(object):
    def __init__(self, object_guid: str,
                 main_file_id: str, thumbnail_file_id: str, *args, **kwargs):
        """_UploadAvatar_

        Args:
            object_guid (str):
                _object guid_
            main_file_id (str):
                _main file id_
            thumbnail_file_id (str):
            _thumbnail fil id_
        """

        self.input = {
            'object_guid': object_guid,
            'main_file_id': main_file_id,
            'thumbnail_file_id': thumbnail_file_id}


class DeleteAvatar(object):
    def __init__(self, object_guid: str, avatar_id: str, *args, **kwargs):
        """_DeleteAvatar_

        Args:
            object_guid (str):
                _object guid_
            avatar_id (str):
                _avatar id_
        """

        self.input = {'object_guid': object_guid, 'avatar_id': avatar_id}


class GetAvatars(object):
    def __init__(self, object_guid: str, *args, **kwargs):
        """_GetAvatars_

        Args:
            object_guid (str):
                _object guid_
        """

        self.input = {'object_guid': object_guid}
