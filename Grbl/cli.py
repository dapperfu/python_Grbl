# -*- coding: utf-8 -*-
"""Module for the ```grbl2.py``` command line interface.

An entrypoint for ```grbl2``` module.
"""
import os

import click

import Grbl


@click.group()
@click.version_option()
def cli():
    """Grbl command line interface entry point.

    grbl.py is a utility for interacting with Grbl from the
    command line.
    """


@cli.command("aimlaser")
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
def aimlaser(port: str, baudrate: int):
    """Aim the laser.

    Turns the laser on to the minimal power setting for aiming.
    Example
    -------

    $ grbl2.py aimlaser
    """
    grbl = Grbl.Grbl(port=port)
    grbl.aim_laser()
