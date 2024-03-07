"""
This module defines type definitions and functions for various purposes.
"""

__all__ = ["Guid", "makeguid"]

from typing import NewType
from uuid import uuid4

#: Defines a new-type for globally-unique identifiers.
Guid = NewType("Guid", str)


def makeguid() -> Guid:
    """
    Creates a new :py:class:`Guid`.

    :return: :py:class:`Guid` instance.

    >>> isinstance(makeguid(), str)  ## During static analysis, it is `Guid`.
    True
    """
    return Guid(uuid4().hex)
