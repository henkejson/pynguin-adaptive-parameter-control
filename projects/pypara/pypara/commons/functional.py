__all__ = ["identity"]

from typing import Iterable, List, TypeVar

#: A named, generic type variable.
_T = TypeVar("_T")


def identity(x: _T) -> _T:
    """
    Provides the identity function.

    :param x: Any value of the generic type.
    :return: The value consumed.

    >>> identity(1)
    1
    """
    return x


def chunk(lst: List[_T], n: int) -> Iterable[List[_T]]:
    """
    Splits given list in chunks of given size and returns them in an iterable.

    :param lst: List of items.
    :param n: Chunks size.
    :return: Iterable of item lists.

    >>> list(chunk([], 1))
    []
    >>> list(chunk([], 2))
    []
    >>> list(chunk([1, 2, 3, 4], 1))
    [[1], [2], [3], [4]]
    >>> list(chunk([1, 2, 3, 4], 2))
    [[1, 2], [3, 4]]
    >>> list(chunk([1, 2, 3, 4, 5], 2))
    [[1, 2], [3, 4], [5]]
    """
    for x in range(0, len(lst), n):
        yield lst[x : x + n]  # noqa: E203
