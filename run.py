#! /usr/bin/env python3
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

from argparse import ArgumentParser
from datetime import datetime
from random import seed
from shutil import get_terminal_size
from time import sleep

from Color import Color, RandomColor


parser = ArgumentParser()

parser.add_argument('-a',
                    '--algorithm',
                    help='Algorithm to run',
                    choices=('random',
                             'brute',
                             'genetic1',
                             'genetic2',
                             'genetic3'),
                    type=str,
                    required=True)

parser.add_argument('-c',
                    '--color',
                    help='Color to find',
                    type=str)

parser.add_argument('-d',
                    '--delay',
                    help='Delay between each iteration',
                    type=float)

parser.add_argument('-f',
                    '--fitness',
                    help='\u0394E considered acceptable',
                    type=float,
                    default=1)

parser.add_argument('-i',
                    '--iterations',
                    help='Number of iterations',
                    type=int)

parser.add_argument('-p',
                    '--population-size',
                    help='Size of population at each iteration',
                    type=int)

parser.add_argument('-s',
                    '--seed',
                    help='Seed to initialize the random number generator',
                    type=int)

args = parser.parse_args()


columns, lines = get_terminal_size()

if not args.population_size:
    args.population_size = (columns // 5) - 1
    if args.population_size % 2 != 0:
        args.population_size -= 1

if args.population_size % 2 != 0:
    raise ValueError('Population must be a multiple of 2')

if args.seed:
    seed(args.seed)

if args.algorithm == 'random':
    from AlgoRandom import AlgoRandom as Algo
elif args.algorithm == 'brute':
    from AlgoBrute import AlgoBrute as Algo
elif args.algorithm == 'genetic1':
    from AlgoGenetic1 import AlgoGenetic1 as Algo
elif args.algorithm == 'genetic2':
    from AlgoGenetic2 import AlgoGenetic2 as Algo
elif args.algorithm == 'genetic3':
    from AlgoGenetic3 import AlgoGenetic3 as Algo
else:
    raise NotImplementedError('Unknown algorithm')


def dump(ref, algo, deltas):

    print('\033[90m{}\033[0m\n{} '.format('=' * columns, ref), end='')
    algo.dump()

    print(' \u0394E ', end='')
    for delta in deltas:
        if delta <= 1:     # Not perceptible by human eyes
            color = '92'
        elif delta <= 2:   # Perceptible through close observation
            color = '96'
        elif delta <= 5:   # More similar than different
            color = '93'
        elif delta <= 10:  # Perceptible at a glance
            color = '91'
        else:              # Not similar at all
            color = '90'
        print(' \033[{}m{:3.0f} \033[0m'.format(color, delta), end='')

    print('\n', flush=True)


def main():

    print('\033c', end='')

    ref = Color.from_rgb(args.color) if args.color else RandomColor()
    algo = Algo(args.population_size)

    n = 0
    ok = None
    start = datetime.now()
    while True:
        n += 1

        deltas = []
        for color in algo.population:
            delta = ref.delta_e(color)
            deltas.append(delta)
            if delta <= args.fitness:
                if ok is None or ok[1] > delta:
                    ok = (color, delta)

        dump(ref, algo, deltas)
        if ok:
            break
        if n == args.iterations:
            print('\033[1;31mFailed after {} iterations\033[0;0m'.format(n))
            exit(1)

        algo.tick(deltas)
        if args.delay:
            sleep(args.delay)

    stop = datetime.now()
    duration = (stop - start).total_seconds()
    color, delta = ok
    print('Color to find   : {} {}'.format(ref, ref.rgb))
    print('Color found     : {} {} (\u0394E = {:.3f})'.format(color,
                                                              color.rgb,
                                                              delta))
    print('Algorithm       : {}'.format(algo.__class__.__name__))
    print('Iterations      : {}'.format(n))
    print('Population size : {}'.format(args.population_size))
    print('Colors tested   : {}'.format(n * args.population_size))
    print('All that in     : {:.3f} seconds'.format(duration))


if __name__ == '__main__':
    main()
