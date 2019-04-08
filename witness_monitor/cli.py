import click
from uptick.main import main
from uptick.decorators import unlock, online
from bitshares.witness import Witness
from bitshares.instance import set_shared_blockchain_instance
from collections import Counter
from pprint import pprint
from . import Monitor
from .config import config
from .features import Feature


monitor = Monitor(config)
FAIL_LINE = "{witness}: {description}: {error}"
SUCC_LINE = "{witness}: {description}"


@main.command()
def test():
    monitor.test()
    for fail in Feature.get_failures():
        click.echo(click.style(FAIL_LINE.format(**fail), fg="red"))
    for success in Feature.get_successes():
        click.echo(click.style(SUCC_LINE.format(**success), fg="green"))


@main.command()
@click.pass_context
@click.option("--account")
@online
@unlock
def check(ctx, account):
    ctx.blockchain.bundle = True
    monitor.test()
    monitor.action()
    ctx.blockchain.broadcast()


if __name__ == "__main__":
    main()
