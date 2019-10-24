from IPython.core.magic import cell_magic
from IPython.core.magic import register_cell_magic
from IPython.core.magic import register_line_cell_magic


@register_cell_magic
def grbl_cell_magic(cfg, cell):
    "# Sending G-Code"
    grbl.run(cell)
