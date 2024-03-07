import wrapt
import collections
import itertools
import operator


def accumulate(iterable, func=operator.add):
    """
    Iterate over running totals, ie [a,b,c,d] -> func( func( func(a, b), c), d) with each func result yielded.
    Func is operator.add by default.

    >>> list(accumulate([1,2,3,4,5]))
    [1, 3, 6, 10, 15]
    >>> list(accumulate([1,2,3,4,5], operator.mul))
    [1, 2, 6, 24, 120]

    :param iterable: Iterable
    :param func: method (default=operator.add) to call for each pair of (last call result or first item, next item)
    :return generator: Generator
    """
    it = iter(iterable)
    try:
        total = next(it)
    except StopIteration:
        return
    yield total
    for element in it:
        total = func(total, element)
        yield total


def consume(iterator, n=None):
    """
    Efficiently advance an iterator n-steps ahead. If n is none, consume entirely.
    Consumes at C level (and therefore speed) in cpython.
    """
    if n is None:
        # feed the entire iterator into a zero-length deque
        collections.deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(itertools.islice(iterator, n, n), None)


def dedupe_iter(iterator, hashfunc=hash):
    """"
    Deduplicates an iterator iteratively using hashed values in a set.
    Not exactly memory efficient because of that of course.
    If you have a large dataset with high cardinality look at HyperLogLog instead.

    :return generator: Iterator of deduplicated results.
    """
    done = set()
    for item in iterator:
        hashed = hashfunc(item)

        if hashed in done:
            continue

        done.add(hashed)
        yield item


@wrapt.decorator
def dedupe(f, instance, args, kwargs):
    """
    Decorator to dedupe it's output iterable automatically.

    :param f: Wrapped meth
    :param instance: wrapt provided property for decorating hydrated class instances (unused)
    :param args: Passthrough args
    :param kwargs: Passthrough kwargs
    :return decorator: Decorator method that ingests iterables and dedupes them iteratively.
    """
    gen = f(*args, **kwargs)
    return dedupe_iter(gen)
