# -*- coding: utf-8 -*-
"""Module for the ```grblcli``` command line interface.

An entrypoint for ```grbl``` module.
"""
import os
import time

import click

from .Grbl import Grbl


@click.group()
@click.version_option()
@click.option(
    "--port",
    metavar="port",
    default="/dev/ttyUSB0",
    help="Grbl port. [Default: {}]".format("/dev/ttyUSB0"),
)
@click.option(
    "--baudrate",
    metavar="baudrate",
    default=115200,
    help="Grbl baud rate . [Default: 115200]",
)
@click.option("--debug/--no-debug", default=False)
@click.option("--home/--no-home", default=False, help="Perform a $H homing if $22=1")
@click.pass_context
def cli(ctx, port, baudrate, debug, home):
    """Grbl command line interface entry point.

    grblcli is a utility for interacting with Grbl from the
    command line.
    """
    # click.echo("Debug mode is %s" % ("on" if debug else "off"))
    ctx.obj = dict()
    ctx.obj["DEBUG"] = debug
    ctx.obj["GRBL_CFG"] = {"port": port, "baudrate": baudrate}
    ctx.obj["HOME"] = home


@cli.command("aimlaser")
@click.pass_context
def aimlaser(ctx):
    """Aim the laser.

    Turns the laser on to the minimal power setting for aiming.
    Example
    -------

    $ grblcli aimlaser
    """
    
    grbl = Grbl(**ctx.obj["GRBL_CFG"])
    grbl.reset()
    grbl.cmd("$X")
    if ctx.obj["HOME"]:
        if grbl.hard_limits==1:
            grbl.home()        
    grbl.aim_laser()


@cli.command("status")
@click.pass_context
def status(ctx):
    """Get Grbl status.

    Example
    -------

    $ grblcli status
    """
    grbl = Grbl(**ctx.obj["GRBL_CFG"])
    grbl.reset()
    time.sleep(0.1)
    grbl.status
    print(grbl.status)


@cli.command("print_settings")
@click.pass_context
def print_settings(ctx):
    """Prints the current grbl device settings.

    Useful for saving current grbl configuration to a file.
    Good practice to dump a pre-built flash config so that you can re-load it if needed.

    Example
    -------

    $ grblcli print_settings > machine.config
    """
    grbl = Grbl(**ctx.obj["GRBL_CFG"])
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
    """Load grbl device settings from a file.

    Useful for loading configurations from known good files.

    Example
    -------

    $ grblcli load_settings machine.config
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

    grbl = Grbl(**ctx.obj["GRBL_CFG"])
    print(grbl.run("\n".join(settings)))


@cli.command("run")
@click.argument("ngc_file")
@click.pass_context
def run(ctx, ngc_file):
    """Run a gcode file on the grbl device.

    Example
    -------

    $ grblcli run --zero file.ngc

    $ grblcli run --home file.ngc
    """
    # For S,C,&J, Christmas 2019
    # For C&J, halloween 2019.
    grbl = Grbl(**ctx.obj["GRBL_CFG"])
    grbl.reset()
    grbl.cmd("$X")
    if ctx.obj["HOME"]:
        if grbl.hard_limits==1:
            grbl.home()        
    
    grbl.cmd("G92X0.0Y0.0Z0.0")
    grbl.cmd("G21")
    with open(ngc_file, "r") as fid:
        grbl.run(fid.readlines())
