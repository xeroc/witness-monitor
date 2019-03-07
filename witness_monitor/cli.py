import click
from uptick.main import main
from uptick.decorators import unlock, online
from bitshares.witness import Witness
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
    ctx.blockchain.nobroadcast = True
    monitor.test()
    failed_witnesses = Counter()
    for fail in Feature.get_failures():
        failed_witnesses[fail["witness"]] += fail["weight"]

    if not config.get("actions"):
        return

    disapprovewitnesses = list()
    if config["actions"].get("disapprove"):
        threshold = config["actions"]["disapprove"].get("threshold", 1)
        for failed_witness, weight in failed_witnesses.items():
            if weight > threshold:
                click.echo(
                    click.style(
                        "Disapproving witness {}".format(failed_witness),
                        fg="bright_yellow",
                    )
                )
                disapprovewitnesses.append(failed_witness)
        click.echo(
            ctx.blockchain.disapprovewitness(disapprovewitnesses, account=account)
        )


if __name__ == "__main__":
    main()
