from ..storage import Cache
from ..utils import AutoRegister


class Action(metaclass=AutoRegister):
    _subclasses = {}

    def __init__(self, action, config={}, result=None):
        self.config = config
        self.action = action
        self.result = result

    @classmethod
    def register_subclass(klass, cls):
        if hasattr(cls, "__tag__"):
            klass._subclasses[cls.__tag__] = cls

    @classmethod
    def get_class(klass, tag):
        if tag in klass._subclasses:
            return klass._subclasses[tag]

    @property
    def cache(self):
        return Cache

    @property
    def params(self):
        return self.config.get("actions", {}).get(self.__tag__)
