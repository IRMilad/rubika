import typing


class GroupValues:
    Set = 'Set'
    Unset = 'Unset'

    SetAdmin = 'SetAdmin'
    UnsetAdmin = 'UnsetAdmin'

    Hidden = 'Hidden'
    Visible = 'Visible'

    AddMember = 'AddMember'
    ViewAdmins = 'ViewAdmins'
    ViewMembers = 'ViewMembers'
    SendMessages = 'SendMessages'

    SetAdmin = 'SetAdmin'
    BanMember = 'BanMember'
    ChangeInfo = 'ChangeInfo'
    PinMessages = 'PinMessages'
    SetJoinLink = 'SetJoinLink'
    SetMemberAccess = 'SetMemberAccess'
    DeleteGlobalAllMessages = 'DeleteGlobalAllMessages'


class AddGroup(object):
    def __init__(self, title: str,
                 member_guids: typing.Union[list, str], *args, **kwargs):
        """_AddGroup_

        Args:
            title (str):
                _title_

            member_guids (list, str):
                _member guids_
        """

        if not isinstance(member_guids, list):
            member_guids = [member_guids]

        self.input = {'title': title, 'member_guids': member_guids}


class JoinGroup(object):
    def __init__(self, hash_link: str, *args, **kwargs):
        """_ChannelPreviewByJoinLink_

        Args:
            hash_link (str):
                _hash link_
        """

        self.input = {'hash_link': hash_link}


class LeaveGroup(object):
    def __init__(self, group_guid: str, *args, **kwargs):
        """_LeaveGroup_

        Args:
            group_guid (str):
                _group guid_
        """

        self.input = {'group_guid': group_guid}


class RemoveGroup(object):
    def __init__(self, group_guid: str, *args, **kwargs):
        """_RemoveGroup_

        Args:
            group_guid (str):
                _group guid_
        """

        self.input = {'group_guid': group_guid}


class GetGroupInfo(object):
    def __init__(self, group_guid: str, *args, **kwargs):
        """_GetGroupInfo_

        Args:
            group_guid (str):
                _group guid_
        """

        self.input = {'group_guid': group_guid}


class GetGroupLink(object):
    def __init__(self, group_guid: str, *args, **kwargs):
        """_GetGroupLink_

        Args:
            group_guid (str):
                _group guid_
        """

        self.input = {'group_guid': group_guid}


class SetGroupLink(object):
    def __init__(self, group_guid: str, *args, **kwargs):
        """_SetGroupLink_

        Args:
            group_guid (str):
                _group guid_
        """

        self.input = {'group_guid': group_guid}


class EditGroupInfo(object):
    def __init__(self,
                 group_guid: str,
                 title: str = None,
                 description: str = None,
                 chat_history_for_new_members: str = None,
                 ):
        """_EditGroupInfo_

        Args:
            group_guid (str):
                _group guid_

            title (str, optional):
                _title_

            description (str, optional):
                _description_

            chat_history_for_new_members (str, optional):
                _chat history for new members_. (
                        GroupValues.Hidden,
                        GroupValues.Visible
                )
        """

        self.input = {
            'title': title,
            'description': description,
            'chat_history_for_new_members': chat_history_for_new_members}

        updated_parameters = []
        for key, value in self.input.items():
            if value:
                updated_parameters.append(key)

        self.input['group_guid'] = group_guid
        self.input['updated_parameters'] = updated_parameters


class SetGroupAdmin(object):
    def __init__(self, group_guid: str,
                 member_guid: str, access_list: list,
                 action: str = GroupValues.SetAdmin, *args, **kwargs):
        """_SetGroupAdmin_

        Args:
            group_guid (str):
                _group guid_

            member_guid (str):
                _member guid_

            access_list (list):
                _access_list_ (
                    GroupValues.SetAdmin,
                    GroupValues.BanMember,
                    GroupValues.ChangeInfo,
                    GroupValues.PinMessages,
                    GroupValues.SetJoinLink,
                    GroupValues.SetMemberAccess,
                    GroupValues.DeleteGlobalAllMessages
                )

            action (str):
                _action_ . Default to GroupValues.SetAdmin (
                    GroupValues.SetAdmin,
                    GroupValues.UnsetAdmin
                )
        """

        self.input = {'action': action,
                      'group_guid': group_guid,
                      'member_guid': member_guid,
                      'access_list': access_list}


