from collections.abc import Iterable

def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x, ignore_types)
        else:
            yield x



if __name__ == '__main__':
    items = [1, 2, (3, 4, [5, 6], 7), 8]

    assert tuple(flatten(items)) == (1, 2, 3, 4, 5, 6, 7, 8)
