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

@pytest.fixture(scope="session")
def cnc(request):
    grbl_cfg = {
        "port": request.config.getoption("--port"),
        "baudrate": request.config.getoption("--baudrate"),
    }
    cnc = grbl.Grbl(**grbl_cfg)
    time.sleep(2)
    cnc.reset()
    cnc.home()
    cnc.cmd("G91")
    cnc.cmd("G21")
    yield cnc
