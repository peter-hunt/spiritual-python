from logging import info as l_info
from types import FunctionType

__all__ = ['safe_func']


def safe_func(func: FunctionType) ->  FunctionType:
    def _func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            l_info('keyboard interrupt')

    _func.__name__ = func.__name__
    _func.__doc__ = func.__doc__
    return _func
