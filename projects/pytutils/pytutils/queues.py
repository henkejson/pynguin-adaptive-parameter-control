from six.moves.queue import Queue
from threading import Thread


def multiplex(q, count=2, queue_factory=lambda: Queue()):
    """ Convert one queue into several. Kind of like a teeing queue.

    >>> in_q = Queue()
    >>> q1, q2, q3 = multiplex(in_q, count=3)
    """
    out_queues = [queue_factory() for _ in range(count)]

    def f():
        while True:
            x = q.get()
            for out_q in out_queues:
                out_q.put(x)

    t = Thread(target=f)
    t.daemon = True
    t.start()
    return out_queues


def push(in_q, out_q):
    while True:
        x = in_q.get()
        out_q.put(x)


def merge(*in_qs, **kwargs):
    """ Merge multiple queues together

    >>> q1, q2, q3 = [Queue() for _ in range(3)]
    >>> out_q = merge(q1, q2, q3)
    """
    out_q = Queue(**kwargs)
    threads = [Thread(target=push, args=(q, out_q)) for q in in_qs]
    for t in threads:
        t.daemon = True
        t.start()
    return out_q
