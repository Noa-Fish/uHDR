# uHDR: HDR image editing software
#   Copyright (C) 2024  antoine bacquet et noa watel 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
# hdrCore project 2020-2024
# author: bacquet antoine et watel noa


# import
# ------------------------------------------------------------------------------------------
from core import colourData, colourSpace
from guiQt.ColorEditor import ColorEditor
# ------------------------------------------------------------------------------------------
# test
# ------------------------------------------------------------------------------------------
def test() -> ColorEditor:

    # def cb(name: str, min:int, max:int) -> None : print(f'/§\\ {name}::[{min},{max}]')

    testCS : ColorEditor = ColorEditor()
    return testCS
# ------------------------------------------------------------------------------------------