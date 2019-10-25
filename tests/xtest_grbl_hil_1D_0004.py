import time
import uuid

import pytest

import Grbl


def test_grbl_reset(grbl):
    grbl.reset()


@pytest.mark.parametrize("x_rate", [100])
def test_G0_X10(grbl, x_rate):
    print(grbl.status)
    grbl.run(
        f"""
G21
G91
G0X10F{x_rate}
"""
    )
    print(grbl.status)
