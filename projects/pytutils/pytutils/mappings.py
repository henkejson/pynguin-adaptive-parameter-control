import collections
import os
import re

import six

from .props import classproperty


class AttrDict(dict):
    """
    >>> m = AttrDict(omg=True, whoa='yes')
    """

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


Messenger = AttrDict


class ProxyMutableMapping(collections.MutableMapping):
    """
    Proxies access to an existing dict-like object.

    >>> a = dict(whoa=True, hello=[1,2,3], why='always')
    >>> b = ProxyMutableAttrDict(a)

    Nice reprs:

    >>> b
    <ProxyMutableAttrDict {'whoa': True, 'hello': [1, 2, 3], 'why': 'always'}>

    Setting works as you'd expect:

    >>> b['nice'] = False
    >>> b['whoa'] = 'yeee'
    >>> b
    <ProxyMutableAttrDict {'whoa': 'yeee', 'hello': [1, 2, 3], 'why': 'always', 'nice': False}>

    Checking that the changes are in fact being performed on the proxied object:

    >>> a
    {'whoa': 'yeee', 'hello': [1, 2, 3], 'why': 'always', 'nice': False}

    """

    def __init__(self, mapping, fancy_repr=True, dictify_repr=False):
        """
        :param collections.MutableMapping mapping: Dict-like object to wrap
        :param bool fancy_repr: If True, show fancy repr, otherwise just show dict's
        :param bool dictify_repr: If True, cast mapping to a dict on repr
        """
        self.__fancy_repr = fancy_repr
        self.__dictify_repr = dictify_repr

        self._set_mapping(mapping)

    def __repr__(self):
        if not self.__fancy_repr:
            return '%s' % dict(self)

        mapping = self.__mapping
        if self.__dictify_repr:
            mapping = dict(mapping)

        return '<%s %s>' % (self.__class__.__name__, mapping)

    def _set_mapping(self, mapping):
        self.__mapping = mapping

    def __contains__(self, item):
        return item in self.__mapping

    def __getitem__(self, item):
        return self.__mapping[item]

    def __setitem__(self, key, value):
        self.__mapping[key] = value

    def __delitem__(self, key):
        del self.__mapping[key]

    def __iter__(self):
        return iter(self.__mapping)

    def __len__(self):
        return len(self.__mapping)


class HookableProxyMutableMapping(ProxyMutableMapping):
    def __init__(self, mapping, fancy_repr=True, dictify_repr=False):
        self.__mapping = mapping

        super(HookableProxyMutableMapping, self).__init__(mapping, fancy_repr=fancy_repr, dictify_repr=dictify_repr)

    def __key_trans__(self, key, store=False, get=False, contains=False, delete=False):
        return key

    def __key_allowed__(self, key):
        return True

    def __iter__(self):
        orig_iter = super(HookableProxyMutableMapping, self).__iter__()
        return (self.__key_remove_prefix__(key) for key in orig_iter if self.__key_allowed__(key))

    def __contains__(self, item):
        item = self.__key_trans__(item, contains=True)
        return super(HookableProxyMutableMapping, self).__contains__(item)

    def __getitem__(self, item):
        item = self.__key_trans__(item, get=True)
        return super(HookableProxyMutableMapping, self).__getitem__(item)

    def __setitem__(self, item, value):
        item = self.__key_trans__(item, store=True)
        return super(HookableProxyMutableMapping, self).__setitem__(item, value)

    def __delitem__(self, item):
        item = self.__key_trans__(item, delete=True)
        return super(HookableProxyMutableMapping, self).__delitem__(item)


