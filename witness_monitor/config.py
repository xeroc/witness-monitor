import os
import yaml


class ConfigClass(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

    def load_yaml(self, *args):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        o = open(os.path.join(dir_path, *args))
        d = yaml.load(o.read())
        self.update(d)


# load defaults
config = ConfigClass()
config.load_yaml("config-defaults.yaml")
try:
    config.load_yaml("..", "config.yaml")
except Exception:
    pass
