import click
from .abstractaction import Action


class Log(Action):

    __tag__ = "log"

    def fire(self, witness):
        account = self.params.get("account", None)
        click.echo(
            click.style(
                "Disapproving witness {} from {}: {}".format(
                    witness, account, self.result
                ),
                fg="bright_yellow",
            )
        )
