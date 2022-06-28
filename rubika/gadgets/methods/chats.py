import time
import typing


class ChatValues:
    Mute = 'Mute'
    Unmute = 'Unmute'

    Typing = 'Typing'
    Uploading = 'Uploading'
    Recording = 'Recording'

    Text = 'Text'
    Hashtag = 'Hashtag'


class GetChats(object):
    def __init__(self, start_id: int = None, *args, **kwargs):
        """_GetChats_

        Args:
            start_id (int, optional):
                _start id_. Defaults to None.
        """

        self.input = {'start_id': start_id}


class SeenChats(object):
    def __init__(self, seen_list: dict):
        """_SeenChats_

        Args:
            seen_list (dict):
                _seen list_
        """

        self.input = {'seen_list': seen_list}


class GetChatAds(object):
    def __init__(self, state: int = None, *args, **kwargs):
        """_GetChatAds_

        Args:
            state (int, optional):
                _state_. Defaults to int(time.time()).
        """

        if not state:
            state = int(time.time())
        self.input = {'state': state}


class SetActionChat(object):
    def __init__(self, object_guid: str,
                 action: str = ChatValues.Mute, *args, **kwargs):
        """_SetActionChat_

        Args:
            object_guid (str):
                _object guid_

            action (str, optional):
                _action_. Defaults to ChatValues.Mute. (
                    ChatValues.Mute,
                    ChatValues.Unmute
                )
        """

        self.input = {'object_guid': object_guid, 'action': action}


class GetAbsObjects(object):
    def __init__(self,
                 objects_guids: typing.Union[list, str], *args, **kwargs):
        """_GetAbsObjects_

        Args:
            objects_guids (list):
                _objects guids_
        """

        if not isinstance(objects_guids, list):
            objects_guids = [objects_guids]
        self.input = {'objects_guids': objects_guids}


class GetChatsUpdates(object):
    def __init__(self, state: int = None, *args, **kwargs):
        """_GetChatsUpdates_

        Args:
            state (int, optional):
                _state_. int(time.time())
        """

        if not state:
            state = int(time.time())
        self.input = {'state': state}


class SendChatActivity(object):
    def __init__(self, object_guid: str,
                 activity: str = ChatValues.Typing, *args, **kwargs):
        """_SendChatActivity_

        Args:
            object_guid (str):
                _object guid_

            activity (str, optional):
                _activity_. Defaults to ChatValues.Typing.(
                    ChatValues.Typing,
                    ChatValues.Uploading,
                    ChatValues.Recording
                )
        """

        self.input = {'object_guid': object_guid, 'activity': activity}


class DeleteChatHistory(object):
    def __init__(self, object_guid: str, *args, **kwargs):
        """_DeleteChatHistory_

        Args:
            object_guid (str):
                _object guid_
        """

        self.input = {'object_guid': object_guid}


class SearchChatMessages(object):
    def __init__(self, object_guid: str, search_text: str,
                 search_type: str = ChatValues.Hashtag, *args, **kwargs):
        """_SearchChatMessages_

        Args:
            object_guid (str):
                _object guid_

            search_text (str):
                _search text_

            search_type (str, optional):
                _search type_. Defaults to ChatValues.Hashtag. (
                    ChatValues.Text,
                    ChatValues.Hashtag
                )
        """

        self.input = {
            'object_guid': object_guid,
            'search_text': search_text, 'type': search_type}