class BanGroupMember(object):
    def __init__(self, group_guid: str, member_guid: str,
                 action: str = GroupValues.Set, *args, **kwargs):
        """_BanGroupMember_

        Args:
            group_guid (str):
                _group guid_

            member_guid (str):
                _member guid_

            action (str):
                _action_ . Defaults to GroupValues.Set. (
                    GroupValues.Set,
                    GroupValues.Unset
                )
        """

        self.input = {
            'group_guid': group_guid,
            'member_guid': member_guid, 'action': action}


class AddGroupMembers(object):
    def __init__(self, group_guid: str,
                 member_guids: typing.Union[list, str], *args, **kwargs):
        """_AddGroupMembers_

        Args:
            group_guid (str):
                _group guid_
            member_guids (list, str):
                _membe guids_
        """

        if not isinstance(member_guids, list):
            member_guids = [member_guids]

        self.input = {'group_guid': group_guid, 'member_guids': member_guids}


class GetGroupAllMembers(object):
    def __init__(self, group_guid: str, search_text: str = None,
                 start_id: int = None, *args, **kwargs):
        """_GetGroupAllMembers_

        Args:
            group_guid (str):
                _group guid_

            search_text (str, optional):
                _search text_. Defaults to None.

            start_id (int, optional):
                _start id_. Defaults to None.
        """

        self.input = {'group_guid': group_guid}


class GetGroupAdminMembers(object):
    def __init__(self, group_guid: str, start_id: int = None, *args, **kwargs):
        """_GetGroupAdminMembers_

        Args:
            group_guid (str):
                _group guid_

            start_id (int, optional):
                _start id_. Defaults to None.
        """

        self.input = {'group_guid': group_guid, 'start_id': start_id}


class GetGroupMentionList(object):
    def __init__(self, group_guid: str,
                 search_mention: str = None, *args, **kwargs):
        """_GetGroupMentionList_

        Args:
            group_guid (str):
                _group guid_

            search_mention (str, optional):
                _search mention_. Defaults to None.
        """

        self.input = {'group_guid': group_guid,
                      'search_mention': search_mention}


class GetGroupDefaultAccess(object):
    def __init__(self, group_guid: str, *args, **kwargs):
        """_GetGroupDefaultAccess_

        Args:
            group_guid (str):
                _group guid_
        """

        self.input = {'group_guid': group_guid}


class SetGroupDefaultAccess(object):
    def __init__(self, group_guid: str, access_list: list, *args, **kwargs):
        """_summary_

        Args:
            group_guid (str):
                _group guid_

            access_list (list):
                _access list_: (
                    GroupValues.AddMember,
                    GroupValues.ViewAdmins,
                    GroupValues.ViewMembers,
                    GroupValues.SendMessages
                )
        """
        self.input = {'group_guid': group_guid, 'access_list': access_list}


class GroupPreviewByJoinLink(object):
    def __init__(self, hash_link: str, *args, **kwargs):
        """_GroupPreviewByJoinLink_

        Args:
            hash_link (str):
                _hash link_
        """

        self.input = {'hash_link': hash_link}


class DeleteNoAccessGroupChat(object):
    def __init__(self, group_guid: str, *args, **kwargs):
        """_DeleteNoAccessGroupChat_

        Args:
            group_guid (str):
                _group guid_
        """

        self.input = {'group_guid': group_guid}


class GetGroupAdminAccessList(object):
    def __init__(self, group_guid: str, member_guid: str, *args, **kwargs):
        """_getGroupAdminAccessList_

        Args:
            group_guid (str):
                _group guid_

            member_guid str):
                _membe guid_
        """
        self.input = {'group_guid': group_guid, 'member_guid': member_guid}
