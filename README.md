# python_GRBL

#

Pythonic wrapper for GRBL control.

Tested on GRBL v1.1f

Hardware Tested:

- "CNC6030"
- "CNC3018"

*New* 2019! CNC6030 Support!

![](.img/cnc6030.jpg)

# Usage & Examples

Usage from git

    git clone https://github.com/dapperfu/python_Grbl.git
    make develop
    source virtual_env/bin/activate
    
In an existing virtual environment:

    pip install git+https://github.com/dapperfu/python_Grbl.git

## Save & Load settings.

Useful for migrating configs between machines/arduino devices.

- Dump GRBL machine settings to stdout.

    grblcli print_settings
    
- Save GRBL machine settings to a file.

    grblcli print_settings > machine.config
    
- Load GRBL machine settings from a file.

    grbl_cli load_settings machine.config
    
# Aim the laser.

Useful for aiming the laser.

```
grblcli aimlaser
```

Will prompt you to start and stop aiming the laser.

```
grblcli aimlaser
1
Press Enter to start aiming laser.
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4/4 [00:00<00:00,  9.42it/s]

Running...
Press Enter to stop aiming laser.
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2/2 [00:00<00:00,  9.40it/s]

Running...
```

# Run a g-code file.

Stream a G-code file to the GRBL device. 

    grblcli run drawing.ngc
    
## Bash Completion

https://click.palletsprojects.com/en/7.x/bashcomplete/

    eval "$(_GRBLCLI_COMPLETE=source `which grblcli`)"
  
