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

from abc import ABC, abstractmethod

from Color import RandomColor


class Algo(ABC):

    def __init__(self, population_size):

        assert population_size % 2 == 0

        self.half_population_size = population_size // 2
        self.population_size = population_size

        self.set_random_population()

    def set_random_population(self):
        self.population = []
        for i in range(self.population_size):
            self.population.append(RandomColor())

    def dump(self):
        for color in self.population:
            print('{} '.format(color), end='')
        print(flush=True)

    @abstractmethod
    def tick(self, deltas):
        pass
