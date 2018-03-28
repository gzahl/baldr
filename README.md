# Baldr - Python pipes for data analysis inspired by unix pipes

Inspired by the exellent talks of [David Beazley](http://www.dabeaz.com/coroutines/) about coroutines, i implemented coroutines with the '|' pipe operator to build data analysis pipelines. Additionally to the pipe data, each pipe has its own key-value store to share a state between the pipe building blocks.

We use this to do data analysis directly on the console and building complicated plots from prewritten coroutine, which can prototyped and combined in unlimited ways. If a plot is done, the pipe can be saved in a larger script or workflow engine for later reuse.

## Examples

```
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
```

## FAQ

- Baldr is a god in [Norse mythology](https://en.wikipedia.org/wiki/Baldr) and the father of [Fosite](https://en.wikipedia.org/wiki/Forseti). Baldr was originally developed for use in [Fosite](http://portia.astrophysik.uni-kiel.de/fosite/) - an astrophysical fluid dynamic code from Kiel University.
