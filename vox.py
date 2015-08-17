"""
Vox
---
Enzo Calamia, 2015
"""

import sys
from random import randint
from functools import reduce, partial
from collections import namedtuple
import statistics as stat

MAX_INT = 2**64-1

R = namedtuple('R', 'val')
I = namedtuple('I', 'val')
S = namedtuple('S', 'val')
V = namedtuple('V', 'val')
BinOp = namedtuple('BinOp', 'val')
Op = namedtuple('Op', 'val')

class Err(Exception):
    pass

def add_(x, y):
    if isinstance(x, I):
        x, y = x.val, y.val
        return I(x + y)
    if isinstance(x, V):
        x, y = x.val, y.val
        w = map(lambda t: add_(t[0], t[1]), zip(x, y))
        return V(list(w))
    #raise Err('Type error')

def sum_(v):
    v = v.val
    sigma = sum(i.val for i in v)
    return I(sigma)

def mean_(v):
    v = v.val
    mean = stat.mean(i.val for i in v)
    return R(mean)

def stdev_(v):
    v = v.val
    avg = stat.stdev(i.val for i in v)
    return R(avg)

def cov_(X, Y):
    X = [x.val for x in X.val]
    Y = [y.val for y in Y.val]
    Ex = stat.mean(X)
    Ey = stat.mean(Y)
    cov = sum((x-Ex)*(y-Ey) for x,y in zip(X,Y)) / (len(X)-1) 
    return R(cov)
    
    cov = stat.mean(x*y for x,y in zip(X, Y))
    cov -= stat.mean(X) * stat.mean(Y)
    return R(cov)

def beta_(X, Y):
    cov = cov_(X, Y)
    var = cov_(Y, Y)
    cov = cov.val
    var = var.val
    return R(cov/var)


def len_(v):
    v = v.val
    l = len(v)
    return I(l)


binop_table = {
    '+': add_,
    'cov': cov_,
    'beta': beta_
}

op_table = {
    'sum': sum_,
    'len': len_,
    'mean': mean_,
    'stdev': stdev_,
    'var': lambda x: cov_(x, x)
}

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
        elif x in binop_table.keys():
            yield BinOp(x)
        elif x in op_table.keys():
            yield Op(x)
        else:
            yield S(x)

def eval_ast(ast):
    def eval_units(u1, u2):
        if isinstance(u2, BinOp):
            binop = binop_table[u2.val]
            return partial(binop, u1)
        if isinstance(u2, Op):
            op = op_table[u2.val]
            return op(u1)
        if hasattr(u1, '__call__'):
            return u1(u2)
        raise Err('Semantic error')
    
    return reduce(eval_units, ast)

#program = '(0 20) stdev'
#iprogram = (program.replace('(', ' ( ').replace(')', ' ) ').split())
#parsed = list(parse(iprogram))

#print(parsed)
#print(eval_ast(parsed))

if __name__ == '__main__':
    try:
        while True:
            inp = input('Vox> ')
            program = (inp.replace('(', ' ( ').replace(')', ' ) ').split())
            ast = parse(program)
            res = eval_ast(ast)
            print(res)
    except EOFError:
        print()
        sys.exit(0)
