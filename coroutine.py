#!/usr/bin/env python
from __future__ import division

import functools
try:
    # python 2
    from UserDict import IterableUserDict
except ImportError:
    from collections import UserDict as IterableUserDict


def coroutine(func):
    #@functools.wraps(func)
    class wrapper(IterableUserDict):
        def __init__(self, *args, **kwargs):
            super().__init__()
            self.target = None
            self.func = func
            self.data = dict()
            self.cr = self.func(self, *args, **kwargs)
            self.initialized = False
            functools.update_wrapper(self, func)

        def __or__(self, other):
            o = self._getLast()
            o.target = other
            self.ref(other)
            return self

        def ref(self, other):
            a = other
            while a is not None:
                a.data = self.data
                a = a.target

        def _getLast(self):
            o = self
            while o.target is not None:
                o = o.target
            return o

        # send to next target
        def __call__(self, *args, **kwargs):
            if self.target is not None:
                self.target.send(*args, **kwargs)

        def send(self, *args, **kwargs):
            if not self.initialized:
                next(self.cr)
                self.initialized = True
            if len(args) == 0:
                self.cr.send(None)
            else:
                self.cr.send(*args)

        def close(self):
            self.cr.close()

    return wrapper


# Example use
if __name__ == '__main__':

    @coroutine
    def printer(send):
        while True:
            s = (yield)
            print(s)
            send(s)

    @coroutine
    def plus(send, a):
        while True:
            v = (yield)
            send(v + a)

    @coroutine
    def plusconst(send, n):
        while True:
            d = (yield)
            c = send['const']
            send(d + c)

    p = plus(3) | plus(2) | printer()
    p.send(1)

    p = plus(3) | printer() | plusconst('const') | printer()
    p['const'] = 5

    p.send(2)
