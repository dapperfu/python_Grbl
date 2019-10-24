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


@pytest.fixture(scope="session")
def grbl():
    grbl = Grbl.Grbl(port="/dev/ttyUSB0", baudrate=115200)
    time.sleep(2)
    yield grbl
    if not grbl.serial.closed:
        grbl.serial.close()
