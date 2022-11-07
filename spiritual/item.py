from dataclasses import *
from typing import *


@dataclass
class Item:
    item_id: str = ''
    amount: int = 1

    @classmethod
    def is_valid(cls, obj, /) -> bool:
        anno = cls.__annotations__
        for name, value in obj.items():
            if name in anno and not isinstance(value, anno[name]):
                return False
        return True

    @classmethod
    def loads(cls, obj: dict[str, any], /) -> Self:
        result = cls()
        anno = cls.__annotations__
        for name, value in obj.items():
            if name in anno and isinstance(value, anno[name]):
                setattr(result, name, value)
        if result.world_name == '' or result.world_id == '':
            print('')
        return result

    def dumps(self, /) -> dict[str, any]:
        result = {}
        anno = type(self).__annotations__
        for name in anno.items():
            result[name] = getattr(self, name)
            if hasattr(result[name], 'dumps'):
                result[name] = result[name].dumps()
        return result
