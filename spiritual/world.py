from dataclasses import *
from pathlib import *
from types import *
from typing import *

from .command import *
from .myjson import *
from .player import *
from .util import *

__all__ = ['World']


@dataclass
class World:
    world_name: str = ''
    story_id: str | None = None
    players: list[Player] = field(default_factory=list)

    @classmethod
    def is_valid(cls, obj, /) -> bool:
        anno = cls.__annotations__
        for name, anno_type in anno.items():
            if name not in obj:
                return False
            value = obj[name]
            if isinstance(anno_type, GenericAlias):
                if not isinstance(value, anno_type.__origin__):
                    return False
                if anno_type.__origin__ in {tuple, list}:
                    if len(anno_type.__args__) != 1:
                        continue
                    subtype = anno_type.__args__[0]
                    if not hasattr(subtype, 'is_valid'):
                        continue
                    for item in value:
                        if not isinstance(item, subtype):
                            return False
                        if not subtype.is_valid(item):
                            return False
                    else:
                        continue
                elif anno_type.__origin__ == dict:
                    if len(anno_type.__args__) != 2:
                        continue
                    subtype = anno_type.__args__[1]
                    if not hasattr(subtype, 'is_valid'):
                        continue
                    for item in value.values():
                        if not isinstance(item, subtype):
                            return False
                        if not subtype.is_valid(item):
                            return False
                    else:
                        continue
            elif name in anno and not isinstance(value, anno_type):
                return False
        return True

    @classmethod
    def loads(cls, obj: dict[str, any], /) -> Self | None:
        result = cls()
        anno = cls.__annotations__
        for name, value in obj.items():
            if name not in anno:
                continue
            anno_type = (anno[name].__origin__ if isinstance(anno[name], GenericAlias)
                         else anno[name])
            if isinstance(value, anno_type):
                setattr(result, name, value)
        if result.world_name == '':
            red('Cannot load a world without valid world name.')
            return
        return result

    def dumps(self, /) -> dict[str, any]:
        result = {}
        anno = type(self).__annotations__
        for name in anno.keys():
            result[name] = getattr(self, name)
            if hasattr(result[name], 'dumps'):
                result[name] = result[name].dumps()
        return result

    def save(self, /) -> NoReturn:
        obj = self.dumps()
        with open(Path('.', 'data', 'saves', f'{self.world_name}.json'), 'w') as file:
            dump(obj, file)

    @classmethod
    def new(cls, /) -> Self:
        return cls()

    @safe_func
    def main(self, /) -> NoReturn:
        world_cmd.run(self, prompt='>> ')


world_cmd = CommandHandler('world')
