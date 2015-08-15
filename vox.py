#
#
#  vox.py
#  ------
#
#

from random import randint
from functools import reduce, partial
from operator import add
from collections import namedtuple

MAX_INT = 2**64-1


I = namedtuple('I', 'val')
S = namedtuple('S', 'val')
V = namedtuple('V', 'val')

def iadd(n, m):
    n = n.val
    m = m.val
    p = n + m
    return I(p)

def vadd(u, v):
    u = u.val
    v = v.val
    w = map(lambda t: iadd(t[0], t[1]), zip(u, v))
    return V(list(w))

def parse(xs):
    xs = iter(xs)
    while True:
        x = next(xs)
        if x.isdigit():
            yield I(int(x))
        elif x == '(':
            yield V(list(parse(xs)))
        elif x == ')':
            return
        elif x == '?':
            yield I(randint(0, MAX_INT))
        else:
            yield S(x)

def eval_ast(ast):
    def eval_units(u1, u2):
        if isinstance(u2, S):
            if isinstance(u1, I):
                return partial(iadd, u1)
            if isinstance(u1, V):
                return partial(vadd, u1)
        if hasattr(u1, '__call__'):
            return u1(u2)
    
    return reduce(eval_units, ast)

program = '(1 2 3) + (8 4 3) + (2 3 3)'
iprogram = (program.replace('(', ' ( ').replace(')', ' ) ').split())
parsed = list(parse(iprogram))

#print(parsed)
print(list(eval_ast(parsed)))