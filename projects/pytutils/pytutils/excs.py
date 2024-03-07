from contextlib import contextmanager


@contextmanager
def ok(*exceptions):
    """Context manager to pass exceptions.
    :param exceptions: Exceptions to pass
    """
    try:
        yield
    except Exception as e:
        if isinstance(e, exceptions):
            pass
        else:
            raise e

