def bind(instance, func, as_name):
    """
    Turn a function to a bound method on an instance

    >>> class Foo(object):
    ...     def __init__(self, x, y):
    ...         self.x = x
    ...         self.y = y
    >>> foo = Foo(2, 3)
    >>> my_unbound_method = lambda self: self.x * self.y
    >>> bind(foo, my_unbound_method, 'multiply')
    >>> foo.multiply()  # noinspection PyUnresolvedReferences
    6

    :param object instance: some object
    :param callable func: unbound method (i.e. a function that takes `self` argument, that you now
        want to be bound to this class as a method)
    :param str as_name: name of the method to create on the object
    """
    setattr(instance, as_name, func.__get__(instance, instance.__class__))

