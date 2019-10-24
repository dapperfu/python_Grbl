import uuid
import Grbl
import time
import pytest

def test_grbl_reset(grbl):
    grbl.reset()

def test_grbl_status(grbl):
    assert len(grbl.cmd("$$"))==36

def test_grbl_status(grbl):
    print(f"{grbl.status}")
"""
# Inline, one test for all the settings/parameters.
def test_grbl_settings(grbl):
    for key, setting in GRBL.settings_key:
        print(f"{key}=${setting}={getattr(grbl, setting)}")

def test_grbl_gcode_parameters(grbl):
    for gcode_parameter in GRBL.gcode_parameters:
        print(f"{gcode_parameter}={getattr(grbl, gcode_parameter)}")
"""
# Paramaterized, generate a bunch of tests        
@pytest.mark.parametrize("key, setting", Grbl.settings_key)
def test_grbl_settings(grbl, key, setting):
    print(f"{setting} ({key}): {getattr(grbl, setting)}")
    time.sleep(0.1)


@pytest.mark.parametrize("gcode_parameter", Grbl.gcode_parameters)
def test_grbl_gcode_parameters2(grbl, gcode_parameter):
    print(f"{gcode_parameter}={getattr(grbl, gcode_parameter)}")
    time.sleep(0.1)
