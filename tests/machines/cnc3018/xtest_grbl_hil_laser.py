import time
import uuid

import Grbl
import pytest


def test_grbl_reset(grbl):
    grbl.reset()


@pytest.mark.parametrize("laser_power", [100])
def laser_mark(grbl, laser_power):
    print(grbl.status)
    grbl.run(
        f"""
G21
G91
G1X0Y0F100
M3S{laser_power}
G0X0Y0F100
G0X10Y0F100
G1X0Y0F100
M3S{laser_power}
G0X0Y0F100
M5
"""
    )
    print(grbl.status)
