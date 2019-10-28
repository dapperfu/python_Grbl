import datetime
import time
import warnings

import numpy as np
import serial
from tqdm import tqdm

run_states = ["Idle", "Run", "Hold", "Door", "Home", "Alarm", "Check"]


class Grbl:
    """Class for a Grbl controlled CNC.

    Tested on Grbl v1.1f, v1.1g, & v1.1h.
    """

    def __init__(self, port: str, baudrate: int = 115200):
        """
        port <str>
        """
        self.serial = serial.Serial()
        self.serial.port = port
        self.serial.baudrate=baudrate
        self.serial.timeout=0.10
        self.serial.setDTR(False)
        self.serial.open()
        self.cmd("$10=2")

    def __del__(self):
        pass

    def __repr__(self):
        return f"Grbl<{self.serial.port}>"

    def write(self, command_line: str = ""):
        bytes_written = [0, 0]
        bytes_written[0] = self.serial.write("\n".encode())
        bytes_written[1] = self.serial.write(f"{command_line}\n".encode())
        return bytes_written

    def read(self, multiline=True, timeout=-1):
        """
        Read multiple responses from Grbl.

        multiline [true]: Read multiple lines.
        timeout [-1]: Specify alternative timeout.
        """
        if timeout is not -1:
            old_timeout = self.serial.timeout
            self.serial.timeout = timeout
        if multiline:
            responses = self.serial.readlines()
            responses = [response.decode().strip() for response in responses]
            return responses
        else:
            responses = self.serial.readline().decode().strip()
        if timeout is not -1:
            self.serial.timeout = old_timeout
        return responses

    def cmd(self, command_line, resp=True, multiline=True):
        """cmd: Send a command to Grbl and return its response.
        command_line: command to send to grbl
        resp [True]: return a response.
        multiline [True]: return a multiple line response.
        """

        # Flush serial input.
        self.serial.flushInput()
        # Write the command.
        self.write(command_line)
        # If waiting on a response.
        if resp:
            # Return the response.
            return self.read(multiline=multiline)
        # Otherwise none.
        return None

    def reset(self, attempts=40):
        """ https://github.com/gnea/grbl/wiki/Grbl-v1.1-Commands#grbl-v11-realtime-commands
        """
        for t in range(attempts):
            ret = self.cmd("\x18")
            if len(ret) > 0:
                return (t, ret)
                break
            time.sleep(0.25)
        return None

    def sleep(self):
        """ https://github.com/gnea/grbl/wiki/Grbl-v1.1-Commands#slp---enable-sleep-mode
        """
        ret = self.cmd("$SLP")
        assert ret[-1] == "ok"

    @property
    def status(self):
        """Return the status of Grbl.
        """
        ret = self.cmd("?")
        while len(ret) == 0:
            time.sleep(0.25)
            ret = self.cmd("?")

        for r in ret:
            if r == "ok":
                continue
            return r
        return None

    def kill_alarm(self):
        """ https://github.com/gnea/grbl/wiki/Grbl-v1.1-Commands#x---kill-alarm-lock
        """
        ret = self.cmd("$X")
        assert ret[-1] == "ok"

    def home(self):
        """ https://github.com/gnea/grbl/wiki/Grbl-v1.1-Commands#h---run-homing-cycle
        """
        self.write("$H")
        for t in range(10):
            ret = self.cmd("")
            if len(ret) == 2:
                assert ret[0] == "ok"
                assert ret[1] == "ok"
                return t
                break
            time.sleep(1)
        return None

    def run(self, program):
        """" run: Run a Grbl 'program'.

        A 'program' can be:
        - Plain text GCode file.
        - GCode commands in a list.
        - Python GCode object.
        - Any class with a 'buffer' property where 'buffer' is a list of GCode commands.

        """
        if isinstance(program, list):
            pass
        elif isinstance(program, str):
            program = program.splitlines()
        elif hasattr(program, "buffer"):
            program = program.buffer
        else:
            raise Exception(f"Unknown Program {type(program)}\n{program}")

        # Strip whitespace and force letters to capital.
        program = [line.strip().upper() for line in program]
        # Strip out all whitespace
        program = [line.replace(" ", "") for line in program]

        t1 = time.time()
        self.serial.flushInput()

        # Create list to store the number of bytes we think are in memory.
        buffer_bytes = list()

        try:
            # For each line in the program"
            for program_line in tqdm(program):
                bytes_written = self.write(program_line)
                buffer_bytes.extend(bytes_written)
                results = self.read(multiline=True, timeout=0.1)
                # While we wait on grbl to respond with an ok.
                while len(results) == 0:
                    # Wait
                    time.sleep(0.25)
                    # Try again
                    results = self.read(multiline=True, timeout=0.1)
            time.sleep(0.5)
            # While the command is running:
            while "Run" in self.status:
                print(".", end="")
                time.sleep(0.25)
        except KeyboardInterrupt:
            # Halt the machine on a keyboard interrupt.
            self.cmd("!")
            print("^C")

        return time.time() - t1

    @property
    def cordinates_absolute(self):
        return "G90" in parser_state

    @cordinates_absolute.setter
    def cordinates_absolute(self, mode: bool):
        if mode:
            self.cmd("G90")
        else:
            self.cmd("G91")
        assert self.cordinates_absolute

    @property
    def coordinates_relative(self):
        return "G91" in parser_state

    @coordinates_relative.setter
    def coordinates_relative(self, mode: bool):
        if mode:
            self.cmd("G91")
        else:
            self.cmd("G90")

    @property
    def inch(self):
        inch_mode = "G20" in states
        if inch_mode:
            warnings.warn(
                DeprecationWarning(
                    f"Inches are deprecated. It is {datetime.datetime.now().year}"
                )
            )
        return inch_mode

    @inch.setter
    def inch(self, mode: bool):
        if mode:
            warnings.warn(
                DeprecationWarning(
                    f"Inches are deprecated. It is {datetime.datetime.now().year}"
                )
            )
            self.cmd("G20")
        else:
            self.cmd("G21")

    @property
    def mm(self):
        return "G21" in states

    @mm.setter
    def mm(self, mode: bool):
        if mode:
            self.cmd("G21")
        else:
            warnings.warn(
                DeprecationWarning(
                    f"Inches are deprecated. It is {datetime.datetime.now().year}"
                )
            )
            self.cmd("G20")

    def aim_laser(self, laser_power: int = 1):
        """Run laser at specified power to aim laser.
        *** Warning. Will turn on laser. ***
        *** Warning. Do not look at laser with remaining eye. ***

        laser_power [int:1]: laser power to use. [0, 255]
        """
        input("Press Enter to start aiming laser.")
        self.run(
            """
G0
M3S1
G1F1
"""
        )
        input("Press Enter to stop aiming laser.")
        self.run(
            """
M5
"""
        )

    @property
    def probe_success(self):
        prb_line = [line for line in self.cmd("$#") if "PRB" in line]
        assert len(prb_line) == 1
        _, _, success = prb_line[0].strip("[]").split(":")
        if success == "0":
            return False
        elif success == "1":
            return True
        raise Exception(success)


