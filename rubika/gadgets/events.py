class BaseEvent(object):

    def __init__(self, func=None, users=None) -> None:
        self.func = func
        self.users = users

    def analyze(self, name, update):
        if name != type(self).__name__:
            return False

        elif callable(self.func) and not self.func(update):
            return False

        elif self.users and update.guid not in self.users:
            return False

        else:
            return True


class ChatUpdates(BaseEvent):
    pass


class MessageUpdates(BaseEvent):
    pass


class ShowActivities(BaseEvent):
    pass


class ShowNotifications(BaseEvent):
    pass


class RemoveNotifications(BaseEvent):
    pass


class GroupVoiceChatUpdates(BaseEvent):
    pass


class GroupVoiceChatParticipantUpdates(BaseEvent):
    pass
