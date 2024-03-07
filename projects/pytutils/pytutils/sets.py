try:
    from collections.abc import MutableSet
except ImportError:
    from collections import MutableSet

import collections
import copy
import random
import time

import attr

from .iters import consume


@attr.s
class MetaSet(MutableSet):
    """
    Set that tracks the time a value was added.
    """

    _meta_func = attr.ib(default=lambda value, **kwargs: random.randint(0, 1))  # type: callable

    _store = attr.ib(factory=set)  # type: MutableSet
    _meta = attr.ib(factory=dict)  # type: collections.MutableMapping

    _initial = attr.ib(default=None)  # type: collections.Iterable

    def __attrs_post_init__(self):
        if self._initial:
            self.update(self._initial)
            delattr(self, '_initial')

    def __contains__(self, item):
        return item in self._store

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def add(self, value):
        self._meta[value] = self._meta_func(value, self=self)
        self._store.add(value)

    def discard(self, value):
        self._meta.pop(value, None)
        self._store.discard(value)

    def update(self, iterable):
        """Add all values from an iterable (such as a list or file)."""
        # Must comsume generator fully on py3k
        consume(map(self.add, iterable))

    def _asdict(self):
        return copy.copy(self._meta)


@attr.s
class TimedValueSet(MetaSet):
    _meta_func = attr.ib(default=lambda value, **kwargs: time.time())

    @property
    def added_at(self):
        return self._meta
