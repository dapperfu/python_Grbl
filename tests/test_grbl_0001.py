import time
import uuid

import pytest


def test_grbl_reset(cnc):
    cnc.reset()


def test_grbl_status(cnc):
    print(cnc.status)
