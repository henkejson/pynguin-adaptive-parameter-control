import random


def randomize_modules():
    # seed generated from os.urandom(20)
    random.seed(b'\x0b\xfdg=\x98\xbe\xf9z$?fp\x81m95\x029gH')

    # Generate a list of 24 unique numbers from 1 to 66
    random_numbers = random.sample(range(1, 67), 24)

    random_numbers.sort()
    print(random_numbers)


def get_path_modules() -> (str, str):
    """Paths and modules for all python files used for experimentation"""
    # Relative address (from input/) and module names for all files
    path_modules = [

        # ("projects/codetiming", "codetiming._timer"),  # 1.

        # ("projects/flake8/src", "flake8.formatting.base"),  # 2
        # ("projects/flake8/src", "flake8.formatting.default"),  # 3
        # ("projects/flake8/src", "flake8.main.debug"),  # 4

        # ("projects/flutils", "flutils.decorators"),  # 5
        # ("projects/flutils", "flutils.namedtupleutils"),  # 6
        # ("projects/flutils", "flutils.packages"),  # 7
        # ("projects/flutils", "flutils.pathutils"),  # 8
        # ("projects/flutils", "flutils.setuputils.cmd"),  # 9

        # ("projects/httpie", "httpie.cli.dicts"),  # 10
        # ("projects/httpie", "httpie.output.formatters.colors"),  # 11
        # ("projects/httpie", "httpie.output.formatters.headers"),  # 12
        # ("projects/httpie", "httpie.output.processing"),  # 13
        # ("projects/httpie", "httpie.output.streams"),  # 14
        # ("projects/httpie", "httpie.plugins.base"),  # 15
        # ("projects/httpie", "httpie.sessions"),  # 16
        # ("projects/httpie", "httpie.ssl_"),  # 17

        # ("projects/isort", "isort.exceptions"),  # 18
        # ("projects/isort", "isort.utils"),  # 19

        # ("projects/mimesis", "mimesis.builtins.da"),  # 20
        # ("projects/mimesis", "mimesis.builtins.it"),  # 21
        # ("projects/mimesis", "mimesis.builtins.pt_br"),  # 22
        # ("projects/mimesis", "mimesis.providers.choice"),  # 23

        # ("projects/py-backwards", "py_backwards.conf"),  # 24
        # ("projects/py-backwards", "py_backwards.files"),  # 25
        # ("projects/py-backwards", "py_backwards.transformers.base"),  # 26
        # ("projects/py-backwards", "py_backwards.transformers.dict_unpacking"),  # 27
        # ("projects/py-backwards", "py_backwards.transformers.formatted_values"),  # 28
        # ("projects/py-backwards", "py_backwards.transformers.metaclass"),  # 29
        # ("projects/py-backwards", "py_backwards.transformers.python2_future"),  # 30
        # ("projects/py-backwards", "py_backwards.transformers.return_from_generator"),  # 31
        # ("projects/py-backwards", "py_backwards.transformers.starred_unpacking"),  # 32
        # ("projects/py-backwards", "py_backwards.transformers.string_types"),  # 33
        # ("projects/py-backwards", "py_backwards.transformers.variables_annotations"),  # 34
        # ("projects/py-backwards", "py_backwards.transformers.yield_from"),  # 35
        # ("projects/py-backwards", "py_backwards.utils.helpers"),  # 36
        ("projects/py-backwards", "py_backwards.utils.snippet"),  # 37

        # ("projects/pyMonet", "pymonet.immutable_list"),  # 38
        # ("projects/pyMonet", "pymonet.lazy"),  # 39
        ("projects/pyMonet", "pymonet.maybe"),  # 40
        # ("projects/pyMonet", "pymonet.monad_try"),  # 41
        # ("projects/pyMonet", "pymonet.semigroups"),  # 42
        # ("projects/pyMonet", "pymonet.task"),  # 43
        # ("projects/pyMonet", "pymonet.validation"),  # 44

        # ("projects/pypara", "pypara.accounting.journaling"),  # 45
        # ("projects/pypara", "pypara.commons.errors"),  # 46
        ("projects/pypara", "pypara.monetary"),  # 47

        # ("projects/pytutils", "pytutils.excs"),  # 48
        # ("projects/pytutils", "pytutils.lazy.lazy_import"),  # 49
        ("projects/pytutils", "pytutils.props"),  # 50
        ("projects/pytutils", "pytutils.python"),  # 51

        # ("projects/sanic", "sanic.config"),  # 52
        # ("projects/sanic", "sanic.headers"),  # 53
        # ("projects/sanic", "sanic.helpers"),  # 54
        ("projects/sanic", "sanic.mixins.listeners"),  # 55
        # ("projects/sanic", "sanic.mixins.middleware"),  # 56
        # ("projects/sanic", "sanic.mixins.routes"),  # 57
        # ("projects/sanic", "sanic.mixins.signals"),  # 58
        # ("projects/sanic", "sanic.models.protocol_types"),  # 59
        # ("projects/sanic", "sanic.views"),  # 60

        # ("projects/string-utils", "string_utils.manipulation"),  # 61

        # ("projects/thonny", "thonny.languages"),  # 62
        # ("projects/thonny", "thonny.plugins.pgzero_frontend"),  # 63
        # ("projects/thonny", "thonny.roughparse"),  # 64
        # ("projects/thonny", "thonny.terminal"),  # 65

        # ("projects/typesystem", "typesystem.tokenize.positional_validation"),  # 66
    ]
    return path_modules
