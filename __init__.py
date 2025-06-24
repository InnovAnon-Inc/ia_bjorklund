#! /usr/bin/env python
# cython: language_level=3
# distutils: language=c++

from typing      import Iterable

from bitarray    import bitarray

from ia_bits     import pack_bitstring, rotate
from ia_coprimes import coprimes
from ia_gcd      import egcd2

def build(pattern:bitarray, level:int, remainders:Iterable[int], counts:Iterable[int])->None:
    if level == -1:
        pattern.append(0)
        return

    if level == -2:
        pattern.append(1)
        return

    for i in range(0, counts[level]):
        build(pattern, level - 1, remainders, counts)

    if remainders[level] != 0:
        build(pattern, level - 2, remainders, counts)

def bjorklund(steps:int, pulses:int)->bitarray:
    if pulses > steps:
        raise ValueError
    d, level           = egcd2(steps - pulses, pulses)
    d                  = zip(*d)
    #pattern            = []
    pattern            = bitarray()
    build(pattern, level, *d)
    i                  = pattern.index(1)
    pattern            = rotate(pattern, i)
    return pattern

def bjorklund_generator():
    for a, b in coprimes():
        c = bjorklund(a, b)
        logger.info('bjorklund generator: %s/%s: %s', a, b, c)
        yield c

if __name__ == '__main__':
    for a, b in coprimes():
        c = bjorklund(a, b)
        d = pack_bitstring(c, a)
        print(a, b, d)

__author__:str = 'InnovAnon, Inc.' # NOQA
