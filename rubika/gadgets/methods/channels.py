import typing


class ChannelValues:
    Join = 'Join'
    Remove = 'Remove'
    Archive = 'Archive'

    Set = 'Set'
    Unset = 'Unset'


class AddChannel(object):
    def __init__(self, title: str, description: str = None, *args, **kwargs):
        """_summary_

        Args:
            title (str):
                title

            description (str, optional):
                _description_. Defaults to None.
        """

        self.input = {'title': title, 'description': description}


class RemoveChannel(object):
    def __init__(self, channel_guid: str, *args, **kwargs):
        """_RemoveChannel_

        Args:
            channel_guid (str):
                _channe guid_
        """

        self.input = {'channel_guid': channel_guid}


class GetChannelInfo(object):
    def __init__(self, channel_guid, *args, **kwargs):
        """_GetChannelInfo_

        Args:
            channel_guid (_type_):
                _channel guid_
        """

        self.input = {'channel_guid': channel_guid}


class EditChannelInfo(object):
    def __init__(self, channel_guid: str, title: str = None,
                 channel_type: str = None, description: str = None,
                 sign_messages: str = None, *args, **kwargs):
        """_EditChannelInfo_

        Args:
            channel_guid (str):
                _channel guid_

            title (str, optional):
                _title_. Defaults to None.

            channel_type (str, optional):
                _channel type_. Defaults to None. (
                    ChannelValues.Public,
                    ChannelValues.Private
                )

            description (str, optional):
                _description_. Defaults to None.

            sign_messages (str, optional):
                _sign messages_. Defaults to None.
        """

        self.input = {
            'title': title,
            'description': description,
            'channel_type': channel_type,
            'sign_messages': sign_messages}

        updated_parameters = []
        for key, value in self.input.items():
            if value:
                updated_parameters.append(key)
        self.input['channel_guid'] = channel_guid
        self.input['updated_parameters'] = updated_parameters


class JoinChannelAction(object):
    def __init__(self, channel_guid: str,
                 action=ChannelValues.Join, *args, **kwargs):
        """_JoinChannelAction_

        Args:
            channel_guid (str):
                _channel guid_

            action (_type_, optional):
                _action_. Defaults to ChannelValues.Join. (
                    ChannelValues.Join,
                    ChannelValues.Remove,
                    ChannelValues.Archive
                )
        """

        self.input = {'channel_guid': channel_guid, 'action': action}


class JoinChannelByLink(object):
    def __init__(self, hash_link: str, *args, **kwargs):
        """_JoinChannelByLink_

        Args:
            hash_link (str):
                _hash link_
        """

        self.input = {'hash_link': hash_link}


class AddChannelMembers(object):
    def __init__(self, channel_guid: str,
                 member_guids: typing.Union[list, str], *args, **kwargs):
        """_AddChannelMembers_

        Args:
            channel_guid (str):
                _channel guid_

            member_guids (list, str):
                _member guids_
        """

        if not isinstance(member_guids, list):
            member_guids = [member_guids]

        self.input = {'channel_guid': channel_guid,
                      'member_guids': member_guids}


class BanChannelMember(object):
    def __init__(self, channel_guid: str, member_guid: str,
                 action: str = ChannelValues.Set, *args, **kwargs):
        """_BanChannelMember_

        Args:
            channel_guid (str):
                _channel guid_

            member_guid (str):
                _member guid_

            action (str, optional):
                _action_. Defaults to ChannelValues.Set.
        """

        self.input = {'channel_guid': channel_guid,
                      'member_guid': member_guid, 'action': action}


class CheckChannelUsername(object):
    def __init__(self, username: str, *args, **kwargs):
        """_CheckChannelUsername_

        Args:
            username (str):
                _username_
        """

        self.input = {'username': username}


class ChannelPreviewByJoinLink(object):
    def __init__(self, hash_link: str, *args, **kwargs):
        """_ChannelPreviewByJoinLink_

        Args:
            hash_link (str):
                _hash link_
        """

        self.input = {'hash_link': hash_link}


class GetChannelAllMembers(object):
    def __init__(self, channel_guid: str, search_text: str = None,
                 start_id: int = None, *args, **kwargs):
        """_GetChannelAllMembers_

        Args:
            channel_guid (str):
                _channel guid_

            search_text (str, optional):
                _search text_. Defaults to None.

            start_id (int, optional):
                _start id_. Defaults to None.
        """

        self.input = {'channel_guid': channel_guid,
                      'search_text': search_text, 'start_id': start_id}


class GetChannelAdminMembers(object):
    def __init__(self, channel_guid: str,
                 start_id: int = None, *args, **kwargs):
        """_GetChannelAdminMembers_

        Args:
            channel_guid (str):
                _channel guid_

            start_id (int, optional):
                _start id_. Defaults to None.
        """

        self.input = {'channel_guid': channel_guid, 'start_id': start_id}


class UpdateChannelUsername(object):
    def __init__(self, channel_guid: str, username: str, *args, **kwargs):
        """_UpdateChannelUsername_

        Args:
            channel_guid (str):
                _channel guid_

            username (str):
                _user name_
        """

        self.input = {'channel_guid': channel_guid, 'username': username}


class GetChannelLink(object):
    def __init__(self, channel_guid: str, *args, **kwargs):
        """_GetChannelLink_

        Args:
            channel_guid (str):
                _channel guid_
        """

        self.input = {'channel_guid': channel_guid}


class SetChannelLink(object):
    def __init__(self, channel_guid: str, *args, **kwargs):
        """_SetChannelLink_

        Args:
            channel_guid (str):
                _channel guid_
        """

        self.input = {'channel_guid': channel_guid}


class GetChannelAdminAccessList(object):
    def __init__(self, channel_guid: str, member_guid: str, *args, **kwargs):
        """_SetChannelLink_

        Args:
            channel_guid (str):
                _channel guid_

            member_guid (str):
                _member guid_
        """

        self.input = {'channel_guid': channel_guid, 'member_guid': member_guid}
