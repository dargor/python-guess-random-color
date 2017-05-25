#! /usr/bin/env python3
#
# Copyright (c) 2017, Gabriel Linder <linder.gabriel@gmail.com>
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

from random import randint, random, randrange, shuffle
from statistics import mean
from time import sleep


GOAL = 'Bonjour, le monde !'
CHROMOSOME_SIZE = len(GOAL)

POPULATION_SIZE = 73
MUTATION_PROBABILITY = 0.05


def random_gene():
    return chr(randint(0, 255))


def random_chromosome():
    return ''.join([random_gene() for _ in range(CHROMOSOME_SIZE)])


def random_population():
    return [random_chromosome() for _ in range(POPULATION_SIZE)]


def square_error(a, b):
    return (ord(a) - ord(b)) ** 2


def mean_square_error(chromosome):
    return mean([square_error(a, b) for a, b in zip(chromosome, GOAL)])


def print_population():
    scores = []
    print('\033[1;37m>>> Population at epoch {}\033[0;0m'.format(epoch))
    for p in population:
        score = mean_square_error(p)
        print('\033[{}m{}{: 18.5f}\033[0;0m'.format(
            '1;32' if score == 0 else '0;0',
            ''.join([c if c.isprintable() else '▒' for c in p]),
            score))
        scores.append(score)
    return scores


def mute(gene):
    def _mute(c):
        c = ord(c)
        n = random()
        if n <= 0.3:
            c += 1
            if c > 255:
                c = 0
        elif n <= 0.6:
            c -= 1
            if c < 0:
                c = 255
        else:
            return random_gene()
        return chr(c)
    if random() <= MUTATION_PROBABILITY:
        i = randrange(0, len(gene))
        gene = list(gene)
        gene[i] = _mute(gene[i])
        gene = ''.join(gene)
    return gene


def mate(a, b):
    n = randrange(1, CHROMOSOME_SIZE - 1)
    a1, a2 = a[:n], a[n:]
    b1, b2 = b[:n], b[n:]
    return mute(mute(a1) + mute(b2)), mute(mute(b1) + mute(a2))


epoch = 0
population = random_population()

scores = print_population()
best_score = min(scores)
while best_score != 0:
    epoch += 1

    p = [x for x, _ in sorted(zip(population, scores), key=lambda x: x[1])]
    alpha = p[0]

    mates = []
    for position, parent in enumerate(p):
        mating_possibilities = POPULATION_SIZE - position
        mates.extend([parent for _ in range(mating_possibilities)])
    shuffle(mates)

    children = [alpha]
    n = len(mates) - 1
    while len(children) < POPULATION_SIZE:
        parent_1 = mates[randint(0, n)]
        parent_2 = mates[randint(0, n)]
        for child in mate(parent_1, parent_2):
            if child not in children:
                children.append(child)
    population = children[:POPULATION_SIZE]
    scores = print_population()
    best_score = min(scores)

    sleep(0.1)
