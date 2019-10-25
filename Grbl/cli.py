# -*- coding: utf-8 -*-
"""Module for the ```grbl.py``` command line interface.

An entrypoint for ```grbl``` module.
"""
import os

import click

import Grbl


@click.group()
@click.version_option()
@click.option(
    "--port",
    metavar="port",
    default="/dev/ttyUSB0",
    help="Weight file. [Default: {}]".format("/dev/ttyUSB0"),
)
@click.option(
    "--baudrate",
    metavar="baudrate",
    default=115200,
    help="Weight file. [Default: 115200]",
)
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def cli(ctx, port, baudrate, debug):
    """Grbl command line interface entry point.

    grbl.py is a utility for interacting with Grbl from the
    command line.
    """
    # click.echo("Debug mode is %s" % ("on" if debug else "off"))
    ctx.obj = dict()
    ctx.obj["DEBUG"] = debug
    ctx.obj["GRBL_CFG"] = {"port": port, "baudrate": baudrate}


@cli.command("aimlaser")
@click.pass_context
def aimlaser(ctx):
    """Aim the laser.

    Turns the laser on to the minimal power setting for aiming.
    Example
    -------

    $ grbl.py aimlaser
    """
    grbl = Grbl.Grbl(**ctx.obj["GRBL_CFG"])
    grbl.aim_laser()


@cli.command("status")
@click.pass_context
def status(ctx):
    """Get Grbl status

    Example
    -------

    $ grbl.py status
    """
    grbl = Grbl.Grbl(**ctx.obj["GRBL_CFG"])
    print(grbl.status)


@cli.command("print_config")
@click.pass_context
def print_settings(ctx):
    """Prints the current grbl device settings

    Example
    -------

    $ grbl.py print_settings > machine.config
    """
    grbl = Grbl.Grbl(**ctx.obj["GRBL_CFG"])
    grbl.reset()
    grbl_settings = grbl.cmd("$$")
    #    assert grbl_settings[0] == "ok"
    #    assert grbl_settings[-1] == "ok"
    print("\n".join(grbl_settings[1:-1]))


import sys

from .Grbl import settings_key_dict


@cli.command("load_settings")
@click.argument("settings_file", type=click.File("rb"))
@click.pass_context
def load_settings(ctx, settings_file):
    """Load grbl device settings from a file
    """
    print(",Loading Settings:,")
    settings = list()
    for setting in settings_file.readlines():
        setting = setting.decode("UTF-8").strip()
        if setting.startswith(";"):
            continue
        settings.append(setting)
        key, value = setting.split("=")
        print(f"{key},{settings_key_dict[key]},{value}")

    grbl = Grbl.Grbl(**ctx.obj["GRBL_CFG"])
    print(grbl.run("\n".join(settings)))
