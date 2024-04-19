import random


def randomize_modules():
    # seed generated from os.urandom(20)
    random.seed(b'\x02.f\xfc f\x15\x1f\xa0w\xb9]\xae\x7fu\xb4\xf9\x8a/\x8e')

    # Generate a list of 24 unique numbers from 1 to 58
    random_numbers = random.sample(range(1, 59), 24)

    random_numbers.sort()
    print(random_numbers)


def get_path_modules() -> (str, str):
    """Paths and modules for all python files used for experimentation"""
    # Relative address (from input/) and module names for all files
    path_modules = [

        ("projects/codetiming", "codetiming._timer"),  # 1.

        ("projects/flake8/src", "flake8.formatting.base"),  # 2
        ("projects/flake8/src", "flake8.formatting.default"),  # 3
        # ("projects/flake8/src", "flake8.main.debug"),  # 4

        # ("projects/flutils", "flutils.decorators"),  # 5
        # ("projects/flutils", "flutils.namedtupleutils"),  # 6
        # ("projects/flutils", "flutils.packages"),  # 7
        # ("projects/flutils", "flutils.setuputils.cmd"),  # 8

        # ("projects/httpie", "httpie.cli.dicts"),  # 9
        # ("projects/httpie", "httpie.output.formatters.headers"),  # 10
        # ("projects/httpie", "httpie.output.processing"),  # 11
        # ("projects/httpie", "httpie.output.streams"),  # 12
        # ("projects/httpie", "httpie.plugins.base"),  # 13
        # ("projects/httpie", "httpie.sessions"),  # 14
        # ("projects/httpie", "httpie.ssl_"),  # 15

        # ("projects/isort", "isort.exceptions"),  # 16
        # ("projects/isort", "isort.utils"),  # 17

        # ("projects/mimesis", "mimesis.builtins.da"),  # 18
        # ("projects/mimesis", "mimesis.builtins.pt_br"),  # 19

        # ("projects/py-backwards", "py_backwards.conf"),  # 20
        # ("projects/py-backwards", "py_backwards.files"),  # 21
        # ("projects/py-backwards", "py_backwards.transformers.base"),  # 22
        # ("projects/py-backwards", "py_backwards.transformers.dict_unpacking"),  # 23
        # ("projects/py-backwards", "py_backwards.transformers.metaclass"),  # 24
        # ("projects/py-backwards", "py_backwards.transformers.python2_future"),  # 25
        # ("projects/py-backwards", "py_backwards.transformers.return_from_generator"),  # 26
        # ("projects/py-backwards", "py_backwards.transformers.starred_unpacking"),  # 27
        # ("projects/py-backwards", "py_backwards.transformers.string_types"),  # 28
        # ("projects/py-backwards", "py_backwards.transformers.variables_annotations"),  # 29
        # ("projects/py-backwards", "py_backwards.transformers.yield_from"),  # 30
        # ("projects/py-backwards", "py_backwards.utils.helpers"),  # 31
        # ("projects/py-backwards", "py_backwards.utils.snippet"),  # 32

        # ("projects/pyMonet", "pymonet.immutable_list"),  # 33
        # ("projects/pyMonet", "pymonet.lazy"),  # 34
        # ("projects/pyMonet", "pymonet.maybe"),  # 35
        # ("projects/pyMonet", "pymonet.monad_try"),  # 36
        # ("projects/pyMonet", "pymonet.semigroups"),  # 37
        # ("projects/pyMonet", "pymonet.task"),  # 38
        # ("projects/pyMonet", "pymonet.validation"),  # 39

        # ("projects/pypara", "pypara.accounting.journaling"),  # 40
        # ("projects/pypara", "pypara.commons.errors"),  # 41

        # ("projects/pytutils", "pytutils.excs"),  # 42
        # ("projects/pytutils", "pytutils.lazy.lazy_import"),  # 43
        # ("projects/pytutils", "pytutils.props"),  # 44
        # ("projects/pytutils", "pytutils.python"),  # 45

        # ("projects/sanic", "sanic.config"),  # 46
        # ("projects/sanic", "sanic.headers"),  # 47
        # ("projects/sanic", "sanic.helpers"),  # 48
        # ("projects/sanic", "sanic.mixins.listeners"),  # 49
        # ("projects/sanic", "sanic.mixins.middleware"),  # 50
        # ("projects/sanic", "sanic.mixins.routes"),  # 51
        # ("projects/sanic", "sanic.mixins.signals"),  # 52
        # ("projects/sanic", "sanic.models.protocol_types"),  # 53
        # ("projects/sanic", "sanic.views"),  # 54

        # ("projects/string-utils", "string_utils.manipulation"),  # 55

        # ("projects/thonny", "thonny.plugins.pgzero_frontend"),  # 56
        # ("projects/thonny", "thonny.roughparse"),  # 57

        # ("projects/typesystem", "typesystem.tokenize.positional_validation"),  # 58
    ]
    return path_modules
