from logging import getLogger

from .utility import *


__all__ = ['menu']

logger = getLogger('MENU')


@safe_func
def menu():
    logger.info('debug enabled for <menu>.')
    print(f'Hello World of Spiritual!')
    while True:
        a = input('> ')
        if a == 'exit':
            break
