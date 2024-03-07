import functools

import cachetools

from .props import lazyclassproperty, lazyperclassproperty

_default = []  # evaluates to False


class CachedException(object):
    def __init__(self, ex):
        self.ex = ex

    def throw(self):
        raise self.ex

    __call__ = throw


def cachedmethod(cache, key=_default, lock=None, typed=_default, cached_exception=None):
    """Decorator to wrap a class or instance method with a memoizing
    callable that saves results in a cache.

    You can also specify a cached exception to cache and re-throw as well.

    Originally from cachetools, but modified to support caching certain exceptions.
    """
    if key is not _default and not callable(key):
        key, typed = _default, key
    if typed is not _default:
        warnings.warn(
            "Passing 'typed' to cachedmethod() is deprecated, "
            "use 'key=typedkey' instead", DeprecationWarning, 2
        )

    def decorator(method):
        # pass method to default key function for backwards compatibilty
        if key is _default:
            makekey = functools.partial(cachetools.typedkey if typed else cachetools.hashkey, method)
        else:
            makekey = key  # custom key function always receive method args

        @six.wraps(method)
        def wrapper(self, *args, **kwargs):
            c = cache(self)
            ret = _sentinel

            if c is not None:
                k = makekey(self, *args, **kwargs)
                try:
                    if lock is not None:
                        with lock(self):
                            ret = c[k]
                    else:
                        ret = c[k]
                except KeyError:
                    pass  # key not found

            if ret is _sentinel:
                try:
                    ret = method(self, *args, **kwargs)
                except cached_exception as e:
                    ret = CachedException(e)

                if c is not None:
                    try:
                        if lock is not None:
                            with lock(self):
                                c[k] = ret
                        else:
                            c[k] = ret
                    except ValueError:
                        pass  # value too large

            if isinstance(ret, CachedException):
                ret()
            else:
                return ret

        # deprecated wrapper attribute
        def getter(self):
            warnings.warn('%s.cache is deprecated' % method.__name__, DeprecationWarning, 2)
            return cache(self)

        wrapper.cache = getter
        return wrapper

    return decorator


def lazyproperty(fn):
    """
    Lazy/Cached property.
    """
    attr_name = '_lazy_' + fn.__name__

    @property
    def _lazyprop(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return _lazyprop
