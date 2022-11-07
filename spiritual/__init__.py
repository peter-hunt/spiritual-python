
from sys import version_info

if version_info < (3, 11):
    raise ValueError('at least python 3.11 is required to run this project')


from .game import *
from .game import __all__ as __game_all__
from .player import *
from .player import __all__ as __player_all__
from .world import *
from .world import __all__ as __world_all__


__all__ = __game_all__ + __player_all__ + __world_all__
