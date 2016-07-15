#
# Copyright (c) 2016, Gabriel Linder <linder.gabriel@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#

from random import randint, random, shuffle

from Algo import Algo
from Color import Color


class P:

    __slots__ = ('red', 'green', 'blue', 'delta')

    def __init__(self, red, green, blue, delta):

        assert 0 <= red <= 255
        self.red = red

        assert 0 <= green <= 255
        self.green = green

        assert 0 <= blue <= 255
        self.blue = blue

        self.delta = delta

    @property
    def rgb(self):
        return self.red << 12 | self.green << 8 | self.blue


class AlgoGenetic(Algo):

    MUTATION_PROBABILITY = 0.05

    def tick(self, deltas):

        def crossover(mate_1, mate_2):

            def combine(G1, G2):
                return G1 & G2

            def brass(G1, G2):
                return G1 | G2

            def cross(G1, G2):
                return G1 ^ G2

            def mix(G1, G2):
                return (G1 + G2) // 2

            def mutation(n):
                if random() <= self.MUTATION_PROBABILITY:
                    return randint(0, 255)
                return n

            ops = [combine, brass, cross, mix]
            shuffle(ops)
            l = []
            for op in ops:
                l.append(P(mutation(op(mate_1.red, mate_2.red)),
                           mutation(op(mate_1.green, mate_2.green)),
                           mutation(op(mate_1.blue, mate_2.blue)),
                           None))
            return l

        parents = []
        for color, delta in zip(self.population, deltas):
            parents.append(P(color.red, color.green, color.blue, delta))
        parents = sorted(parents, key=lambda t: t.delta)
        alpha = parents[0]

        mates = []
        n = sum([t.delta for t in parents])
        for parent in parents:
            delta = parent.delta
            mating_possibilities = n / parent.delta
            while mating_possibilities > 0:
                mates.append(parent)
                mating_possibilities -= 1
        shuffle(mates)

        children = [alpha]
        n = len(mates) - 1
        while len(children) < self.population_size:
            parent_1 = mates[randint(0, n)]
            parent_2 = mates[randint(0, n)]
            for child in crossover(parent_1, parent_2):
                if child not in children:
                    children.append(child)
        children = sorted(children, key=lambda t: t.rgb)

        n = children.index(alpha)
        a = n - self.half_population_size
        b = n + self.half_population_size
        if a < 0:
            a = 0
            b = self.population_size
        n = len(children)
        if b > n:
            b = n
            a = n - self.population_size
        children = children[a:b]

        self.population = [Color(c.red, c.green, c.blue) for c in children]
        assert len(self.population) == self.population_size
