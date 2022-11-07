from .command import *
from .util import *


__all__ = ['menu_cmd']


menu_cmd = CommandHandler('menu')

@menu_cmd.add_func
def list_worlds(self):
    """
    > list
    List avaliable worlds.
    """
    green('Listing worlds...')
