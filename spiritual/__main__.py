"""
Spiritual Python Prototype

Usage:
  spiritual [--debug]
  spiritual -h | --help

Options:
  --debug       Execute with debug logs.
  -h --help     Show this screen.
"""

from docopt import docopt
from logging import basicConfig as l_config

from .__init__ import menu


def main():
    args = docopt(__doc__)

    l_config(level = 0 if args['--debug'] else 50)

    menu()


if __name__ == '__main__':
    main()