# https://github.com/gnea/grbl/wiki/Grbl-v1.1-Configuration#---view-grbl-settings
# $$ - View Grbl settings

"""
# The x of $x=val indicates a particular setting, while val is the
setting value. In prior versions of Grbl, each setting had a description
next to it in () parentheses, but Grbl v1.1+ no longer includes them
unfortunately.
"""

# Map the setting to human readable names values.
settings_key = [
    ("$0", "step_pulse"),
    ("$1", "step_idle_delay"),
    ("$2", "step_port_invert"),
    ("$3", "direction_port_invert"),
    ("$4", "step_enable_invert"),
    ("$5", "limit_pin_invert"),
    ("$6", "probe_pin_invert"),
    ("$10", "status_report"),
    ("$11", "junction_deviation"),
    ("$12", "arc_tolerance"),
    ("$13", "report_inches"),
    ("$20", "soft_limits"),
    ("$21", "hard_limits"),
    ("$22", "homing_cycle"),
    ("$23", "homing_dir_invert"),
    ("$24", "homing_feed"),
    ("$25", "homing_seek"),
    ("$26", "homing_debounce"),
    ("$27", "homing_pull_off"),
    ("$30", "max_spindle_speed"),
    ("$31", "min_spindle_speed"),
    ("$32", "laser_mode"),
    ("$100", "x_steps_mm"),
    ("$101", "y_steps_mm"),
    ("$102", "z_steps_mm"),
    ("$110", "x_max_rate"),
    ("$111", "y_max_rate"),
    ("$112", "z_max_rate"),
    ("$120", "x_acceleration"),
    ("$121", "y_acceleration"),
    ("$122", "z_acceleration"),
    ("$130", "x_travel"),
    ("$131", "y_travel"),
    ("$132", "z_travel"),
]

