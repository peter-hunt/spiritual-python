__all__ = ['TYPED_ARGS']

TYPED_ARGS = {
    r'item(\-\d+)?': (r'\d+', int),
    r'integer(\-\d+)?': (r'\d+', int),
    r'number(\-\d+)?': (r'(\d+(\.(\d+)?)?)|(\.\d+)', float),
    r'(name)|(id)(\-\d+)?': (r'\w+', lambda value: value),
}
