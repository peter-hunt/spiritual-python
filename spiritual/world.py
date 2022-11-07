from dataclasses import *
from typing import *

from .command import *
from .player import *
from .util import *

__all__ = ['World']


@dataclass
class World:
    world_name: str = ''
    world_id: str = ''
    story_id: str | None = None
    players: list[Player] = field(default_factory=list)

    @classmethod
    def is_valid(cls, obj, /) -> bool:
        anno = cls.__annotations__
        for name, value in obj.items():
            if name in anno and not isinstance(value, anno[name]):
                return False
        return True

    @classmethod
    def loads(cls, obj: dict[str, any], /) -> Self | None:
        result = cls()
        anno = cls.__annotations__
        for name, value in obj.items():
            if name in anno and isinstance(value, anno[name]):
                setattr(result, name, value)
        if result.world_name == '' or result.world_id == '':
            red('Cannot load a world without valid world name or ID.')
            return
        return result

    def dumps(self, /) -> dict[str, any]:
        result = {}
        anno = type(self).__annotations__
        for name in anno.items():
            result[name] = getattr(self, name)
            if hasattr(result[name], 'dumps'):
                result[name] = result[name].dumps()
        return result

    @classmethod
    def new(cls, /) -> Self:
        return cls()

    @safe_func
    def main(self, /) -> NoReturn:
        world_cmd.run(self)


world_cmd = CommandHandler('world')
