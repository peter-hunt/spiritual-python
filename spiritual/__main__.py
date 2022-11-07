"""
Spiritual Python Prototype

Usage:
  spiritual [--debug]
  spiritual -h | --help

Options:
  --debug       Execute with debug logs.
  -h --help     Show this screen.
"""

from sys import version_info

if version_info < (3, 11):
    raise ValueError('at least python 3.11 is required to run this project')


from docopt import docopt
from logging import basicConfig as l_config

__all__ = ['spiritual_main']


def spiritual_main():
    args = docopt(__doc__)

    l_config(level = 0 if args['--debug'] else 50)


    from .__init__ import menu_cmd
    from .util import green

    green('Welcome to the Spiritual Universe!')
    menu_cmd.run()


if __name__ == '__main__':
    spiritual_main()
