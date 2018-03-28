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
            super(IterableUserDict).__init__()
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
