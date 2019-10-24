"""Grbl: Python Grbl Serial Wraper Thing."""
from .Grbl import gcode_parameters
from .Grbl import Grbl
from .Grbl import settings_key

# from .magics import grbl_cell_magic


# def load_ipython_extension(ipython):
#    ipython.register_magics(grbl_cell_magic)


__all__ = [
    "Grbl",
    "settings_key",
    "gcode_parameters",
    #    "grbl_cell_magic",
    #    "load_ipython_extension",
]
