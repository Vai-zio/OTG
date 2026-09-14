from fibonacci import fibit

# in terminal, "pytest test_fib.py"

def test_f0():
    assert fibit(0) == 0

def test_f1():
    assert fibit(1) == 1

def test_f2():
    assert fibit(2) == 1

def test_f3():
    assert fibit(3) == 2