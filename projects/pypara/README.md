# Python Library for Currencies and Monetary Values

[![PyPI](https://img.shields.io/pypi/v/pypara?style=flat-square)](https://pypi.org/project/pypara/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pypara?style=flat-square)](https://pypi.org/project/pypara/)
[![License](https://img.shields.io/github/license/vst/pypara?style=flat-square)](https://github.com/vst/pypara/blob/main/LICENSE)
[![Builds](https://img.shields.io/github/actions/workflow/status/vst/pypara/test.yml?style=flat-square)](https://github.com/vst/pypara/actions/workflows/test.yml)
[![Issues](https://img.shields.io/github/issues/vst/pypara?style=flat-square)](https://github.com/vst/pypara/issues)
[![Last Commit](https://img.shields.io/github/last-commit/vst/pypara?style=flat-square)](https://github.com/vst/pypara/commits)

> **TODO**: Provide a complete README.

## Development Notes

Enter the Nix shell:

```sh
nix-shell
```

Run the test suite:

```sh
python -m nox
```

> **Note:** Since we are under Nix shell, `nox` command will attempt to use its
> own Python interpreter pinned during `nox` installation. We want our own
> interpreter to be used during `nox` checks.

Alternatively:

```sh
nix-shell --argstr python python39  --run "python -m nox"
nix-shell --argstr python python310 --run "python -m nox"
nix-shell --argstr python python311 --run "python -m nox"
```

> **Note:** Python 3.9 test are not added to GitHub Actions test workflow. It
> takes very long to setup the Nix shell as Python 3.9 packages are no longer
> fetched from the cache.

## Publishing

Building a package and uploading it to PyPI is handled by the GitHub Action upon
successful GitHub Release (using Release Please Action).

However, in the event of emergency, you can still manually build a package and
upload it to PyPI:

```sh
rm -Rf dist/
python -m build
twine check dist/*
twine upload -s dist/*
```
