from dataclasses import dataclass

__all__ = ['Player']


@dataclass
class Player:
    @classmethod
    def loads(cls, obj: dict[str, any], /):
        pass

    def dumps(self, /):
        pass
