from coroutine import coroutine

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
def plusconst(send, key):
    while True:
        d = (yield)
        c = send[key]
        send(d + c)

def test_plus(capfd):
  p = plus(3) | plus(2) | printer()
  p.send(1)

  out, err = capfd.readouterr()
  assert out == "6\n"

def test_const(capfd):
  p = plus(3) | printer() | plusconst('const') | printer()
  p['const'] = 5
  p.send(2)

  out, err = capfd.readouterr()
  assert out == "5\n10\n"
