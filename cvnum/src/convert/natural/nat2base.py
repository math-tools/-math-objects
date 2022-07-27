#!/usr/bin/env python3

###
# This module converts different kinds of decimal writings of naturals
# into different kinds of "base" writings.
###


from typing import *

from string import digits as STR_DIGITS
from .natconv import NatConv

from math import (
    ceil,
    log
)


# ----------------------------------------- #
# -- NATURAL: DECIMAL ~~~> SPECIFIC BASE -- #
# ----------------------------------------- #

INT_DIGITS = tuple(range(10))

###
# This class can transform a decimal writting natural like ``123`` to a "base"
# one like ``"7B"`` (which is the hexadecimal writing of ``123``).
#
# The input for conversion can be of the following kinds.
#
#     1) An ``int`` Python like ``123`` (``str`` version are not supported
#        by this module, and they won't be).
#
#     1) A list of digits like ``[1, 2, 3]``.
#
#     1) A list of numerals like ``["1", "2", "3"]``.
#
#
# note::
#     For this module, digits are ``int`` Python variables, and numerals are
#     ``str`` ones. In hexadecimal, the digits are the naturals from `0` to
#     `15`, and numerals are the strings ``"0"``, ..., ``"9"``, ``"A"``, ...,
#     and ``"F"`` (with the uppercase style).
#
#
# The base must be ``int`` Python greater than ``1``, and the output for
# conversion can be of the following kinds.
#
#     1) A ``str`` Python like ``"7B"``.
#
#     1) A list of digits like ``[7, 11]``.
#
#     1) A list of numerals like ``["7", "11"]``.
###
class Nat2Base(NatConv):
###
# prototype::
#     nb : a natural ¨nb
#        @ nb in NN
#
#     :return: the list of textual decimal digits of ``nb`` sorted from
#              the biggest weight to the smallest one
#            @ v in return ==> v in str(0..9)
###
    def numeralsof(self, nb: int) -> List[str]:
# Safe mode used?
        self.checknatural(nb)

# Let's work.
        return [d for d in str(nb)]


###
# prototype::
#     nb : :see: self.numeralsof
#
#     :return: the list of decimal digits of ``nb``, the digits sorted from
#              the biggest weight to the smallest one
#            @ v in return ==> v in 0..9
###
    def digitsof(self, nb: int) -> List[int]:
# Safe mode used?
        self.checknatural(nb)

# We can do the conversion.
        return [int(d) for d in str(nb)]


###
# prototype::
#     nb   : :see: self.numeralsof
#     base : the base used to write a natural natural
#          @ base in 2 .. +inf
#
#     :return: the list of natural digits of ``nb`` when it is converted
#              into the base ``base``, the digits are sorted from the biggest
#              weight to the smallest one
#            @ v in return ==> v in 0 .. (base-1)
#
#
# note::
#     The name ``nat2bdigits`` comes from "natural to base digits".
###
    def nat2bdigits(
        self,
        nb  : int,
        base: int,
    ) -> List[int]:
# Safe mode used?
        self.checknatural(nb)

# Special case of ``base = 10``.
        if base == 10:
            return self.digitsof(nb)

# Safe mode used?
        self.checknatural(
            nb      = base,
            mini    = 2,
            errname = 'base'
        )

# Special case of 0.
        if nb == 0:
            return [0]

# Let's work a little.
        bdigits = []

        while(nb):
            bdigits.append(nb % base)
            nb = nb // base

        bdigits.reverse()

        return bdigits


###
# prototype::
#     base : :see: self.nat2bdigits
#
#     :return: a function that converts a ``base`` natural digit into
#              a textual numeral.
#
#     :see: self.nat2bdigits
#
#
# warning::
#     This method is an internal one even if we let it public. No check
#     is done on the type and the value of ``base``!
###
    def numeralize(self, base: int) -> Callable[[int], str]:
# Number of characters needed to code one single digit.
        if base > self.max_singledigit:
            nbchars = ceil(log(base) / log(self.max_singledigit))

        else:
            nbchars = 1


# Internal functions
        def alphanum_single(
            x      : int,
            padding: bool = True
        ) -> str:
# We need more than one character.
            if x >= self.max_singledigit:
                result = "".join(
                    alphanum_single(
                        x       = d,
                        padding = False
                    )
                    for d in self.nat2bdigits(
                        nb   = x,
                        base = self.max_singledigit,
                    )
                )

# One single decimal numeral.
            elif x < 10:
                result = str(x)

# One single upper case letter.
            else:
# 65 - 10 = 55
                result = chr(55 + x)

# Padding or not padding? That is the question...
            if padding:
                result = result.rjust(nbchars, '0')

            return result


        def alphanum(nb: int) -> str:
            coding = tuple(
                map(
                    alphanum_single,
                    self.nat2bdigits(
                        nb   = nb,
                        base = base,
                    )
                )
            )

            return coding

# We return the coding function.
        return alphanum


###
# prototype::
#     nb   : :see: self.nat2bdigits
#     base : :see: self.nat2bdigits
#
#     :return: the list of textual numerals of ``nb`` when it is converted
#              into the base ``base``, the numerals beeing sorted from
#              the biggest weight to the smallest one
#
#     :see: self.numeralize
#
#
# note::
#     The name ``nat2bnumerals`` comes from "natural to base numerals".
###
    def nat2bnumerals(
        self,
        nb  : int,
        base: int,
    ) -> List[str]:
