"""
This module provides the configuration for our complete test suite.

We are using `nox` as our test-suite runner.

Unlike the default and common use pattern, we let `nox` run all commands via the
same Python interpreter as it is invoked by.

This makes `pyright` happy. Furthermore, we are using Nix to install all
development dependencies anyway.

A few examples for invoking `nox`:

```sh
python -m nox
python -m nox -k "not pytest"
python -m nox -k "not pyright and not mypy and not pytest"
python -m nox -s pyright mypy
python -m nox -s black isort
```

Note that we are not invoking `nox` directly. The reason is that it is installed
via Nix and its Python interpreter is different than our Python interpreter
under the Nix shell. Otherwise, none of our development dependencies would be
accessible by `nox` sessions.
"""

import nox

#: Files and directories of interest.
paths = [
    "noxfile.py",
    "pypara",
    "tests",
]


@nox.session(python=False)
def black(session: nox.Session) -> None:
    session.run("black", "--check", *paths, external=True)


@nox.session(python=False)
def isort(session: nox.Session) -> None:
    session.run("isort", "--check-only", *paths, external=True)


@nox.session(python=False)
def pylint(session: nox.Session) -> None:
    session.run("pylint", "pypara", "tests", external=True)


@nox.session(python=False)
def flake8(session: nox.Session) -> None:
    session.run("flake8", "pypara", "tests", external=True)


@nox.session(python=False)
def pyright(session: nox.Session) -> None:
    session.run("pyright", external=True)


@nox.session(python=False)
def mypy(session: nox.Session) -> None:
    session.run("mypy", "pypara", "tests", external=True)


@nox.session(python=False)
def pytest(session: nox.Session) -> None:
    session.run("pytest", "--verbose", "--cov", "--doctest-modules", external=True)


@nox.session(python=False)
def piplist(session: nox.Session) -> None:
    session.run("pip", "list", "-o")
