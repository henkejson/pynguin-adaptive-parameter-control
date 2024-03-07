import logging
import logging.config
import inspect
import sys
import os

from contextlib import contextmanager


class _PyInfo(object):
    PY2 = sys.version_info[0] == 2
    PY3 = sys.version_info[0] == 3

    if PY3:
        string_types = str,
        text_type = str
        binary_type = bytes
    else:  # PY2
        string_types = basestring,
        text_type = unicode
        binary_type = str


def _namespace_from_calling_context():
    """
    Derive a namespace from the module containing the caller's caller.

    :return: the fully qualified python name of a module.
    :rtype: str
    """
    # Not py3k compat
    # return inspect.currentframe(2).f_globals["__name__"]
    # TODO Does this work in both py2/3?
    return inspect.stack()[2][0].f_globals["__name__"]


DEFAULT_CONFIG = dict(
    version=1,
    disable_existing_loggers=False,
    formatters={
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format':
                '%(bg_black)s%(log_color)s'
                '[%(asctime)s] '
                '[%(name)s/%(process)d] '
                '%(message)s '
                '%(blue)s@%(funcName)s:%(lineno)d '
                '#%(levelname)s'
                '%(reset)s',
            'datefmt': '%H:%M:%S',
        },
        'simple': {
            # format=' '.join(
            #     [
            #         '%(asctime)s|',
            #         '%(name)s/%(processName)s[%(process)d]-%(threadName)s[%(thread)d]:'
            #         '%(message)s @%(funcName)s:%(lineno)d #%(levelname)s',
            #     ]
            # ),
            'format':
                '%(asctime)s| %(name)s/%(processName)s[%(process)d]-%(threadName)s[%(thread)d]: '
                '%(message)s @%(funcName)s:%(lineno)d #%(levelname)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    handlers={
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
            'level': logging.DEBUG,
        },
    },
    root=dict(handlers=['console'], level=logging.DEBUG),
    loggers={
        'requests': dict(level=logging.INFO),

        # ipython completion
        'parso': dict(level=logging.INFO),
        'importmagic': dict(level=logging.INFO),
    },
)


def configure(config=None, env_var='LOGGING', default=DEFAULT_CONFIG):
    """

    >>> log = logging.getLogger(__name__)
    >>> configure()
    >>> log.info('test')

    """
    cfg = get_config(config, env_var, default)

    try:
        logging.config.dictConfig(cfg)
    except TypeError as exc:
        try:
            logging.basicConfig(**cfg)
        except Exception as inner_exc:
            raise inner_exc from exc


def get_config(given=None, env_var=None, default=None):
    config = given

    if not config and env_var:
        config = os.environ.get(env_var)

    if not config and default:
        config = default

    if config is None:
        raise ValueError('Invalid logging config: %s' % config)

    if isinstance(config, _PyInfo.string_types):
        import json

        try:
            config = json.loads(config)
        except ValueError:
            import yaml

            try:
                config = yaml.load(config)
            except ValueError:
                raise ValueError(
                    "Could not parse logging config as bare, json,"
                    " or yaml: %s" % config
                )

    return config


_CONFIGURED = []


def _ensure_configured(_has_configured=_CONFIGURED):
    if _has_configured:
        return

    configure()
    _has_configured.append(True)


def get_logger(name=None):
    """
    >>> log = get_logger()
    >>> log.info('test')

    >>> log = get_logger('test2')
    >>> log.info('test2')
    """
    _ensure_configured()

    if not name:
        name = _namespace_from_calling_context()

    return logging.getLogger(name)


# gross, old stdlib. gross.
getLogger = get_logger


@contextmanager
def logger_level(logger, level):
    """Set logger level to `level` within a context block. Don't use this except for debugging please, it's gross."""
    initial = logger.level
    logger.level = level
    try:
        yield
    finally:
        logger.level = initial
