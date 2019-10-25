import time
import uuid

import pytest

import Grbl


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


@pytest.fixture(scope="session")
def grbl(request):
    grbl_cfg = {
        "port": request.config.getoption("--port"),
        "baudrate": request.config.getoption("--baudrate"),
    }
    grbl = Grbl.Grbl(**grbl_cfg)
    time.sleep(2)
    grbl.reset()
    yield grbl