settings_key_dict = dict()
for key, value in settings_key:
    settings_key_dict[key] = value

# Generate a getter to look for


def grbl_getter_generator(grbl_key):
    # Function prototype
    def grbl_getter(self):
        # Get the config by sending $$
        config = self.cmd("$$", resp=True, multiline=True)
        # For each line in the config response.
        for config_line in config:
            # If the line starts with $
            if config_line.startswith("$"):
                # split by key
                key, value = config_line.split("=")
                # Compare loop key to grbl_getter_generator's namespace's grbl_key
                if key == grbl_key:
                    # Return the float (all settings are floats).
                    return float(value)
        return None

    # Return the function.
    return grbl_getter


# Generator/Factory for a setter
def grbl_setter_generator(cmd):
    def grbl_setter(self, value):
        set_cmd = f"{cmd}={value}"
        ret = self.cmd(set_cmd, resp=True, multiline=False)
        print(ret)

    return grbl_setter


# For each
for grbl_key, human_readable in settings_key:
    # Generate setters and getters from the Grbl
    setter = grbl_setter_generator(grbl_key)
    getter = grbl_getter_generator(grbl_key)
    # Generate documentation.
    doc = " ".join(human_readable.split("_"))
    # Create a property with the function setter, getter and documentation.
    fcn_prop = property(fget=getter, fset=setter, doc=doc)
    # Add the property to Grbl class.
    setattr(Grbl, human_readable, fcn_prop)

# GCode parameters:
# https://github.com/gnea/grbl/wiki/Grbl-v1.1-Commands#---view-gcode-parameters
# List of each of the the supported gcode parameters.
gcode_parameters = [
    "G54",
    "G55",
    "G56",
    "G57",
    "G58",
    "G59",
    "G28",
    "G30",
    "G92",
    "TLO",
    #    "PRB",
]

# Getter to make a function
def gcode_param_gen(parameter):
    def gcode_param(self):
        # Send the Grbl command to get the gcode_parameters:
        gcode_parameters = self.cmd("$#")  # View gcode parameters
        # Loop through each of the returned parameters
        for gcode_parameter in gcode_parameters:
            # If the parameter matches the return line
            if parameter in gcode_parameter:
                # Split the response line by the colon,
                try:
                    _, value = gcode_parameter.split(":")
                except:
                    try:
                        _, value, self.probe_success = gcode_parameter.split(":")
                    except:
                        print(f"{gcode_parameter}")
                        print(gcode_parameters)
                        raise Exception(f"{gcode_parameter}")
                # String lineup.
                value = value.strip("]")
                # Split the return line
                values = value.split(",")
                # Convert string values to floats.
                values = [float(value) for value in values]
                # Return
                return values
        # Not Found.
        return None

    return gcode_param


for parameter in gcode_parameters:
    fcn = gcode_param_gen(parameter)
    prop = property(fget=fcn)
    setattr(Grbl, parameter, prop)
