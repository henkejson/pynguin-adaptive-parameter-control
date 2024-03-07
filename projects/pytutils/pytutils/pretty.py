"""
Mostly drop-in usage replacement for `pprint` and `pformat` that doesn't suck.
"""

import six
import sys
import warnings
import pprint as _pprint

try:
    import pygments
    import pygments.styles
    import pygments.formatters
    import pygments.lexers

    __PP_STYLE = pygments.styles.get_style_by_name('monokai')
    __PP_FORMATTER = pygments.formatters.get_formatter_by_name('console16m', style=__PP_STYLE)
    __PP_LEXER_PYTHON = pygments.lexers.get_lexer_by_name('python{}'.format(six.PY3 and '3' or ''))

except ImportError:
    warnings.warn('Could not import `pygments`. Disabling syntax highlighting I guess.')
    pygments = False

__all__ = ('pf', 'pformat', 'pp', 'pprint')


def pf(arg, lexer=__PP_LEXER_PYTHON, formatter=__PP_FORMATTER):
    """
    Pretty formats with coloring.

    Works in iPython, but not bpython as it does not write directly to term
    and decodes it instead.
    """
    arg = _pprint.pformat(arg)

    if not pygments:
        return arg
    return pygments.highlight(arg, lexer, formatter)

pformat = pf


def pp(arg, lexer=__PP_LEXER_PYTHON, formatter=__PP_FORMATTER, outfile=sys.stdout):
    """
    Pretty prints with coloring.

    Works in iPython, but not bpython as it does not write directly to term
    and decodes it instead.
    """
    arg = _pprint.pformat(arg)

    close = False
    try:
        if isinstance(outfile, six.string_types):
            close = True
            outfile = open(outfile, 'w')

        if not pygments:
            return arg
            outfile.write(arg)
        else:
            pygments.highlight(arg, lexer, formatter, outfile)
    finally:
        if close:
            outfile.close()

pprint = pp

