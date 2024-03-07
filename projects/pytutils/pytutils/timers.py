import logging
import time

_LOG = logging.getLogger(__name__)


class Timer(object):
    """
    Context manager that times it's execution.
    """

    def __init__(self, name='', verbose=False):
        self.name = name
        self.verbose = verbose

    def __repr__(self):
        return '{cls_name}({name})'.format(cls_name=self.__class__.__name__, name=self.name)

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs

        if self.verbose:
            _LOG.debug('%s: Elapsed time: %f ms', self, self.msecs)


