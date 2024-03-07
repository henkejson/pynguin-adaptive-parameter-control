"""
Utilities to work with files.
"""

import os
import sys
import functools

LINEMODE = 0


def islurp(filename, mode='r', iter_by=LINEMODE, allow_stdin=True, expanduser=True, expandvars=True):
    """
    Read [expanded] `filename` and yield each (line | chunk).

    :param str filename: File path
    :param str mode: Use this mode to open `filename`, ala `r` for text (default), `rb` for binary, etc.
    :param int iter_by: Iterate by this many bytes at a time. Default is by line.
    :param bool allow_stdin: If Truthy and filename is `-`, read from `sys.stdin`.
    :param bool expanduser: If Truthy, expand `~` in `filename`
    :param bool expandvars: If Truthy, expand env vars in `filename`
    """
    if iter_by == 'LINEMODE':
        iter_by = LINEMODE

    fh = None
    try:
        if filename == '-' and allow_stdin:
            fh = sys.stdin
        else:
            if expanduser:
                filename = os.path.expanduser(filename)
            if expandvars:
                filename = os.path.expandvars(filename)

            fh = open(filename, mode)
            fh_next = fh.readline if iter_by == LINEMODE else functools.partial(fh.read, iter_by)

        while True:
            buf = fh_next()
            if buf == '':  # EOF
                break
            yield buf
    finally:
        if fh and fh != sys.stdin:
            fh.close()

# convenience
islurp.LINEMODE = LINEMODE

# alias
slurp = islurp


def burp(filename, contents, mode='w', allow_stdout=True, expanduser=True, expandvars=True):
    """
    Write `contents` to `filename`.
    """
    if filename == '-' and allow_stdout:
        sys.stdout.write(contents)
    else:
        if expanduser:
            filename = os.path.expanduser(filename)
        if expandvars:
            filename = os.path.expandvars(filename)

        with open(filename, mode) as fh:
            fh.write(contents)
