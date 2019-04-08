import os
import yaml
import click
from .abstractaction import Action
from datetime import datetime


class Jekyll(Action):

    __tag__ = "jekyll"

    def fire(self, witness):
        reason = yaml.dump(self.result)
        string = """---
date: {:%Y-%m-%d %H:%M:%S}
witness: {witness}
{reason}
---""".format(
            datetime.utcnow(), witness=witness, reason=reason
        )

        assert "dest" in self.params
        dest = self.params.get("dest")

        filename = os.path.join(
            dest, "{:%Y-%m-%d-%H%M%S.%f}.md".format(datetime.utcnow())
        )

        with open(filename, "w") as fid:
            fid.write(string)
