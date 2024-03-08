def get_path_modules() -> (str, str):
    """Paths and modules for all python files used for experimentation"""
    # Relative address (from input/) and module names for all files
    path_modules = [

        # ("projects/codetiming", "codetiming._timer"),
        #
        # ("projects/dataclasses-json", "dataclasses_json.undefined"),
        #
        # ("projects/flake8/src", "flake8.formatting.base"),
        # ("projects/flake8/src", "flake8.formatting.default"),
        # ("projects/flake8/src", "flake8.main.debug"),
        #
        # ("projects/flutils", "flutils.decorators"),
        # ("projects/flutils", "flutils.namedtupleutils"),
        # ("projects/flutils", "flutils.packages"),
        # ("projects/flutils", "flutils.pathutils"),
        # ("projects/flutils", "flutils.setuputils.cmd"),
        # ("projects/flutils", "flutils.strutils"),
        #
        #
        # ("projects/httpie", "httpie.cli.dicts"),
        # ("projects/httpie", "httpie.output.formatters.colors"),
        # ("projects/httpie", "httpie.output.formatters.headers"),
        # ("projects/httpie", "httpie.output.formatters.json"),
        # ("projects/httpie", "httpie.output.processing"),
        # ("projects/httpie", "httpie.output.streams"),
        # ("projects/httpie", "httpie.plugins.base"),
        # ("projects/httpie", "httpie.sessions"),
        # ("projects/httpie", "httpie.ssl_"),
        # ("projects/httpie", "httpie.status"),
        #
        # ("projects/isort", "isort.comments"),
        # ("projects/isort", "isort.exceptions"),
        # ("projects/isort", "isort.utils"),
        #
        # ("projects/mimesis", "mimesis.builtins.da"),
        # ("projects/mimesis", "mimesis.builtins.it"),
        # ("projects/mimesis", "mimesis.builtins.pt_br"),
        # ("projects/mimesis", "mimesis.providers.choice"),
        #
        # ("projects/py-backwards", "py_backwards.conf"),
        # ("projects/py-backwards", "py_backwards.files"),
        # ("projects/py-backwards", "py_backwards.transformers.base"),
        # ("projects/py-backwards", "py_backwards.transformers.class_without_bases"),
        # ("projects/py-backwards", "py_backwards.transformers.dict_unpacking"),
        # ("projects/py-backwards", "py_backwards.transformers.formatted_values"),
        # ("projects/py-backwards", "py_backwards.transformers.metaclass"),
        # ("projects/py-backwards", "py_backwards.transformers.python2_future"),
        # ("projects/py-backwards", "py_backwards.transformers.return_from_generator"),
        # ("projects/py-backwards", "py_backwards.transformers.starred_unpacking"),
        # ("projects/py-backwards", "py_backwards.transformers.string_types"),
        # ("projects/py-backwards", "py_backwards.transformers.variables_annotations"),
        # ("projects/py-backwards", "py_backwards.transformers.yield_from"),
        # ("projects/py-backwards", "py_backwards.utils.helpers"),
        # ("projects/py-backwards", "py_backwards.utils.snippet"),
        #
        # ("projects/pyMonet", "pymonet.immutable_list"),
        # ("projects/pyMonet", "pymonet.lazy"),
        # ("projects/pyMonet", "pymonet.maybe"),
        # ("projects/pyMonet", "pymonet.monad_try"),
        # ("projects/pyMonet", "pymonet.semigroups"),
        # ("projects/pyMonet", "pymonet.task"),
        # ("projects/pyMonet", "pymonet.validation"),
        #
        ("projects/pypara", "pypara.accounting.journaling"),
        ("projects/pypara", "pypara.commons.errors"),
        ("projects/pypara", "pypara.monetary"),
        #
        # ("projects/pytutils", "pytutils.excs"),
        # ("projects/pytutils", "pytutils.files"),
        # ("projects/pytutils", "pytutils.lazy.lazy_import"),
        # ("projects/pytutils", "pytutils.path"),
        # ("projects/pytutils", "pytutils.pretty"),
        # ("projects/pytutils", "pytutils.props"),
        # ("projects/pytutils", "pytutils.python"),
        #
        # ("projects/sanic", "sanic.config"),
        # ("projects/sanic", "sanic.headers"),
        # ("projects/sanic", "sanic.helpers"),
        # ("projects/sanic", "sanic.mixins.listeners"),
        # ("projects/sanic", "sanic.mixins.middleware"),
        # ("projects/sanic", "sanic.mixins.routes"),
        # ("projects/sanic", "sanic.mixins.signals"),
        # ("projects/sanic", "sanic.models.protocol_types"),
        # ("projects/sanic", "sanic.views"),
        #
        # ("projects/string-utils", "string_utils.manipulation"),
        #
        # ("projects/thonny", "thonny.languages"),
        # ("projects/thonny", "thonny.plugins.pgzero_frontend"),
        # ("projects/thonny", "thonny.roughparse"),
        # ("projects/thonny", "thonny.terminal"),
        #
        # ("projects/typesystem", "typesystem.tokenize.positional_validation"),
        # ("projects/typesystem", "typesystem.tokenize.tokenize_yaml"),
        # ("projects/typesystem", "typesystem.unique"),


        # ("projects/toy_example", "bmi_calculator")
    ]
    return path_modules
