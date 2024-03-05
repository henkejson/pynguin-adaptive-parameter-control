import errno
import fcntl
import os
import pty
import shlex
import shutil
import struct
import subprocess
import sys
import termios
from collections import UserString
from copy import copy
from itertools import chain
from select import select
from subprocess import Popen
from typing import (
    Any,
    IO,
    List,
    NamedTuple,
    Optional,
    Sequence,
    TextIO,
    Tuple,
    cast,
)

from flutils.codecs import get_encoding
from flutils.namedtupleutils import to_namedtuple

try:  # pragma: no cover
    from functools import cached_property  # type: ignore
except ImportError:  # pragma: no cover
    from flutils.decorators import cached_property  # type: ignore

__all__ = ['run', 'prep_cmd', 'CompletedProcess', 'RunCmd']


def _set_size(
        fd: int,
        columns: int = 80,
        lines: int = 20
) -> None:
    """Using the passed in file descriptor (of tty), set the terminal
    size to that of the current terminal size.  If the current
    terminal size cannot be found the given defaults will be used.
    """
    # The following was adapted from: https://stackoverflow.com/a/6420070
    size = struct.pack("HHHH", lines, columns, 0, 0)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, size)  # type: ignore[call-overload]


def run(
        command: Sequence,
        stdout: Optional[IO] = None,
        stderr: Optional[IO] = None,
        columns: int = 80,
        lines: int = 24,
        force_dimensions: bool = False,
        interactive: bool = False,
        **kwargs: Any
) -> int:
    """Run the given command line command and return the command's
    return code.

    When the given ``command`` is executed, the command's stdout and
    stderr outputs are captured in a pseudo terminal.  The captured
    outputs are then added to this function's ``stdout`` and ``stderr``
    IO objects.

    This function will capture any ANSI escape codes in the output of
    the given command.  This even includes ANSI colors.

    Args:
        command (str, List[str], Tuple[str]): The command to execute.
        stdout (:obj:`typing.IO`, optional):  An input/output stream
            that will hold the command's ``stdout``.  Defaults to:
            :obj:`sys.stdout <sys.stdout>`; which will output
            the command's ``stdout`` to the terminal.
        stderr (:obj:`typing.IO`, optional):  An input/output stream
            that will hold the command's ``stderr``.  Defaults to:
            :obj:`sys.stderr <sys.stderr>`; which will output
            the command's ``stderr`` to the terminal.
        columns (int, optional): The number of character columns the pseudo
            terminal may use.  If ``force_dimensions`` is :obj:`False`, this
            will be the fallback columns value when the the current terminal's
            column size cannot be found.  If ``force_dimensions`` is
            :obj:`True`, this will be actual character column value.
            Defaults to: ``80``.
        lines (int, optional): The number of character lines the pseudo
            terminal may use.  If ``force_dimensions`` is :obj:`False`, this
            will be the fallback lines value when the the current terminal's
            line size cannot be found.  If ``force_dimensions`` is :obj:`True`,
            this will be actual character lines value.  Defaults to: ``24``.
        force_dimensions (bool, optional): This controls how the given
            ``columns`` and ``lines`` values are to be used.  A value of
            :obj:`False` will use the given ``columns`` and ``lines`` as
            fallback values if the current terminal dimensions cannot be
            successfully queried.  A value of :obj:`True` will resize the
            pseudo terminal using the given ``columns`` and ``lines`` values.
            Defaults to: :obj:`False`.
        interactive (bool, optional): A value of :obj:`True` will
            interactively run the given ``command``.  Defaults to:
            :obj:`False`.
        **kwargs: Any additional key-word-arguments used with
            :obj:`Popen <subprocess.Popen>`.  ``stdout`` and ``stderr``
            will not be used if given in ``**default_kwargs``.  Defaults to:
            ``{}``.

    Returns:
        int: The return value from running the given ``command``

    Raises:
        RuntimeError: When using ``interactive=True`` and the ``bash``
            executable cannot be located.
        OSError: Any errors raised when trying to read the pseudo terminal.

    Example:
        An example using :obj:`~flutils.cmdutils.run` in code::

            from flutils.cmdutils import run
            from io import BytesIO
            import sys
            import os

            home = os.path.expanduser('~')
            with BytesIO() as stream:
                return_code = run(
                    'ls "%s"' % home,
                    stdout=stream,
                    stderr=stream
                )
                text = stream.getvalue()
            text = text.decode(sys.getdefaultencoding())
            if return_code == 0:
                print(text)
            else:
                print('Error: %s' % text)
    """
    # Handle bytes
    if hasattr(command, 'decode'):
        raise TypeError(
            "The given 'command' must be of type: str, List[str] or "
            "Tuple[str]."
        )
    # Handle str
    cmd: List[str]
    if hasattr(command, 'capitalize'):
        command = cast(str, command)
        cmd = list(shlex.split(command))
    else:
        cmd = list(command)

    if interactive is True:
        bash = shutil.which('bash')
        if not bash:
            raise RuntimeError(
                "Unable to run the command:  %r, in interactive mode "
                "because 'bash' could NOT be found on the system."
                % ' '.join(command)
            )
        cmd = [bash, '-i', '-c'] + cmd

    if stdout is None:
        stdout = sys.stdout
    stdout = cast(IO, stdout)

    if stderr is None:
        stderr = sys.stderr
    stderr = cast(IO, stderr)

    if force_dimensions is False:
        columns, lines = shutil.get_terminal_size(
            fallback=(columns, lines)
        )

    # The following is adapted from: https://stackoverflow.com/a/31953436

    masters, slaves = zip(pty.openpty(), pty.openpty())

    try:
        # Resize the pseudo terminals to the size of the current terminal
        for fd in chain(masters, slaves):
            _set_size(
                fd,
                columns=columns,
                lines=lines
            )

        kwargs['stdout'] = slaves[0]
        kwargs['stderr'] = slaves[1]

        if 'stdin' not in kwargs.keys():
            kwargs['stdin'] = slaves[0]

        with Popen(cmd, **kwargs) as p:

            for fd in slaves:
                os.close(fd)  # no input
            readable = {
                masters[0]: stdout,
                masters[1]: stderr,
            }
            while readable:
                for fd in select(readable, [], [])[0]:
                    try:
                        data = os.read(fd, 1024)  # read available
                    except OSError as e:
                        if e.errno != errno.EIO:
                            raise
                        del readable[fd]  # EIO means EOF on some systems
                    else:
                        if not data:  # EOF
                            del readable[fd]
                        else:
                            if hasattr(readable[fd], 'encoding'):
                                obj = readable[fd]
                                obj = cast(TextIO, obj)
                                data_str = data.decode(
                                    obj.encoding
                                )
                                readable[fd].write(data_str)
                            else:
                                readable[fd].write(data)
                            readable[fd].flush()
    finally:
        for fd in chain(masters, slaves):
            try:
                os.close(fd)
            except OSError:
                pass
    return p.returncode


