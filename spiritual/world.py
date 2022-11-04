from dataclasses import dataclass
from logging import getLogger

from .utility import *

__all__ = ['World']

logger = getLogger('WORLD')


@dataclass
class World:
    story_id: str | None = None

    @classmethod
    def loads(cls, obj: dict[str, any], /):
        pass

    def dumps(self, /):
        pass

    @safe_func
    def main(self, /):
        logger.info('debug enabled for <world>.')
        while True:
            a = input('> ')
            if a == 'exit':
                break
