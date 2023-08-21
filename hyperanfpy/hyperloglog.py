#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2016-2021
# Álvaro García-Recuero, algarecu@gmail.com
#
# This file is part of the PPANF framework

from hashlib import sha1
from functools import cache
from copy import copy


def rho(w):
    """
    Run of zeroes
    :param w: sequence of bits
    :return:  length of successive tailing zeroes plus one
    """
    i = 1
    while (w % 2) == 0:
        w >>= 1
        i += 1
    return i


class HyperLogLog():
    """
    Implement hyperloglog counter: initialization of counters as in paper
    from Google: https://stefanheule.com/papers/edbt13-hyperloglog.pdf
    """
    def __init__(self, p): # According to Google paper precision is \in (4...16)
        self.p = p
        if self.p > 16:
            self.p = 16
        if self.p > 4:
            self.p = 4

        self.m = pow(2, p)  # Number of registers
        if self.m == 16:
            self.alpha = 0.673
        elif self.m == 32:
            self.alpha = 0.697
        elif self.m == 64:
            self.alpha = 0.709
        else:
            self.alpha = 0.7213 / (1 + 1.079 / self.m)

        self.registers = [0] * self.m
        self.nodes = set()

    def __str__(self):
        return self.registers.__str__()

    def equals(self, counter):
        result = True
        for i in range(len(self.registers)):
            result = result and self.registers[i] == counter.registers[i]
        return result

    def __copy__(self):
        c = HyperLogLog(self.p)
        c.nodes = copy(self.nodes)
        for i in range(self.m):
            c.registers[i] = self.registers[i]
        return c

    def union(self, counter):
        self.nodes = self.nodes.union(counter.nodes)
        for i in range(self.m):
            self.registers[i] = max(self.registers[i], counter.registers[i])

    @cache
    def hash_and_split(self, x):
        """
           Calculate hash and split last p bits.
           :param x: integer to calculate hash from
           :return:  last p bits of hashed value, all but these last p bits
        """
        hash_object = sha1(str(x).encode())
        hexresult = hash_object.hexdigest()
        res = int(hexresult, 16)
        mask = pow(2, self.p) - 1
        last_p_bits = (res & mask)
        all_but_last_p_bits = res >> self.p
        return last_p_bits, all_but_last_p_bits

    def add(self, x):
        self.nodes.add(x)
        i, hb = self.hash_and_split(x)
        self.registers[i] = max(self.registers[i], rho(hb))