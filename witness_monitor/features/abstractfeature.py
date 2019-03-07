from ..storage import Cache


class AutoRegister(type):
    def __new__(mcs, name, bases, classdict):
        new_cls = type.__new__(mcs, name, bases, classdict)
        for b in bases:
            if hasattr(b, "register_subclass"):
                b.register_subclass(new_cls)
        return new_cls


class Feature(metaclass=AutoRegister):
    _subclasses = {}
    failures = []
    successes = []

    def __init__(self, feature={}, config={}, data={}):
        self.config = config
        self.data = data
        self.feature = feature
        self.failed = False

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
        self.successes.append(
            {
                "witness": witness,
                "tag": self.__tag__,
                "description": self.feature.get("description"),
                **kwargs,
            }
        )

    def failure(self, witness, **kwargs):
        self.failed = True
        self.failures.append(
            {
                "witness": witness,
                "tag": self.__tag__,
                "description": self.feature.get("description"),
                **kwargs,
            }
        )
