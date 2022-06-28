import re
import typing
from ..gadgets import methods
from .updateStruct import UpdateStruct


class BaseHandlers(UpdateStruct):
    def __call__(self, name: str, update: dict):
        UpdateStruct.__init__(self, name=name, data=update)
        return self


class ChatUpdates(BaseHandlers):
    def __init__(self,
                 func: typing.Callable = None,
                 guids: typing.Union[list, str] = None,
                 block: bool = None, *args, **kwargs):

        self._func = func
        self._guids = guids
        self._block = block

    @property
    def raw_text(self):
        """_raw_text_

        Returns:
            (str, None): last message text
        """

        if self.chat.last_message:
            return self.chat.last_message.text

    @property
    def analyze(self) -> bool:
        try:
            if self._guids:
                user_guid = self.user_guid
                object_guid = self.object_guid

                if user_guid in self._guids or object_guid in self._guids:
                    if self._block is True:
                        return False

            if callable(self._func):
                if not self.__func(self):
                    return False

        except Exception:
            return False

        else:
            return True

    async def get_user(self, *args, **kwargs):
        """_get_user_

        Returns:
            UpdateStruct: result
        """

        return await self._client(
            methods.users.GetUserInfo(self.user_guid))

    async def get_object(self, *args, **kwargs):
        """_get_object_

        Returns:
            UpdateStruct: result
        """
        if self.type == 'User':
            return await self.get_user(*args, **kwargs)

        elif self.type == 'Group':
            return await self._client(
                methods.groups.GetGroupInfo(self.object_guid))


class MessageUpdates(BaseHandlers):
    def __init__(self,
                 func: typing.Callable = None,
                 guids: typing.Union[list, str] = None,
                 block: bool = None,
                 pattern: str = None, *args, **kwargs):

        self._func = func
        self._guids = guids
        self._block = block
        self._pattern = pattern

    @property
    def analyze(self) -> bool:
        try:
            if self._guids:
                user_guid = self.user_guid
                author_guid = self.message.author_object_guid
                if user_guid in self._guids or author_guid in self._guids:
                    if self._block is True:
                        return False

            if callable(self._func):
                if not self.__func(self):
                    return False

            if self.raw_text and self._pattern:
                self.pattern_match = re.search(
                    self._pattern, self.raw_text, re.DOTALL)

                if self.pattern_match is None:
                    return False

        except Exception:
            return False

        else:
            return True

    @property
    def raw_text(self):
        """_raw_text_

        Returns:
            (str, None): message text
        """

        return self.message.text

    async def edit(self, text: str, *args, **kwargs):
        """_edit_

        Args:
            text (str):
                text

        Returns:
            UpdateStruct: result
        """

        return await self._client(
            methods.messages.EditMessage(
                object_guid=self.object_guid,
                message_id=self.message_id,
                text=text)
        )

    async def reply(self,
                    text: str = None,
                    file: typing.Union[object, dict] = None,
                    thumb: typing.Union[object, dict] = None,
                    send_type: str = methods.messages.MessageValues.File,
                    *args, **kwargs):
        """_reply_

        Args:
            text (str, optional):
                _text_. Defaults to None.
            file (object, dict, optional):
                _file_. Defaults to None.

            thumb (object, dict, optional):
                _thumb_. Defaults to None.

            send_type (str, optional):
                _send type_. Defaults to methods.messages.MessageValues.File.(
                    methods.messages.MessageValues.File,
                    methods.messages.MessageValues.Image
                )

        Returns:
            UpdateStruct: result
        """

        return await self._client(
            methods.messages.SendMessage(
                object_guid=self.object_guid,
                reply_to=self.message_id,
                text=text, file=file, thumb=thumb, send_type=send_type)
        )

    async def set_pin(self,
                      action: str = methods.messages.MessageValues.Pin,
                      *args, **kwargs):
        """_set_pin_

        Args:
            action (str, optional):
            _action_. Defaults to methods.messages.MessageValues.Pin.(
                methods.messages.MessageValues.Pin,
                methods.messages.MessageValues.Unpin
            )

        Returns:
            UpdateStruct: result
        """

        return await self._client(
            methods.messages.SetPinMessage(
                object_guid=self.object_guid,
                message_id=self.message_id,
                action=action)
        )

    async def delete(self, *args, **kwargs):
        """_delete_

        Returns:
            UpdateStruct: result
        """

        return await self._client(
            methods.messages.DeleteMessages(object_guid=self.object_guid,
                                            message_ids=self.message_id)
        )

    async def forward(self, to_object_guid: str, *args, **kwargs):
        """_forward_

        Args:
            to_object_guid (str):
                _to object guid_

        Returns:
            UpdateStruct: result
        """

        return await self._client(
            methods.messages.ForwardMessages(
                message_ids=self.message_id,
                to_object_guid=to_object_guid,
                from_object_guid=self.object_guid)
        )

    async def get_user(self, *args, **kwargs):
        """_get_user_

        Returns:
            UpdateStruct: result
        """

        return await self._client(
            methods.users.GetUserInfo(self.user_guid))

    async def get_object(self, *args, **kwargs):
        """_get_object_

        Returns:
            UpdateStruct: result
        """
        if self.type == 'User':
            return await self.get_user(*args, **kwargs)

        elif self.type == 'Group':
            return await self._client(
                methods.groups.GetGroupInfo(self.object_guid))


