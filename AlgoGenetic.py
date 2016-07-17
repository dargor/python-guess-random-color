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

from abc import abstractmethod
from random import randint, random, shuffle

from Algo import Algo, P


class AlgoGenetic(Algo):

    OPS = []

    MUTATION_PROBABILITY = 0.05

    @abstractmethod
    def crossover(self, G1, G2, op):
        pass

    def reproduce(self, mate_1, mate_2):

        def crossover(G1, G2):

            def mutation(gene):
                if random() <= self.MUTATION_PROBABILITY:
                    return randint(0, 255)
                return gene

            return mutation(self.crossover(mutation(G1),
                                           mutation(G2),
                                           self.OPS[0]))

        shuffle(self.OPS)
        return P(crossover(mate_1.red, mate_2.red),
                 crossover(mate_1.green, mate_2.green),
                 crossover(mate_1.blue, mate_2.blue),
                 None)

    def tick(self, deltas):

        parents = []
        for color, delta in zip(self.population, deltas):
            parents.append(P(color.red, color.green, color.blue, delta))
        parents = sorted(parents, key=lambda t: t.delta)
        alpha = parents[0]

        mates = []
        for position, parent in enumerate(parents):
            mating_possibilities = self.population_size - position
            while mating_possibilities > 0:
                mates.append(parent)
                mating_possibilities -= 1
        shuffle(mates)

        children = []
        n = len(mates) - 1
        while len(children) < self.population_size:
            parent_1 = mates[randint(0, n)]
            parent_2 = mates[randint(0, n)]
            child = self.reproduce(parent_1, parent_2)
            if child not in children:
                children.append(child)
        children.append(alpha)
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

        self.population = [c.color for c in children]
        assert len(self.population) == self.population_size
