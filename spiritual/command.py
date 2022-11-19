from itertools import dropwhile, takewhile
from logging import getLogger
from re import fullmatch
from types import *
from typing import *

from .constants import *
from .util import *

__all__ = ['CommandFunction', 'CommandHandler']


class CommandFunction:
    def __init__(self, func: FunctionType, /):
        self.doc = '\n'.join(line.strip() for line in func.__doc__.strip().split('\n'))
        self.usages = [line[2:] for line in self.doc.split('\n')
                       if line.startswith('> ')]
        self.keyword = ' '.join(word for word in self.usages[0].split() if word[0] not in {'<', '['})
        for usage in self.usages[1:]:
            keyword = ' '.join(word for word in usage.split() if word[0] not in {'<', '['})
            if self.keyword != keyword:
                raise ValueError(f'please put commands with different keywords into'
                                 f' different functions: {keyword!r}')

        for usage in self.usages:
            level = 0
            for word in usage.split():
                if word.startswith('<'):
                    if level > 1:
                        raise ValueError('Cannot have positional arg after optional arg: {usage!r}')
                    level = 1
                elif word.startswith('[--'):
                    level = 3
                elif word.startswith('['):
                    if level > 2:
                        raise ValueError('Cannot have optional arg after optional flag: {usage!r}')
                    level = 2
                else:
                    if level > 0:
                        raise ValueError('Cannot have command word after arg: {usage!r}')
        self.func = func
        self._cached_usage = -1

    def match(self, text: str, /) -> tuple[bool, dict[str, any] | None]:
        if not text.startswith(self.keyword):
            return (False, None)
        keyword_len = len(self.keyword.split())

        input_words = text.split()
        for usage in self.usages:
            usage_words = usage.split()
            min_usage = len([item for item in usage_words
                             if not item.startswith('[')])
            if not min_usage <= len(input_words) <= len(usage_words):
                continue

            args = {}
            num_text = keyword_len
            preflag_usages = takewhile(lambda word: not word.startswith('[--'), usage_words[keyword_len:])
            flag_usages = dropwhile(lambda word: not word.startswith('[--'), usage_words[keyword_len:])
            flag_usages = [flag.strip('[]') for flag in flag_usages]
            for flag in flag_usages:
                args[flag] = False

            for word in preflag_usages:
                if word[0] not in {'<', '['}:
                    if word == input_words[num_text]:
                        continue
                    else:
                        break
                clean_word = word.strip('<>[]')
                if clean_word in TYPED_ARGS:
                    pattern, processor = TYPED_ARGS[clean_word]
                    if not fullmatch(pattern, input_words[num_text]):
                        if word[0] == '[':
                            continue
                        return (False, None)
                else:
                    processor = lambda value: value

                args[clean_word] = processor(input_words[num_text])
                num_text += 1

            for word in input_words[num_text:]:
                for flag in flag_usages:
                    if word == flag:
                        args[flag[2:]] = True
                        break
                else:
                    return (False, None)

            return (True, args)

        return (False, None)

    def call(self, clsself: any, args: dict[str, any], /) -> any:
        self.func(clsself, **args)

    def __eq__(self, value: any, /) -> bool:
        if isinstance(value, Self):
            return self.name == value.name
        elif isinstance(value, str):
            return self.name == value
        else:
            return False


class CommandHandler:
    def __init__(self, name: str, /):
        self.name = name
        self.update = lambda: None
        self.funcs = []
        self.logger = getLogger(self.name)

        @self.add_func
        def exit_loop(self, /):
            """
            > exit
            Exit the current scope.
            """
            pass

    def add_update_func(self, func: FunctionType, /):
        self.update = func

    def add_func(self, func: FunctionType, /):
        self.funcs.append(CommandFunction(func))

    @safe_func
    def run(self, clsself: any = None, /, prompt: str = '> '):
        self.logger.info(f'debug enabled for <{self.name}>.')
        while True:
            user_input = ' '.join(input(prompt).strip().split())
            if user_input == 'help':
                gray('\n\n'.join(func.doc for func in self.funcs))
                continue
            elif user_input.startswith('help '):
                keyword = user_input[5:]
                gray('\n\n'.join(
                    func.doc for func in self.funcs
                    if func.keyword.startswith(keyword)
                ))
            elif user_input == 'exit':
                break

            for func in self.funcs:
                does_match, args = func.match(user_input)
                if does_match:
                    func.call(clsself, args)
                    break
            else:
                red('Unknown command. Use `help` for command usages.')