class ShowActivities(BaseHandlers):
    def __init__(self,
                 func: typing.Callable = None,
                 guids: typing.Union[list, str] = None,
                 block: bool = None,
                 types: list = [], *args, **kwargs):

        self._func = func
        self._guids = guids
        self._block = block
        self._types = types

    @property
    def analyze(self) -> bool:
        try:
            if self._guids:
                object_guid = self.object_guid
                activity_guid = self.user_activity_guid
                if activity_guid in self._guids or object_guid in self._guids:
                    if self._block is True:
                        return False

            if callable(self._func):
                if not self.__func(self):
                    return False

            if self._types:
                if self.type not in self._types:
                    return False

        except Exception:
            return False

        else:
            return True

    async def get_user(self, *args, **kwargs):
        """_get_user_

        Returns:
            UpdateStruct: result
        """
        return await self._client(
            await methods.users.GetUserInfo(self.user_activity_guid))

    async def get_object(self, *args, **kwargs):
        """_get_object_

        Returns:
            UpdateStruct: result
        """
        if self.object_type == 'User':
            return await self.get_user(*args, **kwargs)

        elif self.get_object == 'Group':
            return await self._client(
                methods.groups.GetGroupInfo(self.object_guid))


class ShowNotifications(BaseHandlers):
    def __init__(self,
                 func: typing.Callable = None,
                 guids: typing.Union[list, str] = None,
                 block: bool = None,
                 types: list = [],
                 pattern: str = None, *args, **kwargs):

        self._func = func
        self._guids = guids
        self._block = block
        self._types = types
        self._pattern = pattern

    @property
    def analyze(self) -> bool:
        try:
            if self._guids:
                if self.message_data.object_guid in self._guids:
                    if self._block is True:
                        return False

            if callable(self._func):
                if not self.__func(self):
                    return False

            if self.raw_text and self._pattern:
                self.pattern_match = re.search(
                    self._pattern, self.raw_text, re.DOTALL)

                if self.pattern_match is None:
                    return False

        except Exception:
            return False

        else:
            return True

    @property
    def raw_text(self) -> str:
        if isinstance(self.text, str):
            return self.text

        elif isinstance(self.title, str):
            return self.title

    async def seen(self, *args, **kwargs):
        """_seen_

        Returns:
            UpdateStruct: result
        """

        return await self._client(
            methods.chats.SeenChats(
                {self.message_data.object_guid: self.message_data.message_id})
        )

    async def get_user(self, *args, **kwargs):
        """_get_user_

        Returns:
            UpdateStruct: result
        """

        return await self._client(methods.users.GetUserInfo(self.user_guid))

    async def get_object(self, *args, **kwargs):
        """_get_object_

        Returns:
            UpdateStruct: result
        """

        if self.message_data.object_type == 'User':
            return await self.get_user(*args, **kwargs)

        elif self.message_data.object_type == 'Group':
            return await self._client(
                methods.groups.GetGroupInfo(self.message_data.object_guid)
            )


class RemoveNotifications(BaseHandlers):
    def __init__(self,
                 func: typing.Callable = None,
                 guids: typing.Union[list, str] = None,
                 block: bool = None,
                 pattern: str = None, *args, **kwargs):

        self._func = func
        self._guids = guids
        self._block = block
        self._pattern = pattern

    @property
    def analyze(self) -> bool:
        try:
            if self._guids:
                if self.user_guid in self._guids:
                    if self._block is True:
                        return False

            if callable(self._func):
                if not self.__func(self):
                    return False

        except Exception:
            return False

        else:
            return True

    async def get_user(self, *args, **kwargs):
        """_get_user_

        Returns:
            UpdateStruct: result
        """

        return await self._client(methods.users.GetUserInfo(self.user_guid))

    async def get_object(self, *args, **kwargs):
        """_get_object_

        Returns:
            UpdateStruct: result
        """

        if self.remove_to_data.object_type == 'User':
            return await self.get_user(*args, **kwargs)

        elif self.remove_to_data.object_type == 'Group':
            return await self._client(
                methods.groups.GetGroupInfo(self.remove_to_data.object_guid)
            )
