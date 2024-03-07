class roclassproperty(object):
    """
    Read-only class property descriptor factory/decorator.
    """

    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


classproperty = roclassproperty


class setterproperty(object):
    def __init__(self, func, doc=None):
        self.func = func
        self.__doc__ = doc if doc is not None else func.__doc__

    def __set__(self, obj, value):
        return self.func(obj, value)


def lazyperclassproperty(fn):
    """
    Lazy/Cached class property that stores separate instances per class/inheritor so there's no overlap.
    """

    @classproperty
    def _lazyclassprop(cls):
        attr_name = '_%s_lazy_%s' % (cls.__name__, fn.__name__)
        if not hasattr(cls, attr_name):
            setattr(cls, attr_name, fn(cls))
        return getattr(cls, attr_name)

    return _lazyclassprop


def lazyclassproperty(fn):
    """
    Lazy/Cached class property.
    """
    attr_name = '_lazy_' + fn.__name__

    @classproperty
    def _lazyclassprop(cls):
        if not hasattr(cls, attr_name):
            setattr(cls, attr_name, fn(cls))
        return getattr(cls, attr_name)

    return _lazyclassprop
