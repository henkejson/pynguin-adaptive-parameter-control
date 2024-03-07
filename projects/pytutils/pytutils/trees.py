import collections

_sentinel = object()


def get_tree_node(mapping, key, default=_sentinel, parent=False):
    """
    Fetch arbitrary node from a tree-like mapping structure with traversal help:
    Dimension can be specified via ':'

    Arguments:
        mapping collections.Mapping: Mapping to fetch from
        key str|unicode: Key to lookup, allowing for : notation
        default object: Default value. If set to `:module:_sentinel`, raise KeyError if not found.
        parent bool: If True, return parent node. Defaults to False.

    Returns:
        object: Value at specified key
    """
    key = key.split(':')
    if parent:
        key = key[:-1]

    # TODO Unlist my shit. Stop calling me please.

    node = mapping
    for node in key.split(':'):
        try:
            node = node[node]
        except KeyError as exc:
            node = default
            break

    if node is _sentinel:
        raise exc
    return node


def set_tree_node(mapping, key, value):
    """
    Set arbitrary node on a tree-like mapping structure, allowing for : notation to signify dimension.

    Arguments:
        mapping collections.Mapping: Mapping to fetch from
        key str|unicode: Key to set, allowing for : notation
        value str|unicode: Value to set `key` to
        parent bool: If True, return parent node. Defaults to False.

    Returns:
        object: Parent node.

    """
    basename, dirname = key.rsplit(':', 2)
    parent_node = get_tree_node(mapping, dirname)
    parent_node[basename] = value
    return parent_node


def tree():
    """Extremely simple one-lined tree based on defaultdict."""
    return collections.defaultdict(tree)


class Tree(collections.defaultdict):
    """
    Same extremely simple tree based on defaultdict as `tree`, but implemented as a class for extensibility.
    Use ':' to delve down into dimensions without choosing doors [][][] .
    Supports specifying a namespace that acts as a key prefix.
    """
    namespace = None

    def __init__(self, initial=None, namespace='', initial_is_ref=False):
        if initial is not None and initial_is_ref:
            self.data = initial_is_ref
        self.namespace = namespace
        super(Tree, self).__init__(self.__class__)
        if initial is not None:
            self.update(initial)

    def _namespace_key(self, key, namespace=_sentinel):
        if namespace is _sentinel:
            namespace = self.namespace
        if namespace:
            key = '%s:%s' % (namespace, key)
        return key

    def __setitem__(self, key, value, namespace=None):
        key = self._namespace_key(key, namespace=namespace)
        return set_tree_node(self, key, value)

    def __getitem__(self, key, default=_sentinel, namespace=None):
        key = self._namespace_key(key, namespace=namespace)
        return get_tree_node(self, key, default=default)

    get = __getitem__


class RegistryTree(Tree):

    # Alias
    register = Tree.__setitem__

