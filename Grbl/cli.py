"""Naval Fate.

Usage:
  grbl.py aimlaser [--port=<port>]
  grbl.py (-h | --help)
  grbl.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --port=<port>  Speed in knots [default: /dev/ttyUSB0].

"""
from docopt import docopt


def cli():
    arguments = docopt(__doc__, version="Naval Fate 2.0")
    print(arguments)


if __name__ == "__main__":
    arguments = docopt(__doc__, version="Naval Fate 2.0")
    print(arguments)
