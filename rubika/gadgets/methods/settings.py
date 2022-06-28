import time


class SettingValues:
    Nobody = 'Nobody'
    Everybody = 'Everybody'
    MyContacts = 'MyContacts'

    Bots = 'Bots'
    Groups = 'Groups'
    Contacts = 'Contacts'
    Channels = 'Channels'
    NonConatcts = 'NonConatcts'


class SetSetting(object):
    def __init__(self,
                 show_my_last_online=None,
                 show_my_phone_number=None,
                 show_my_profile_photo=None,
                 link_forward_message=None,
                 can_join_chat_by=None, *args, **kwargs):

        """_SetSetting_

        Args:
            show_my_last_online (str, optional):
                _show my last online_. (
                    SettingValues.Everybody,
                        SettingValues.MyContacts,
                            SettingValues.Nobody)

            show_my_phone_number (str, optional):
                _show my phone_number . (
                    SettingValues.Everybody,
                        SettingValues.MyContacts,
                            SettingValues.Nobody)

            show_my_profile_photo (str, optional):
                _show my profile photo_. (
                    SettingValues.Everybody,
                        SettingValues.MyContacts)

            link_forward_message (str, optional):
                _description_. (
                    SettingValues.Everybody,
                        SettingValues.MyContacts,
                            SettingValues.Nobody)

            can_join_chat_by (str, optional):
                _description_. (
                    SettingValues.Everybody,
                        SettingValues.MyContacts)
        """

        self.input = {
            'settings': {
                'can_join_chat_by': can_join_chat_by,
                'show_my_last_online': show_my_last_online,
                'show_my_phone_number': show_my_phone_number,
                'link_forward_message': link_forward_message,
                'show_my_profile_photo': show_my_profile_photo
            }
        }


class AddFolder(object):
    def __init__(self, name: str,
                 include_chat_types: list = [],
                 exclude_chat_types: list = [],
                 include_object_guids: list = [],
                 exclude_object_guids: list = [], *args, **kwargs):
        """_AddFolder_

        Args:
            name (str):
                _name_

            include_chat_types (list, optional):
                _include chat types_. Defaults to []. (
                    SettingValues.Bots,
                    SettingValues.Groups,
                    SettingValues.Contacts,
                    SettingValues.Channels,
                    SettingValues.NonConatcts
                )

            exclude_chat_types (list, optional):
                _exclude chat types_. Defaults to []. (
                    SettingValues.Bots,
                    SettingValues.Groups,
                    SettingValues.Contacts,
                    SettingValues.Channels,
                    SettingValues.NonConatcts
                )

            include_object_guids (list, optional):
                _include object guids_. Defaults to [].

            exclude_object_guids (list, optional):
                _exclude object guids_. Defaults to [].
        """

        self.input = {'name': name,
                      'include_chat_types': include_chat_types,
                      'exclude_chat_types': exclude_chat_types,
                      'include_object_guids': include_object_guids,
                      'exclude_object_guids': exclude_object_guids}


class GetFolders(object):
    def __init__(self, last_state: int = None, *args, **kwargs):
        """_GetFolders_

        Args:
            last_state (int, optional):
                _last state_. Defaults to int(time.time()).
        """

        if not last_state:
            last_state = int(time.time())
        self.input = {'last_state': last_state}


class EditFolder(object):
    def __init__(self, folder_id: str,
                 name: str = None,
                 include_chat_types: list = [],
                 exclude_chat_types: list = [],
                 include_object_guids: list = [],
                 exclude_object_guids: list = [], *args, **kwargs):
        """_EditFolder_

        Args:
            folder_id (str):
                _folder id_
                    Args:
            name (str, optional):
                _name_

            include_chat_types (list, optional):
                _include chat types_. Defaults to []. (
                    SettingValues.Bots
                    SettingValues.Groups
                    SettingValues.Contacts
                    SettingValues.Channels
                    SettingValues.NonConatcts
                )

            exclude_chat_types (list, optional):
                _exclude chat types_. Defaults to []. (
                    SettingValues.Bots
                    SettingValues.Groups
                    SettingValues.Contacts
                    SettingValues.Channels
                    SettingValues.NonConatcts
                )

            include_object_guids (list, optional):
                _include object guids_. Defaults to [].

            exclude_object_guids (list, optional):
                _exclude object guids_. Defaults to [].
        """

        self.input = {
            'name': name,
            'include_chat_types': include_chat_types,
            'exclude_chat_types': exclude_chat_types,
            'include_object_guids': include_object_guids,
            'exclude_object_guids': exclude_object_guids}

        updated_parameters = []
        for key, value in self.input.items():
            if value:
                updated_parameters.append(key)

        self.input['folder_id'] = folder_id
        self.input['updated_parameters'] = updated_parameters


class DeleteFolder(object):
    def __init__(self, folder_id: str, *args, **kwargs):
        """_DeleteFolder_

        Args:
            folder_id (str):
                _folder id_
        """

        self.input = {'folder_id': folder_id}


class GetSuggestedFolders(object):
    pass


class UpdateProfile(object):
    def __init__(self, first_name: str = None,
                 last_name: str = None, bio: str = None, *args, **kwargs):
        """_UpdateProfile_

        Args:
            first_name (str, optional):
                _first name_. Defaults to None.

            last_name (str, optional):
                _last name_. Defaults to None.

            bio (str, optional):
                _bio_. Defaults to None.
        """

        self.input = {'bio': bio, 'first_name': first_name,
                      'last_name': last_name}

        updated_parameters = []
        for key, value in self.input.items():
            if value:
                updated_parameters.append(key)
        self.input['updated_parameters'] = updated_parameters


class UpdateUsername(object):
    def __init__(self, username: str, *args, **kwargs):
        """_UpdateUsername_

        Args:
            username (str):
                _username_
        """

        self.input = {'username': username}


class GetPrivacySetting(object):
    pass


class GetBlockedUsers(object):
    pass


class GetMySessions(object):
    pass


class TerminateSession(object):
    def __init__(self, session_key: str, *args, **kwargs):
        """_TerminateSession_

        Args:
            session_key (str):
                _session key_
        """

        self.input = {'session_key': session_key}


class GetTwoPasscodeStatus(object):
    pass


class SetupTwoStepVerification(object):
    def __init__(self, password: str, hint: str,
                 recovery_email: str = None, *args, **kwargs):
        """_SetupTwoStepVerification_

        Args:
            password (str):
                _two-step password_

            hint (str):
                _hint_

            recovery_email (_type_, optional):
                _email_. Defaults to None.
        """

        self.input = {'hint': hint, 'password': password,
                      'recovery_email': recovery_email}