class PrefixedProxyMutableMapping(HookableProxyMutableMapping):
    def __init__(self, prefix, mapping, only_prefixed=True, fancy_repr=True, dictify_repr=False):
        """
        :param str prefix: Prefix to add/remove from keys.
        :param collections.MutableMapping mapping: Dict-like object to wrap
        :param bool fancy_repr: If True, show fancy repr, otherwise just show dict's
        :param bool dictify_repr: If True, cast mapping to a dict on repr
        """
        self.__prefix = prefix
        self.__prefix_len = len(prefix)
        self.__only_prefixed = only_prefixed

        super(PrefixedProxyMutableMapping, self).__init__(
            mapping,
            fancy_repr=fancy_repr,
            dictify_repr=dictify_repr,
        )

    def __key_trans__(self, key, store=False, get=False, contains=False, delete=False):
        if store:
            return self.__key_remove_prefix__(key)
        return self.__key_add_prefix__(key)

    def __key_allowed__(self, key):
        if self.__only_prefixed:
            if isinstance(key, six.string_types):
                if not key.startswith(self.__prefix):
                    return False
            else:
                return False
        return True

    def __key_add_prefix__(self, key):
        return self.__prefix + key

    def __key_remove_prefix__(self, key):
        return key[self.__prefix_len:]


class MultiDict(collections.OrderedDict):
    """Simple multi-value ordered dict."""
    _unique = 0

    def __setitem__(self, key, val):
        if isinstance(val, dict) and key in self:
            self._unique += 1
            key += str(self._unique)
        dict.__setitem__(self, key, val)


multidict = MultiDict


def format_dict_recursively(
        mapping, raise_unresolvable=True, strip_unresolvable=False, conversions={
            'True': True,
            'False': False
        }
):
    """Format each string value of dictionary using values contained within
    itself, keeping track of dependencies as required.

    Also converts any formatted values according to conversions dict.

    Example:

    >>> from pprint import pprint as pp
    >>> c = dict(wat='wat{omg}', omg=True)
    >>> pp(format_dict_recursively(c))
    {'omg': True, 'wat': 'watTrue'}

    Dealing with missing (unresolvable) keys in format strings:

    >>> from pprint import pprint as pp
    >>> c = dict(wat='wat{omg}', omg=True, fail='no{whale}')
    >>> format_dict_recursively(c)
    Traceback (most recent call last):
        ...
    ValueError: Impossible to format dict due to missing elements: {'fail': ['whale']}
    >>> pp(format_dict_recursively(c, raise_unresolvable=False))
    {'fail': 'no{whale}', 'omg': True, 'wat': 'watTrue'}
    >>> pp(format_dict_recursively(c, raise_unresolvable=False, strip_unresolvable=True))
    {'omg': True, 'wat': 'watTrue'}

    :param dict mapping: Dict.
    :param bool raise_unresolvable: Upon True, raises ValueError upon an unresolvable key.
    :param bool strip_unresolvable: Upon True, strips unresolvable keys.
    :param dict conversions: Mapping of {from: to}.
    """
    if conversions is None:
        conversions = {}

    ret = {}

    # Create dependency mapping
    deps = {}
    for k, v in mapping.items():
        # Do not include multiline values in this to avoid KeyErrors on actual
        # .format below
        if isinstance(v, six.string_types) and '\n' not in v:
            # Map key -> [*deps]
            # This is a bit naive, but it works well.
            deps[k] = re.findall(r'\{(\w+)\}', v)
        else:
            ret[k] = v

    while len(ret) != len(mapping):
        ret_key_count_at_start = len(ret)
        sret = set(ret)
        keys = set(mapping) - sret

        for k in keys:
            needed = (x not in ret for x in deps[k])
            if any(needed):
                continue

            ret[k] = mapping[k].format(**ret)

            if ret[k] in conversions:
                ret[k] = conversions[ret[k]]

        # We have done all that we can here.
        if ret_key_count_at_start == len(ret):
            if not raise_unresolvable:
                if not strip_unresolvable:
                    # backfill
                    ret.update({k: mapping[k] for k in keys})
                break

            missing = {k: [x for x in deps[k] if x not in ret]}
            raise ValueError('Impossible to format dict due to missing elements: %r' % missing)

    return ret


