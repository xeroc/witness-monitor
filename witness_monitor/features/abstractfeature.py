from ..storage import Cache
from ..utils import AutoRegister


class Feature(metaclass=AutoRegister):
    _subclasses = {}
    failures = []
    successes = []

    def __init__(self, feature={}, config={}, data={}):
        self.config = config
        self.data = data
        self.feature = feature
        self.failed = False
        self.on_success = dict()
        self.on_failure = dict()

    @property
    def params(self):
        return self.feature[self.__tag__]

    @property
    def cache(self):
        return Cache

    @classmethod
    def register_subclass(klass, cls):
        if hasattr(cls, "__tag__"):
            klass._subclasses[cls.__tag__] = cls

    @classmethod
    def get_successes(klass):
        for tag in klass._subclasses:
            return klass._subclasses[tag].successes

    @classmethod
    def get_failures(klass):
        for tag in klass._subclasses:
            return klass._subclasses[tag].failures

    @classmethod
    def get_class(klass, tag):
        if tag in klass._subclasses:
            return klass._subclasses[tag]

    def test(self):
        raise NotImplementedError("{}.test()".format(self.__class__.__name__))

    def success(self, witness, **kwargs):
        self.failed = False
        data = {
            "witness": witness,
            "tag": self.__tag__,
            "description": self.feature.get("description"),
            "actions": self.feature.get("on_success"),
            **kwargs,
        }
        self.successes.append(data)
        self.on_success[witness] = data

    def failure(self, witness, **kwargs):
        self.failed = True
        data = {
            "witness": witness,
            "tag": self.__tag__,
            "description": self.feature.get("description"),
            "weight": float(self.feature.get("weight", 1)),
            "actions": self.feature.get("on_failure"),
            **kwargs,
        }
        self.failures.append(data)
        self.on_failure[witness] = data
