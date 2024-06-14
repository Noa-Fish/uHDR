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
from typing_extensions import Self
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QTabWidget
from PyQt6.QtGui import QDoubleValidator, QIntValidator 
from PyQt6.QtCore import Qt, pyqtSignal, QLocale

from guiQt.LightBlockScroll import LightBlockScroll
from guiQt.ColorBlockScroll import ColorBlockScroll

# ------------------------------------------------------------------------------------------
# --- class Editor (QTabWidget) ------------------------------------------------------
# ------------------------------------------------------------------------------------------
class Editor(QTabWidget):
    # class attributes
    ## signal
    exposureChanged: pyqtSignal = pyqtSignal(float)
    
    # constructor
    def __init__(self: Self) -> None:
        super().__init__()

        # attributes
        self.lightEdit: LightBlockScroll = LightBlockScroll()
        self.nbColorEditor: int = 5
        self.colorEdits: list[ColorBlockScroll] = []
        for i in range(self.nbColorEditor):
            self.colorEdits.append(ColorBlockScroll())

        # QTabWidget setup
        self.setTabPosition(QTabWidget.TabPosition.East)
        self.setMovable(True)

        # add widgets
        self.addTab(self.lightEdit, "Light")
        for i in range(self.nbColorEditor):
            self.addTab(self.colorEdits[i], "Color " + str(i))

        self.lightEdit.light.exposure.valueChanged.connect(self.CBexposureChanged)
       
        
    def CBexposureChanged(self, value):
        print(f'Editor exposure changed: {value}')
        self.parent().exposureChanged.emit(value)
