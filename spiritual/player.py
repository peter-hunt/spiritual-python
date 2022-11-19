from dataclasses import *
from types import *
from typing import *

__all__ = ['Player']


@dataclass
class Player:
    items: list = field(default_factory=list)

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
    def loads(cls, obj: dict[str, any], /) -> Self:
        result = cls()
        anno = cls.__annotations__
        for name, value in obj.items():
            if name in anno and isinstance(value, anno[name]):
                setattr(result, name, value)
        return result

    def dumps(self, /) -> dict[str, any]:
        result = {}
        anno = type(self).__annotations__
        for name in anno.items():
            result[name] = getattr(self, name)
            if hasattr(result[name], 'dumps'):
                result[name] = result[name].dumps()
        return result
