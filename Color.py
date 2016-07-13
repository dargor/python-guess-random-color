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

from random import randint

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000


class Color:

    def __init__(self, red, green, blue):

        assert 0 <= red <= 255
        self.red = red

        assert 0 <= green <= 255
        self.green = green

        assert 0 <= blue <= 255
        self.blue = blue

        self.Lab = convert_color(sRGBColor(self.red,
                                           self.green,
                                           self.blue,
                                           is_upscaled=True),
                                 LabColor,
                                 target_illuminant='d50')

    def delta_e(self, color):
        return delta_e_cie2000(self.Lab, color.Lab)

    @property
    def rgb(self):
        return '#{:02X}{:02X}{:02X}'.format(self.red,
                                            self.green,
                                            self.blue)

    def __str__(self):
        return '\033[38;2;{};{};{}m{}\033[0m'.format(self.red,
                                                     self.green,
                                                     self.blue,
                                                     '\u2588' * 4)


class RandomColor(Color):

    def __init__(self):

        red = randint(0, 255)
        green = randint(0, 255)
        blue = randint(0, 255)

        super().__init__(red, green, blue)
