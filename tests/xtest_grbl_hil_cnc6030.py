import time
import uuid

import pytest

import Grbl


def test_grbl_reset(grbl):
    grbl.reset()


@pytest.mark.parametrize("x_rate", [100])
def test_G0X10(grbl, x_rate):
    print(grbl.status)
    grbl.run(
        f"""
G21
G91
G0X10F{x_rate}
"""
    )
    print(grbl.status)


@pytest.mark.parametrize("rate", [100])
def test_G0X10Y10(grbl, rate):
    print(grbl.status)
    grbl.run(
        f"""
G21
G91
G0X10Y10F{rate}
"""
    )
    print(grbl.status)


@pytest.mark.parametrize("laser_power", [1])
def test_laser(grbl, laser_power):
    print(grbl.status)
    grbl.run(
        f"""
G21
G91
G1F100
M3S{laser_power}
"""
    )
    time.sleep(5)
    grbl.run(
        f"""
M5
G0
"""
    )
    print(grbl.status)


@pytest.mark.parametrize("laser_power", [1])
def test_laser_square(grbl, laser_power):
    print(grbl.status)
    grbl.run(
        f"""
G21
G91
G1F100
M3S{laser_power}
G1X0Y0
G1X10Y0
G1X10Y10
G1X0Y10
G1X0Y0
M5
G0
"""
    )
    print(grbl.status)