def prep_cmd(cmd: Sequence) -> Tuple[str, ...]:
    """Convert a given command into a tuple for use by
    :obj:`subprocess.Popen`.

    Args:
        cmd (:obj:`Sequence <typing.Sequence>`): The command to be converted.

    This is for converting a command of type string or bytes to a tuple of
    strings for use by :obj:`subprocess.Popen`.

    Example:

        >>> from flutils.cmdutils import prep_cmd
        >>> prep_cmd('ls -Flap')
        ('ls', '-Flap')
    """
    if not hasattr(cmd, 'count') or not hasattr(cmd, 'index'):
        raise TypeError(
            "The given 'cmd', %r, must be of type: str, bytes, list or "
            "tuple.  Got: %r" % (
                cmd,
                type(cmd).__name__
            )
        )
    if hasattr(cmd, 'append'):
        out = copy(cmd)
    else:
        out = cmd
    if hasattr(out, 'decode'):
        out = cast(bytes, out)
        out = out.decode(get_encoding())
    if hasattr(out, 'encode'):
        out = cast(str, out)
        out = shlex.split(out)
    out = tuple(out)
    out = cast(Tuple[str], out)
    item: str
    for x, item in enumerate(out):
        if not isinstance(item, (str, UserString)):
            raise TypeError(
                "Item %r of the given 'cmd' is not of type 'str'.  "
                "Got: %r" % (
                    x,
                    type(item).__name__
                )
            )
    return out


