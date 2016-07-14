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

from collections import namedtuple
from random import randint, random

from Algo import Algo
from Color import Color


P = namedtuple('P', ['red', 'green', 'blue', 'delta'])


class AlgoGenetic2(Algo):

    MUTATION_PROBABILITY = 0.4

    def tick(self, deltas):

        def crossover(mate_1, mate_2):

            def reproduce(G1, G2, version):

                def alleles(gene):
                    a1 = (gene & 0xf0) >> 4
                    a2 = gene & 0x0f
                    return a1, a2

                G1A1, G1A2 = alleles(G1)
                G2A1, G2A2 = alleles(G2)

                if version == 1:
                    return (G1A1 << 4) | G2A2
                elif version == 2:
                    return (G2A1 << 4) | G1A2
                else:
                    raise NotImplementedError('Unknown version')

            def reproduce1(G1, G2):
                return reproduce(G1, G2, 1)

            def reproduce2(G1, G2):
                return reproduce(G1, G2, 2)

            def mutation(n):
                if random() <= self.MUTATION_PROBABILITY:
                    return randint(0, 255)
                return n

            l = []
            for op in (reproduce1, reproduce2):
                l.append(P(mutation(op(mate_1.red, mate_2.red)),
                           mutation(op(mate_1.green, mate_2.green)),
                           mutation(op(mate_1.blue, mate_2.blue)),
                           None))
            return l

        def survival():
            l = []
            for child in children:
                delta = alpha.delta_e(child)
                if delta not in [x.delta for x in l]:
                    l.append(P(child.red, child.green, child.blue, delta))
            l = sorted(l, key=lambda t: t.delta)[:self.population_size]
            return [Color(c.red, c.green, c.blue) for c in l]

        parents = []
        for color, delta in zip(self.population, deltas):
            parents.append(P(color.red, color.green, color.blue, delta))
        parents = sorted(parents, key=lambda t: t.delta)
        alpha = Color(parents[0].red, parents[0].green, parents[0].blue)

        children = []
        for parent in parents:
            for child in crossover(alpha, parent):
                children.append(Color(child.red, child.green, child.blue))

        self.population = survival()
        assert len(self.population) == self.population_size
