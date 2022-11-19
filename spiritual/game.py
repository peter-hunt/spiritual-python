from pathlib import *

from .command import *
from .myjson import load
from .util import *
from .world import *


__all__ = ['menu_cmd']


menu_cmd = CommandHandler('menu')


@menu_cmd.add_func
def list_worlds(self):
    """
    > list
    List avaliable worlds.
    """
    green('Listing worlds...')
    for filename in [*Path('.', 'data', 'saves').walk()][0][2]:
        gamename = filename[:-5]
        if not filename.endswith('.json'):
            continue

        try:
            with open(Path('.', 'data', 'saves', filename)) as file:
                obj = load(file)
        except:
            yellow(f'{gamename} (invalid JSON file)')
            continue

        if not World.is_valid(obj):
            yellow(f'{gamename} (invalid world file)')
        else:
            green(f'{gamename}')


@menu_cmd.add_func
def new_world(self):
    """
    > new
    Create a new world.
    """
    green('Please enter the name of the world:')
    name = input_regex(']> ', r'\w+')
    World(name).save()


@menu_cmd.add_func
def open_world(self, name):
    """
    > open <name>
    Run a world.
    """
    filename = name + '.json'

    if not Path('.', 'data', 'saves', filename).is_file():
        yellow('Cannot load world: file not found')
        return

    try:
        with open(Path('.', 'data', 'saves', filename)) as file:
            obj = load(file)
    except:
        yellow('Cannot load world: invalid JSON file')
        return

    if not World.is_valid(obj):
        yellow('Cannot load world: invalid world file')
        return
    else:
        World.loads(obj).main()
