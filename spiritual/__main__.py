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


def main():
    args = docopt(__doc__)
    debug = 'debugging ' if args['--debug'] else ''
    print(f'Hello World of {debug}Spiritual!')


if __name__ == '__main__':
    main()
