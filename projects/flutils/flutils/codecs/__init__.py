import codecs
from locale import getpreferredencoding
from sys import getdefaultencoding
from typing import (
    Optional,
    cast,
)

from . import (
    b64,
    raw_utf8_escape,
)

__all__ = ['register_codecs', 'get_encoding', 'SYSTEM_ENCODING']


def register_codecs() -> None:
    """Register additional codecs.

    *New in version 0.4.*

    :rtype: :obj:`None`

    Examples:

        >>> from flutils.codecs import register_codecs
        >>> register_codecs()
        >>> 'test©'.encode('raw_utf8_escape')
        b'test\\\\xc2\\\\xa9'
        >>> b'test\\\\xc2\\\\xa9'.decode('raw_utf8_escape')
        'test©'
        >>> 'dGVzdA=='.encode('b64')
        b'test'
        >>> b'test'.decode('b64')
        'dGVzdA=='

    """
    raw_utf8_escape.register()
    b64.register()


SYSTEM_ENCODING: str = getpreferredencoding() or getdefaultencoding()
"""str: The default encoding as indicated by the system."""


def get_encoding(
        name: Optional[str] = None,
        default: Optional[str] = SYSTEM_ENCODING
) -> str:
    """Validate and return the given encoding codec name.

    Args:
        name (str): The name of the encoding to validate.
            if empty or invalid then the value of the given ``default``
            will be returned.
        default (str, optional): If set, this encoding name will be returned
            if the given ``name`` is invalid. Defaults to:
            :obj:`~flutils.codecs.SYSTEM_ENCODING`.  If set to :obj:`None`
            which will raise a :obj:`LookupError` if the given ``name``
            is not valid.

    Raises:
        LookupError: If the given ``name`` is not a valid encoding codec name
            and the given ``default`` is set to :obj:`None` or an empty string.
        LookupError: If the given ``default`` is not a valid encoding codec
            name.

    Returns:
        str: The encoding codec name.

    Example:

        >>> from flutils.codecs import get_encoding
        >>> get_encoding()
        'utf-8'
    """
    if name is None:
        name = ''
    if hasattr(name, 'encode') is False:
        name = ''
    name = cast(str, name)
    name = name.strip()

    if default is None:
        default = ''
    if hasattr(default, 'encode') is False:
        default = ''
    default = cast(str, default)
    default = default.strip()

    if default:
        try:
            codec = codecs.lookup(default)
        except LookupError:
            raise LookupError(
                f"The given 'default' of {default!r} is an invalid encoding "
                f"codec name."
            )
        else:
            default = codec.name

    try:
        codec = codecs.lookup(name)
    except LookupError:
        if default:
            return default
        raise LookupError(
            f"The given 'name' of {name!r} is an invalid encoding "
            f"codec name."
        )
    else:
        return codec.name