class ProxyMutableAttrDict(ProxyMutableMapping):
    """
    Proxies mutable access to another mapping and allows for attribute-style access.

    >>> a = dict(whoa=True, hello=[1,2,3], why='always')
    >>> b = ProxyMutableAttrDict(a)

    Nice reprs:

    >>> b
    <ProxyMutableAttrDict {'whoa': True, 'hello': [1, 2, 3], 'why': 'always'}>

    Setting works as you'd expect:

    >>> b['nice'] = False
    >>> b['whoa'] = 'yeee'
    >>> b
    <ProxyMutableAttrDict {'whoa': 'yeee', 'hello': [1, 2, 3], 'why': 'always', 'nice': False}>

    Checking that the changes are in fact being performed on the proxied object:

    >>> a
    {'whoa': 'yeee', 'hello': [1, 2, 3], 'why': 'always', 'nice': False}

    Attribute style access:

    >>> b.whoa
    'yeee'
    >>> b.state = 'new'
    >>> b
    <ProxyMutableAttrDict {'whoa': 'yeee', 'hello': [1, 2, 3], 'why': 'always', 'nice': False, 'state': 'new'}>

    Recursion is handled:

    >>> b.subdict = dict(test=True)
    >>> b.subdict.test
    True
    >>> b
    <ProxyMutableAttrDict {'whoa': 'yeee', 'hello': [1, 2, 3], 'why': 'always', 'nice': False, 'state': 'new',
    'subdict': <ProxyMutableAttrDict {'test': True}>}>

    """

    def __init__(self, mapping, fancy_repr=True, dictify_repr=False, recursion=True):
        self.__recursion = recursion
        self.__mapping = mapping

        super(ProxyMutableAttrDict, self).__init__(mapping, fancy_repr=fancy_repr, dictify_repr=dictify_repr)

    @classproperty
    def _wrap_as(cls):
        return cls

    def __getattr__(self, key):
        if not key.startswith('_'):
            try:
                value = self.__mapping[key]

                if self.__recursion and isinstance(value, collections.Mapping) and not isinstance(value, self._wrap_as):
                    value = self.__class__(value)

                return value
            except KeyError:
                # in py3 I'd chain these
                raise AttributeError(key)

    def __setattr__(self, key, value):
        if not key.startswith('_'):
            if self.__recursion and isinstance(value, collections.Mapping) and not isinstance(value, self._wrap_as):
                value = self.__class__(value)

            try:
                self[key] = value
            except KeyError:
                # in py3 I'd chain these
                raise AttributeError(key)

        return super(ProxyMutableAttrDict, self).__setattr__(key, value)


RecursiveProxyAttrDict = ProxyMutableAttrDict


class ProcessLocal(HookableProxyMutableMapping):
    """
    Provides a basic per-process mapping container that wipes itself if the current PID changed since the last get/set.

    Aka `threading.local()`, but for processes instead of threads.

    >>> plocal = ProcessLocal()
    >>> plocal['test'] = True
    >>> plocal['test']
    True
    >>> plocal._handle_pid(new_pid=-1)  # Emulate a PID change by forcing it to be something invalid.
    >>> plocal['test']                  # Mapping wipes itself since PID is different than what's stored.
    Traceback (most recent call last):
        ...
    KeyError: ...

    """

    __pid__ = -1

    def __init__(self, mapping_factory=dict):
        self.__mapping_factory = mapping_factory

        self._handle_pid()

        super(ProcessLocal, self).__init__(
            self.__mapping,
            fancy_repr=True,
            dictify_repr=False,
        )

    def __key_trans__(self, key, store=False, get=False, contains=False, delete=False):
        self._handle_pid()
        return key

    def _handle_pid(self, new_pid=os.getpid):
        if callable(new_pid):
            new_pid = new_pid()

        if self.__pid__ != new_pid:
            self.__pid__, self.__mapping = new_pid, self.__mapping_factory()
            self._set_mapping(self.__mapping)


class LastUpdatedOrderedDict(collections.OrderedDict):
    """
    Stores items in the order the keys were last added.

    From Python stdlib in `collections`.
    """

    def __setitem__(self, key, value):
        if key in self:
            del self[key]

        return collections.OrderedDict.__setitem__(self, key, value)


class OrderedCounter(collections.Counter, collections.OrderedDict):
    """
    An ordered dictionary can be combined with the Counter class so that the counter remembers the order elements are
    first encountered.

    From Python stdlib in `collections`.
    """

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, collections.OrderedDict(self))

    def __reduce__(self):
        return self.__class__, (collections.OrderedDict(self), )
