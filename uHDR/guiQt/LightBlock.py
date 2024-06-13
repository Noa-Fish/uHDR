# LightBlock.py
# uHDR: HDR image editing software
#   Copyright (C) 2022  remi cozot 
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
# hdrCore project 2020-2022
# author: remi.cozot@univ-littoral.fr

# import
# ------------------------------------------------------------------------------------------
from typing_extensions import Self
from PyQt6.QtWidgets import QFrame, QVBoxLayout
from PyQt6.QtGui import QDoubleValidator, QIntValidator 
from PyQt6.QtCore import Qt, pyqtSignal, QLocale

from guiQt.AdvanceSlider import AdvanceSlider
from guiQt.Contrast import Contrast
from guiQt.CurveWidget import CurveWidget
from guiQt.MemoGroup import MemoGroup

# ------------------------------------------------------------------------------------------
# --- class LightBlock (QFrame) ------------------------------------------------------
# ------------------------------------------------------------------------------------------
class LightBlock(QFrame):
    # class attributes
    ## signal
    exposureChanged: pyqtSignal = pyqtSignal(float)
    saturationChanged: pyqtSignal = pyqtSignal(float)

    # constructor
    def __init__(self: Self) -> None:
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)

        # attributes
        self.active: bool = True

        # layout and widgets
        self.topLayout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.topLayout)

        self.exposure: AdvanceSlider = AdvanceSlider('exposure', 0.0, (-30, +30), (-3.0, +3.0), 10)
        self.saturation: AdvanceSlider = AdvanceSlider('saturation', 0.0, (-100, +100), (-1.0, +1.0), 10)
        self.contrast: Contrast = Contrast()
        self.curve: CurveWidget = CurveWidget()

        # add to layout
        self.topLayout.addWidget(self.exposure)
        self.topLayout.addWidget(self.saturation)
        self.topLayout.addWidget(self.contrast)
        self.topLayout.addWidget(self.curve)

        self.exposure.valueChanged.connect(self.exposureChanged)
        self.saturation.valueChanged.connect(self.saturationChanged)

