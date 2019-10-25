import time
import uuid

import click
from click.testing import CliRunner

from grbl import cli


def test_cli_status(cnc, request):
    grbl_cfg = {
        "port": request.config.getoption("--port"),
        "baudrate": request.config.getoption("--baudrate"),
    }
    runner = CliRunner()
    result = runner.invoke(cli, ["status"])
    assert result.exit_code == 0
    print(grbl_cfg)
    print(result.output)


def test_cli_print_settings(cnc, request):
    grbl_cfg = {
        "port": request.config.getoption("--port"),
        "baudrate": request.config.getoption("--baudrate"),
    }
    runner = CliRunner()
    result = runner.invoke(cli, ["print_settings"])
    assert result.exit_code == 0
    print(grbl_cfg)
    print(result.output)
