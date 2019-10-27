import time
import uuid

import pytest

import grbl


@pytest.fixture(scope="session")
def session_uuid():
    yield uuid.uuid4()


@pytest.fixture(scope="module")
def module_uuid():
    yield uuid.uuid4()


@pytest.fixture(scope="class")
def class_uuid():
    yield uuid.uuid4()


@pytest.fixture(scope="function")
def function_uuid():
    yield uuid.uuid4()


def pytest_addoption(parser):
    parser.addoption(
        "--port", action="store", default="/dev/ttyUSB0", help="grbl serial port"
    )
    parser.addoption(
        "--baudrate", action="store", default="115200", help="grbl serial baudrate"
    )
    parser.addoption(
        "--ngc", action="store", default=None, help="file to run."
    )


@pytest.fixture(scope="session")
def cnc(request):
    grbl_cfg = {
        "port": request.config.getoption("--port"),
        "baudrate": request.config.getoption("--baudrate"),
    }
    cnc = grbl.Grbl(**grbl_cfg)
    time.sleep(2)
    cnc.reset()
    yield cnc
