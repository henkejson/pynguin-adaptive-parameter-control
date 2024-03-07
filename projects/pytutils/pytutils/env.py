import collections
import os
import re
import typing


def expand(val: str) -> str:
    val = os.path.expandvars(val)
    val = os.path.expanduser(val)
    return val


def parse_env_file_contents(lines: typing.Iterable[str] = None) -> typing.Generator[typing.Tuple[str, str], None, None]:
    """
    Parses env file content.

    From honcho.

    >>> lines = ['TEST=${HOME}/yeee', 'THISIS=~/a/test', 'YOLO=~/swaggins/$NONEXISTENT_VAR_THAT_DOES_NOT_EXIST']
    >>> load_env_file(lines, write_environ=dict())
    OrderedDict([('TEST', '.../yeee'),
             ('THISIS', '.../a/test'),
             ('YOLO',
              '.../swaggins/$NONEXISTENT_VAR_THAT_DOES_NOT_EXIST')])

    """
    for line in lines:
        m1 = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)

        if m1:
            key, val = m1.group(1), m1.group(2)

            m2 = re.match(r"\A'(.*)'\Z", val)
            if m2:
                val = m2.group(1)

            m3 = re.match(r'\A"(.*)"\Z', val)
            if m3:
                val = re.sub(r'\\(.)', r'\1', m3.group(1))

            yield key, val


def load_env_file(lines: typing.Iterable[str], write_environ: typing.MutableMapping = os.environ) -> collections.OrderedDict:
    """
    Loads (and returns) an env file specified by `filename` into the mapping `environ`.

    >>> lines = ['TEST=${HOME}/yeee-$PATH', 'THISIS=~/a/test', 'YOLO=~/swaggins/$NONEXISTENT_VAR_THAT_DOES_NOT_EXIST']
    >>> load_env_file(lines, write_environ=dict())
    OrderedDict([('TEST', '.../.../yeee-...:...'),
             ('THISIS', '.../a/test'),
             ('YOLO',
              '.../swaggins/$NONEXISTENT_VAR_THAT_DOES_NOT_EXIST')])
    """
    values = parse_env_file_contents(lines)

    changes = collections.OrderedDict()

    for k, v in values:
        v = expand(v)

        changes[k] = v

        if write_environ is not None:
            write_environ[k] = v

    return changes

