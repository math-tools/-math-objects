#!/usr/bin/env python3

###
# This module converts decimal writings into specific base writings.
###


from typing import *


# ----------------------------------------- #
# -- NATURAL: DECIMAL ~~~> SPECIFIC BASE -- #
# ----------------------------------------- #

###
# ???
###
class NatConv:
###
# prototype::
#     safemode : ???
#     errname  : the name used in case of error message
###
    def __init__(
        self,
        safemode: bool = True,
        errname : str  = "number",
    ):
        self.safemode = safemode
        self.errname  = errname

        self.max_singledigit = 36


###
# ???
###
    @property
    def safemode(self) -> str:
        return self._safemode

    @safemode.setter
    def safemode(self, safemode: bool) -> None:
        self._safemode = safemode

        if safemode:
            self.checknatural = self.__checknatural

        else:
            self.checknatural = lambda nb, mini=0, maxi=0, errname='': None


###
# prototype::
###
    def __checknatural(
        self,
        nb     : Any,
        mini   : float = 0,
        maxi   : float = float('inf'),
        errname: str   = '',
    ) -> None:
        if not errname:
            errname = self.errname

        assert isinstance(nb, int), \
               f"The {errname} ``{nb}`` is not an integer."

        assert nb >= mini, \
               f"The {errname} ``{nb}`` is too small ({mini = })."

        assert nb <= maxi, \
               f"The {errname} ``{nb}`` is too big ({maxi = })."
