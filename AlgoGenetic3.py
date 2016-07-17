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

from AlgoGenetic1 import AlgoGenetic1
from AlgoGenetic2 import AlgoGenetic2


class AlgoGenetic3(AlgoGenetic1, AlgoGenetic2):

    OPS = AlgoGenetic1.OPS + AlgoGenetic2.OPS

    def crossover(self, G1, G2, op):
        if op in AlgoGenetic1.OPS:
            return AlgoGenetic1.crossover(self, G1, G2, op)
        elif op in AlgoGenetic2.OPS:
            return AlgoGenetic2.crossover(self, G1, G2, op)
        else:
            raise ValueError('Unknown op')
