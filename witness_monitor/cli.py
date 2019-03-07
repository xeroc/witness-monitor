import click
from pprint import pprint
from . import Monitor
from .config import config
from .features import Feature


monitor = Monitor(config)
FAIL_LINE = "{witness}: {description}: {error}"
SUCC_LINE = "{witness}: {description}"


@click.group()
def main():
    pass


@main.command()
def test():
    monitor.test()
    for fail in Feature.get_failures():
        click.echo(click.style(FAIL_LINE.format(**fail), fg="red"))
    for success in Feature.get_successes():
        click.echo(click.style(SUCC_LINE.format(**success), fg="green"))


if __name__ == "__main__":
    main()
