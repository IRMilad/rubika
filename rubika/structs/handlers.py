import sys
import asyncio
from .struct import Struct
from ..gadgets import Classino

__handlers__ = [
    'ChatUpdates',
    'MessageUpdates',
    'ShowActivities',
    'ShowNotifications',
    'RemoveNotifications'
]


class BaseHandlers(Struct):
    __name__ = 'CustomHandlers'

    def __init__(self, *models, __any: bool = False, **kwargs) -> None:
        self.__models = models
        self.__any = __any

    async def __call__(self, update: dict, *args, **kwargs) -> bool:
        self.original_update = update
        if self.__models:
            for filter in self.__models:
                if callable(filter):

                    # if BaseModels test is not called
                    if isinstance(filter, type):
                        filter = filter(func=None)

                    # if it is an object, the asyncio.iscoroutinefunction cannot detect __call__ 
                    if isinstance(filter, object):
                        filter = filter.__call__
    
                    if asyncio.iscoroutinefunction(filter):
                        status = await filter(self)

                    else:
                        status = filter(self)

                    if status and self.__any:
                        return True

                    elif not status:
                        return False

        return True

class Handlers(Classino):
    def __init__(self, name, *args, **kwargs) -> None:
        self.__name__ = name
    
    def __eq__(self, value: object) -> bool:
        return BaseHandlers in value.__bases__

    def __dir__(self):
        return sorted(__handlers__)

    def __call__(self, name, *args, **kwargs):
        return self.__getattr__(name)(*args, **kwargs)

    def __getattr__(self, name):
        return self.create(name, (BaseHandlers,), __handlers__)

sys.modules[__name__] = Handlers(__name__)
