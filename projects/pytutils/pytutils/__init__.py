"""
Random utilities that I should stop copying across project boundaries, hence this exists.

~trevorj https://github.com/akatrevorjay/pytutils
"""

# import demandimport; demandimport.enable()


# import importlib
# import sys

# _sentinel = object()


# class _Sneaky(object):
#     __lazy_init_method = '__lazy_module_init__'
#     __loaded = False

#     def __lazy_init(self):
#         if self.__loaded:
#             return

#         fallback = lambda: None

#         if self.__lazy_init_method:
#             meth = getattr(self.__module, self.__lazy_init_method, fallback)

#         try:
#             return meth()
#         finally:
#             self.__loaded = True

#     def __init__(self, name, call_lazy_module_init=True):
#         self.__name = name

#         self.__eat_module()

#     def __eat_module(self, container=sys.modules):
#         """Replaces the module we're lazily loading with myself."""
#         self.__module = container[self.__name]
#         container[self.__name] = self

#     def __puke_module(self, mod, container=sys.modules):
#         container[self.__name] = mod

#     def __load(self, name):
#         mod = importlib.import_module(self.__name)
#         # mod = importlib.import_module(name, package=self.__module.__name__)

#         self.__puke_module(mod)

#         self.__lazy_init()

#     def __getattr__(self, name):
#         if not self.__loaded and not name[:2] == '__' == name[-2:]:
#             self.__load(name)

#         return getattr(self.module, name)

# _Sneaky(__name__)





