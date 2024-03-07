"""
From: https://gist.github.com/Skinner927/413c0e9cc8433123f426832f9fe8d931
To use simply copy ClassPropertyMeta and classproperty into your project
"""


class ClassPropertyMeta(type):
    def __setattr__(self, key, value):
        obj = self.__dict__.get(key, None)
        if type(obj) is classproperty:
            return obj.__set__(self, value)
        return super().__setattr__(key, value)


class rwclassproperty(object):
    """
    Similar to @property but used on classes instead of instances.

    The only caveat being that your class must use the
    classproperty.meta metaclass.

    Class properties will still work on class instances unless the
    class instance has overidden the class default. This is no different
    than how class instances normally work.

    Derived from: https://stackoverflow.com/a/5191224/721519

    class Z(object, metaclass=classproperty.meta):
        @classproperty
        def foo(cls):
            return 123

        _bar = None

        @classproperty
        def bar(cls):
            return cls._bar

        @bar.setter
        def bar(cls, value):
            return cls_bar = value


    Z.foo  # 123

    Z.bar  # None
    Z.bar = 222
    Z.bar  # 222

    """

    meta = ClassPropertyMeta

    def __init__(self, fget, fset=None):
        self.fget = self._fix_function(fget)
        self.fset = None if fset is None else self._fix_function(fset)

    def __get__(self, instance, owner=None):
        if not issubclass(type(owner), ClassPropertyMeta):
            raise TypeError(f"Class {owner} does not extend from the required " f"ClassPropertyMeta metaclass")
        return self.fget.__get__(None, owner)()

    def __set__(self, owner, value):
        if not self.fset:
            raise AttributeError("can't set attribute")
        if type(owner) is not ClassPropertyMeta:
            owner = type(owner)
        return self.fset.__get__(None, owner)(value)

    def setter(self, fset):
        self.fset = self._fix_function(fset)
        return self

    _fn_types = (type(__init__), classmethod, staticmethod)

    @classmethod
    def _fix_function(cls, fn):
        if not isinstance(fn, cls._fn_types):
            raise TypeError("Getter or setter must be a function")
        # Always wrap in classmethod so we can call its __get__ and not
        # have to deal with difference between raw functions.
        if not isinstance(fn, (classmethod, staticmethod)):
            return classmethod(fn)
        return fn


classproperty = rwclassproperty

# ---------------- TESTS ----------------
import unittest
from unittest.mock import MagicMock, sentinel


class TestClassProperty(unittest.TestCase):
    def test_get_set(self):
        get_only_cls = MagicMock()
        get_set_get_cls = MagicMock()
        get_set_set_cls = MagicMock()

        class Z(object, metaclass=classproperty.meta):
            _get_set = sentinel.nothing

            @classproperty
            def get_only(cls):
                get_only_cls(cls)
                return sentinel.get_only

            @classproperty
            def get_set(cls):
                get_set_get_cls(cls)
                return cls._get_set

            @get_set.setter
            def get_set(cls, value):
                get_set_set_cls(cls)
                cls._get_set = value

        for c, msg in [(Z, "class"), (Z(), "instance")]:
            with self.subTest(msg=msg):
                # Reset
                Z._get_set = sentinel.nothing

                # Test get_only
                self.assertEqual(sentinel.get_only, c.get_only)
                get_only_cls.assert_called_once_with(Z)
                get_only_cls.reset_mock()

                # Should return our initial "nothing" value
                self.assertEqual(sentinel.nothing, c.get_set)
                get_set_get_cls.assert_called_once_with(Z)
                get_set_get_cls.reset_mock()

                # Now test the set
                c.get_set = sentinel.get_set_val
                get_set_set_cls.assert_called_once_with(Z)
                get_set_set_cls.reset_mock()

                self.assertEqual(sentinel.get_set_val, c.get_set)
                get_set_get_cls.assert_called_once_with(Z)
                get_set_get_cls.reset_mock()

    def test_read_only(self):
        class Z(object, metaclass=classproperty.meta):
            _get_set = sentinel.nothing

            @classproperty
            def get_only(cls):
                return sentinel.get_only

        self.assertEqual(sentinel.get_only, Z.get_only)
        with self.assertRaises(AttributeError):
            Z.get_only = 123

    def test_proper_metaclass(self):
        class Z(object):
            _get_set = sentinel.nothing

            @classproperty
            def get_only(cls):
                return sentinel.get_only

        with self.assertRaises(TypeError):
            self.assertEqual("should not resolve", Z.get_only)


if __name__ == "__main__":
    unittest.main()
