# ColorEditor.py
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
from PyQt6.QtWidgets import QFrame, QVBoxLayout
from guiQt.AdvanceSliderLine import AdvanceSliderLine
from PyQt6.QtCore import pyqtSignal

# ------------------------------------------------------------------------------------------
# --- class ColorEditor (QFrame) ------------------------------------------------------
# ------------------------------------------------------------------------------------------
class ColorEditor(QFrame):
    # class attributes
    ## signal
    valueChanged = pyqtSignal(dict)

    # constructor
    def __init__(self : Self) -> None:
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)

        # attributes

        ## layout and widget
        self.topLayout : QVBoxLayout = QVBoxLayout()
        self.setLayout(self.topLayout)

        self.hueShift : AdvanceSliderLine = AdvanceSliderLine('hue shift', 0.0,(-180,180))
        self.saturation : AdvanceSliderLine = AdvanceSliderLine('saturation', 0.0,(-100,100))
        self.exposure : AdvanceSliderLine = AdvanceSliderLine('exposure',0, (-300,300),(-3,+3)) # -3,+3 0.01
        self.contrast : AdvanceSliderLine = AdvanceSliderLine('contrast', 0.0,(-100,100))

        ## add widget to layout
        self.topLayout.addWidget(self.hueShift)
        self.topLayout.addWidget(self.saturation)
        self.topLayout.addWidget(self.exposure)
        self.topLayout.addWidget(self.contrast)

        # connect signals
        self.hueShift.valueChanged.connect(lambda value: self.emitValueChanged())
        self.saturation.valueChanged.connect(lambda value: self.emitValueChanged())
        self.exposure.valueChanged.connect(lambda value: self.emitValueChanged())
        self.contrast.valueChanged.connect(lambda value: self.emitValueChanged())

    def emitValueChanged(self):
        values = {
            'hue': self.hueShift.tovalue(),
            'saturation': self.saturation.value(),
            'exposure': self.exposure.value(),
            'contrast': self.contrast.value()
        }
        self.valueChanged.emit(values)
# ------------------------------------------------------------------------------------------