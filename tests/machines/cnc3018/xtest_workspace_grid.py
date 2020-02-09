import time
import uuid

import pytest


def test_grbl_reset(grbl):
    grbl.reset()


@pytest.mark.parametrize("laser_power", [100])
def test_laser_mark(cnc, laser_power):
    grbl=cnc
    print(grbl.status)
    grbl.run(
        f"""
G21
G91
G1X0Y0F200
M3S{laser_power}
G0X0Y0F200
G0X50Y0F200
G1X0Y0F200
M3S{laser_power}
G0X0Y0F200
M5
"""
    )
    print(grbl.status)
