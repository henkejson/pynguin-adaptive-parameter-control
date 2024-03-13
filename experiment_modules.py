import random


def randomize_modules():
    # seed generated from os.urandom(20)
    random.seed(b'&\xf6\xbc\xd3\xc9\xc7\x86\t8:p\xd1\x01\x1au\x0f\x9f\x11\xa0\xc9')

    # Generate a list of 24 unique numbers from 1 to 65
    random_numbers = random.sample(range(1, 66), 24)

    random_numbers.sort()
    print(random_numbers)


def get_path_modules() -> (str, str):
    """Paths and modules for all python files used for experimentation"""
    # Relative address (from input/) and module names for all files
    path_modules = [

        # ("projects/codetiming", "codetiming._timer"),  # 1.

        # ("projects/flake8/src", "flake8.formatting.base"),  # 2
        ("projects/flake8/src", "flake8.formatting.default"),  # 3
        # ("projects/flake8/src", "flake8.main.debug"),  # 4

        ("projects/flutils", "flutils.decorators"),  # 5
        # ("projects/flutils", "flutils.namedtupleutils"),  # 6
        ("projects/flutils", "flutils.packages"),  # 7
        # ("projects/flutils", "flutils.setuputils.cmd"),  # 8

        # ("projects/httpie", "httpie.cli.dicts"),  # 9
        # ("projects/httpie", "httpie.output.formatters.colors"),  # 10
        # ("projects/httpie", "httpie.output.formatters.headers"),  # 11
        ("projects/httpie", "httpie.output.processing"),  # 12
        ("projects/httpie", "httpie.output.streams"),  # 13
        # ("projects/httpie", "httpie.plugins.base"),  # 14
        # ("projects/httpie", "httpie.sessions"),  # 15
        ("projects/httpie", "httpie.ssl_"),  # 16

        # ("projects/isort", "isort.exceptions"),  # 17
        # ("projects/isort", "isort.utils"),  # 18

        # ("projects/mimesis", "mimesis.builtins.da"),  # 19
        # ("projects/mimesis", "mimesis.builtins.it"),  # 20
        # ("projects/mimesis", "mimesis.builtins.pt_br"),  # 21
        # # ("projects/mimesis", "mimesis.providers.choice"),  # 22
        #
        # # ("projects/py-backwards", "py_backwards.conf"),  # 23
        # # ("projects/py-backwards", "py_backwards.files"),  # 24
        # ("projects/py-backwards", "py_backwards.transformers.base"),  # 25
        # ("projects/py-backwards", "py_backwards.transformers.dict_unpacking"),  # 26
        # # ("projects/py-backwards", "py_backwards.transformers.formatted_values"),  # 27
        # # ("projects/py-backwards", "py_backwards.transformers.metaclass"),  # 28
        # ("projects/py-backwards", "py_backwards.transformers.python2_future"),  # 29
        # # ("projects/py-backwards", "py_backwards.transformers.return_from_generator"),  # 30
        # # ("projects/py-backwards", "py_backwards.transformers.starred_unpacking"),  # 31
        # ("projects/py-backwards", "py_backwards.transformers.string_types"),  # 32
        # # ("projects/py-backwards", "py_backwards.transformers.variables_annotations"),  # 33
        # # ("projects/py-backwards", "py_backwards.transformers.yield_from"),  # 34
        # # ("projects/py-backwards", "py_backwards.utils.helpers"),  # 35
        # ("projects/py-backwards", "py_backwards.utils.snippet"),  # 36
        #
        # ("projects/pyMonet", "pymonet.immutable_list"),  # 37
        # # ("projects/pyMonet", "pymonet.lazy"),  # 38
        # # ("projects/pyMonet", "pymonet.maybe"),  # 39
        # ("projects/pyMonet", "pymonet.monad_try"),  # 40
        # # ("projects/pyMonet", "pymonet.semigroups"),  # 41
        # # ("projects/pyMonet", "pymonet.task"),  # 42
        # # ("projects/pyMonet", "pymonet.validation"),  # 43
        #
        # # ("projects/pypara", "pypara.accounting.journaling"),  # 44
        # ("projects/pypara", "pypara.commons.errors"),  # 45
        # ("projects/pypara", "pypara.monetary"),  # 46
        #
        # ("projects/pytutils", "pytutils.excs"),  # 47
        # # ("projects/pytutils", "pytutils.lazy.lazy_import"),  # 48
        # # ("projects/pytutils", "pytutils.props"),  # 49
        # ("projects/pytutils", "pytutils.python"),  # 50
        #
        # ("projects/sanic", "sanic.config"),  # 51
        # # ("projects/sanic", "sanic.headers"),  # 52
        # # ("projects/sanic", "sanic.helpers"),  # 53
        # # ("projects/sanic", "sanic.mixins.listeners"),  # 54
        # ("projects/sanic", "sanic.mixins.middleware"),  # 55
        # # ("projects/sanic", "sanic.mixins.routes"),  # 56
        # # ("projects/sanic", "sanic.mixins.signals"),  # 57
        # # ("projects/sanic", "sanic.models.protocol_types"),  # 58
        # ("projects/sanic", "sanic.views"),  # 59
        #
        # ("projects/string-utils", "string_utils.manipulation"),  # 60
        #
        # ("projects/thonny", "thonny.languages"),  # 61
        # # ("projects/thonny", "thonny.plugins.pgzero_frontend"),  # 62
        # # ("projects/thonny", "thonny.roughparse"),  # 63
        # ("projects/thonny", "thonny.terminal"),  # 64

        # ("projects/typesystem", "typesystem.tokenize.positional_validation"),  # 65
    ]
    return path_modules