class CompletedProcess(NamedTuple):
    """A :obj:`NamedTuple <typing.NamedTuple>` that holds a completed
    process' information.

    Attributes:
         return_code (int): The process return code.
         stdout (str): All lines of the ``stdout`` from the process.
         stderr (str): All lines of the ``stderr`` from the process.
         cmd (str): The command that the process ran.
    """
    return_code: int
    stdout: str
    stderr: str
    cmd: str


class RunCmd:
    """A simple callable that simplifies many calls to :obj:`subprocess.run`.

    Args:
        raise_error (bool, optional): A value of :obj:`True` will raise
            a :obj:`ChildProcessError` if the process,
            exits with a non-zero return code. Default: :obj:`True`
        output_encoding (str, optional): If set, the returned ``stdout``
            and ``stderr`` will be converted to from bytes to a Python
            string using this given ``encoding``.  Defaults to:
            :obj:`None` which will use the value from
            :obj:`locale.getpreferredencoding` or, if not set, the value
            from :obj:`sys.getdefaultencoding` will be used. If the given
            encoding does NOT exist the default will be used.
        **default_kwargs: Any :obj:`subprocess.Popen` keyword argument.

    Attributes:
        default_kwargs (:obj:`NamedTuple <typing.NamedTuple>`): The
            ``default_kwargs`` passed into the constructor which may be
            passed on to :obj:`subprocess.run`.
        output_encoding (str): The encoding used to decode the process
            output

    """

    def __init__(
            self,
            raise_error: bool = True,
            output_encoding: Optional[str] = None,
            **default_kwargs: Any
    ) -> None:
        self.raise_error: bool = raise_error
        if not hasattr(output_encoding, 'encode'):
            output_encoding = ''
        output_encoding = cast(str, output_encoding)
        self._output_encoding: str = output_encoding
        self.default_kwargs: Any = to_namedtuple(default_kwargs)
        self.default_kwargs = cast(NamedTuple, self.default_kwargs)

    @cached_property
    def output_encoding(self) -> str:
        return get_encoding(self._output_encoding)

    def __call__(
            self,
            cmd: Sequence,
            **kwargs: Any,
    ) -> CompletedProcess:
        """Run the given command and return the result.

        Args:
             cmd (:obj:`Sequence <typing.Sequence>`): The command
             **kwargs: Any default_kwargs to pass to :obj:`subprocess.run`.
                These default_kwargs will override any ``default_kwargs``
                set in the constructor.

        Raises:
            FileNotFoundError: If the given ``cmd`` cannot be found.
            ChildProcessError: If ``raise_error=True`` was set in this
                class' constructor; and, the process (from running the
                given ``cmd``) returns a non-zero value.
            ValueError: If the given ``**kwargs`` has invalid arguments.

        Example:

            >>> from flutils.cmdutils import RunCmd
            >>> from subprocess import PIPE
            >>> import os
            >>> run_command = RunCmd(stdout=PIPE, stderr=PIPE)
            >>> result = run_command('ls -flap %s' % os.getcwd())
            >>> result.return_code
            0
            >>> result.stdout
            ...
            >>> result = run_command('ls -flap %s' % os.path.expanduser('~'))
        """
        cmd = prep_cmd(cmd)
        cmd = cast(Tuple[str, ...], cmd)
        # noinspection PyProtectedMember
        keyword_args = self.default_kwargs._asdict()
        keyword_args.update(kwargs)
        result = subprocess.run(cmd, **keyword_args)
        cmd = shlex.join(cmd)
        cmd = cast(str, cmd)
        stdout = result.stdout.decode(self.output_encoding)
        stderr = result.stderr.decode(self.output_encoding)
        if self.raise_error is True:
            if result.returncode != 0:
                raise ChildProcessError(
                    f'Unable to run the command {cmd!r}:\n\n {stdout} '
                    f'{stderr} Return code: {result.returncode}'
                )
        return CompletedProcess(
            return_code=result.returncode,
            stdout=stdout,
            stderr=stderr,
            cmd=cmd,
        )