# Safe mode used?
        self.checknatural(nb)

# Special case of ``base = 10``.
        if base == 10:
            return self.numeralsof(nb)

# Safe mode used?
        self.checknatural(
            nb      = base,
            mini    = 2,
            errname = 'base'
        )

        return self.numeralize(base)(nb)


###
# prototype::
#     nb   : :see: self.nat2bdigits
#     base : :see: self.nat2bdigits
#     sep  : a text to use to separate numerals only if they use at least
#            two characters (that is the case when the base is bigger than 36).
#            An empty separator can be used.
#
#     :return: a string version of ``nb`` when it is converted into the base
#              ``base``
#
#     :see: self.nat2bnumerals
#
#
# note::
#     The name ``nat2bnb`` comes from "natural to base number".
###
    def nat2bnb(
        self,
        nb  : int,
        base: int,
        sep : str = ''
    ) -> str:
# Safe mode used?
        self.checknatural(nb)
        self.checknatural(
            nb      = base,
            mini    = 2,
            errname = 'base'
        )

# Let's work... a little.
        numerals = self.nat2bnumerals(
            nb   = nb,
            base = base,
        )

        return sep.join(numerals)


###
# prototype::
#     digits : a list of digits sorted from the biggest weight to
#              the smallest one
#             @ d in digits ==> d in 0..9
#
#     :return: the natural value corresponding to the digits
#
#
# note::
#     The name ``digits2nat`` comes from "digits to natural".
###
    def digits2nat(
        self,
        digits: List[int],
    ) -> int:
        intval = 0
        power  = 1

        for n in reversed(digits):
            assert n in INT_DIGITS, \
                   'unknown digit ``{0}``.'.format(n)

            intval += n*power
            power  *= 10

        return intval


###
# prototype::
#     numerals : a list of textual numerals sorted from the biggest weight to
#                the smallest one
#             @ d in numerals ==> d in str(0..9)
#
#     :return: the natural value corresponding to thenumerals
#
#
# note::
#     The name ``numerals2nat`` comes from "numerals to natural".
###
    def numerals2nat(
        self,
        numerals: List[str],
    ) -> int:
        for n in reversed(numerals):
            assert n in STR_DIGITS, \
                   'unknown numeral ``{0}``.'.format(n)

        return int(''.join(numerals))


# -- EXTRA METHODS "AUTO" - START -- #

# Lines automatically build by the following file.
#
#     + ``tools/factory/convert/natural/build_02_xtra_methods.py``

###
# prototype::
#     digits : :see: self.digits2nat
#     base : :see: self.nat2bdigits
#
#     :return: :see: self.nat2bdigits
###
    def digits2bdigits(
        self,
        digits: List[int],
        base: int,
    ) -> List[int]:
        return self.nat2bdigits(
            nb = self.digits2nat(
                digits = digits,
            ),
            base = base,
        )


###
# prototype::
#     digits : :see: self.digits2nat
#     base : :see: self.nat2bnb
#     sep : :see: self.nat2bnb
#
#     :return: :see: self.nat2bnb
###
    def digits2bnb(
        self,
        digits: List[int],
        base: int,
        sep: str = '',
    ) -> str:
        return self.nat2bnb(
            nb = self.digits2nat(
                digits = digits,
            ),
            base = base,
            sep = sep,
        )


###
# prototype::
#     digits : :see: self.digits2nat
#     base : :see: self.nat2bnumerals
#
#     :return: :see: self.nat2bnumerals
###
    def digits2bnumerals(
        self,
        digits: List[int],
        base: int,
    ) -> List[str]:
        return self.nat2bnumerals(
            nb = self.digits2nat(
                digits = digits,
            ),
            base = base,
        )


###
# prototype::
#     numerals : :see: self.numerals2nat
#     base : :see: self.nat2bdigits
#
#     :return: :see: self.nat2bdigits
###
    def numerals2bdigits(
        self,
        numerals: List[str],
        base: int,
    ) -> List[int]:
        return self.nat2bdigits(
            nb = self.numerals2nat(
                numerals = numerals,
            ),
            base = base,
        )


###
# prototype::
#     numerals : :see: self.numerals2nat
#     base : :see: self.nat2bnb
#     sep : :see: self.nat2bnb
#
#     :return: :see: self.nat2bnb
###
    def numerals2bnb(
        self,
        numerals: List[str],
        base: int,
        sep: str = '',
    ) -> str:
        return self.nat2bnb(
            nb = self.numerals2nat(
                numerals = numerals,
            ),
            base = base,
            sep = sep,
        )


###
# prototype::
#     numerals : :see: self.numerals2nat
#     base : :see: self.nat2bnumerals
#
#     :return: :see: self.nat2bnumerals
###
    def numerals2bnumerals(
        self,
        numerals: List[str],
        base: int,
    ) -> List[str]:
        return self.nat2bnumerals(
            nb = self.numerals2nat(
                numerals = numerals,
            ),
            base = base,
        )

# -- EXTRA METHODS "AUTO" - END -- #
