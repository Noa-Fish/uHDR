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

"""Only contains main program."""

from PyQt6.QtWidgets import QApplication 
from multiprocessing import freeze_support

from app.App import App

import sys
# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
if __name__ == '__main__':
    freeze_support()
    print("---------------------------------------------------------------------------------------")
    print("--------------------------- uHDRv7 - June 2024 (C++ core) -----------------------------")
    print("---------------------------------------------------------------------------------------")
    print("----                   High Dynamic Range image editing software                   ----")
    print("---- FEATURES:                                                                     ----")
    print("----     1. edit image exposure, contrast, tone curve                              ----")
    print("----     2. define color segments according to hue, saturation and lightness range ----")
    print("----     3. edit color segments: hue shift, exposure, contrast and saturation      ----")
    print("----     4. target many HDR displays: vesa HDR displays, HLG ...                   ----")                                                                            
    print("---------------------------------------------------------------------------------------")
    print("---- author(s): Antoine Bacquet,                                                   ----")
    print("----            Noa Watel,                                                         ----")
    print("---------------------------------------------------------------------------------------")
    print("---- date: uHDRv1:2019, uHDRv7: 2024                                               ----")
    print("---------------------------------------------------------------------------------------")
    print("----                      GNU General Public License version 3                     ----")
    print("---------------------------------------------------------------------------------------")



    appQt : QApplication = QApplication(sys.argv)
    appHDR : App = App()

    sys.exit(appQt.exec())
# ------------------------------------------------------------------------------------------
