import os


def join_each(parent, iterable):
    for p in iterable:
        yield os.path.join(parent, p)

