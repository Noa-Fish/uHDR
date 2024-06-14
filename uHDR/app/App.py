# App.py
# uHDR: HDR image editing software
#   Copyright (C) 2024  antoine bacquet et noa watel 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, ou
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
from __future__ import annotations

from numpy import ndarray
from app.Jexif import Jexif

import preferences.Prefs
from guiQt.MainWindow import MainWindow
from app.ImageFiles import ImageFiles
from app.Tags import Tags
from app.SelectionMap import SelectionMap
from hdrCore import processing
from hdrCore import image

# ------------------------------------------------------------------------------------------
# --- class App ----------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# imports additionnels nécessaires
import copy
import numpy as np
import math
import colour
from timeit import default_timer as timer

from hdrCore.processing import exposure, saturation, Ycurve

class App:
    # static attributes

    # constructor
    def __init__(self: App) -> None:
        """uHDR v7 application"""
        # loading preferences
        preferences.Prefs.Prefs.load()

        # Set default verbose if not set
        if not hasattr(preferences.Prefs.Prefs, 'verbose'):
            preferences.Prefs.Prefs.verbose = False

        ## -----------------------------------------------------
        ## ------------         attributes          ------------
        ## -----------------------------------------------------        
        
        ## image file management
        self.original_image = None
        self.imagesManagement : ImageFiles = ImageFiles()
        self.imagesManagement.imageLoaded.connect(self.CBimageLoaded)
        self.imagesManagement.setPrefs()
        self.imagesManagement.checkExtra()
        nbImages : int = self.imagesManagement.setDirectory(preferences.Prefs.Prefs.currentDir)

        # read image tags in directory
        allTagsInDir : dict[str, dict[str,bool]] =  Tags.aggregateTagsFiles(preferences.Prefs.Prefs.currentDir,preferences.Prefs.Prefs.extraPath)
        
        # merge with default tags from preferences
        self.tags : Tags = Tags(Tags.aggregateTagsData([preferences.Prefs.Prefs.tags, allTagsInDir]))
        
        ## selection
        self.selectionMap :  SelectionMap = SelectionMap(self.imagesManagement.getImagesFilesnames())

        ## current selected image
        self.selectedImageIdx : int | None = None

        ## -----------------------------------------------------
        ## ------------             gui             ------------
        ## -----------------------------------------------------

        self.mainWindow : MainWindow = MainWindow(nbImages, self.tags.toGUI())
        self.mainWindow.showMaximized()
        self.mainWindow.show()

        self.defaultExposureValue = 0
        self.currentExposureValue = 0
        self.exposureActive = True
        
        self.defaultSaturationValue = 0
        self.currentSaturationValue = 0
        self.saturationActive = True
        
        ## callbacks
        self.mainWindow.dirSelected.connect(self.CBdirSelected)
        self.mainWindow.requestImages.connect(self.CBrequestImages)
        self.mainWindow.imageSelected.connect(self.CBimageSelected)

        self.mainWindow.tagChanged.connect(self.CBtagChanged)
        self.mainWindow.scoreChanged.connect(self.CBscoreChanged)

        self.mainWindow.scoreSelectionChanged.connect(self.CBscoreSelectionChanged)
        self.mainWindow.editBlock.edit.lightEdit.light.contrast.scalingSliderChanged.connect(self.CBcontrastscalingChanged)
        
        self.mainWindow.editBlock.edit.lightEdit.light.exposure.activeToggled.connect(self.CBexposureactiveChanged)
        self.mainWindow.editBlock.edit.lightEdit.light.exposure.autoClicked.connect(self.CBexposureautoChanged)
        self.mainWindow.editBlock.edit.lightEdit.light.exposure.valueChanged.connect(self.CBexposureChanged)
        
        self.mainWindow.editBlock.edit.lightEdit.light.saturation.activeToggled.connect(self.CBsaturationactiveChanged)
        self.mainWindow.editBlock.edit.lightEdit.light.saturation.autoClicked.connect(self.CBsaturationautoChanged)
        self.mainWindow.editBlock.edit.lightEdit.light.saturation.valueChanged.connect(self.CBsaturationChanged)
        
        self.mainWindow.editBlock.edit.lightEdit.light.curve.curveChanged.connect(self.CBcurveChanged) 

        self.mainWindow.setPrefs()

        # Initialize exposure, saturation, and Ycurve processing
        self.exposureProcessor = exposure()
        self.saturationProcessor = saturation()
        self.curveProcessor = Ycurve()

    # methods
    # -----------------------------------------------------------------

    ##  getImageRangeIndex
    ## ----------------------------------------------------------------
    def getImageRangeIndex(self: App) -> tuple[int,int]: 
        """return the index range (min index, max index) of images displayed by the gallery."""

        return self.mainWindow.imageGallery.getImageRangeIndex()

    ##  update
    ## ----------------------------------------------------------------
    def update(self: App) -> None:
        """call to update gallery after selection changed or directory changed."""
        # number of image in current pages 
        minIdx, maxIdx = self.getImageRangeIndex()
        self.mainWindow.setNumberImages(self.selectionMap.getSelectedImageNumber()) 
        self.mainWindow.setNumberImages(maxIdx - minIdx) 
        self.CBrequestImages(minIdx, maxIdx)

    ## -----------------------------------------------------------------------------------------------------
    ## app logic: callbacks 
    ## -----------------------------------------------------------------------------------------------------

    #### select new directory
    #### -----------------------------------------------------------------
    def CBdirSelected(self: App, path:str) -> None:
        """callback: called when directory is selected."""

        # ------------- DEBUG -------------
        print(f'App.CBdirSelected({path})')
        # ------------- ------ -------------  

        self.imagesManagement.setDirectory(path)
        self.selectionMap.setImageNames(self.imagesManagement.getImagesFilesnames())
        self.selectionMap.selectAll()

        # reset gallery 
        self.mainWindow.resetGallery()
        self.mainWindow.setNumberImages(self.imagesManagement.getNbImages())
        self.mainWindow.firstPage()

    #### request image: zoom or page changed
    #### -----------------------------------------------------------------
    def CBrequestImages(self: App, minIdx: int , maxIdx:int ) -> None:
        """callback: called when images are requested (occurs when page ou zoom level is changed)."""

        imagesFilenames : list[str] = self.imagesManagement.getImagesFilesnames()

        for sIdx in range(minIdx, maxIdx+1):

            gIdx : int|None = self.selectionMap.selectedlIndexToGlobalIndex(sIdx) 

            if gIdx != None: self.imagesManagement.requestLoad(imagesFilenames[gIdx])
            else: self.mainWindow.setGalleryImage(sIdx, None)


    #### image loaded
    #### -----------------------------------------------------------------
    def CBimageLoaded(self: App, filename: str):
        """"callback: called when requested image is loaded (asynchronous loading)."""

        image : ndarray = self.imagesManagement.images[filename]
        imageIdx = self.selectionMap.imageNameToSelectedIndex(filename)         

        if imageIdx != None: self.mainWindow.setGalleryImage(imageIdx, image)


    #### image selected
    #### -----------------------------------------------------------------
    def CBimageSelected(self: App, index):

        self.selectedImageIdx = index # index in selection

        gIdx : int | None = self.selectionMap.selectedlIndexToGlobalIndex(index) # global index

        if (gIdx != None):

            image : ndarray = self.imagesManagement.getImage(self.imagesManagement.getImagesFilesnames()[gIdx])
            tags : Tags = self.imagesManagement.getImageTags(self.imagesManagement.getImagesFilesnames()[gIdx])
            exif : dict[str,str] = self.imagesManagement.getImageExif(self.imagesManagement.getImagesFilesnames()[gIdx])
            score : int = self.imagesManagement.getImageScore(self.imagesManagement.getImagesFilesnames()[gIdx])

            self.mainWindow.setEditorImage(image)

            # update image info
            imageFilename : str =  self.imagesManagement.getImagesFilesnames()[gIdx] 
            imagePath : str =  self.imagesManagement.imagePath 
            #### if debug : print(f'App.CBimageSelected({index}) > path:{imagePath}')

            self.mainWindow.setInfo(imageFilename, imagePath, *Jexif.toTuple(exif))

            self.mainWindow.setScore(score)

            # update tags info
            self.mainWindow.resetTags()
            if tags:
                self.mainWindow.setTagsImage(tags.toGUI())

    #### tag changed
    #### -----------------------------------------------------------------
    def CBtagChanged(self, key: tuple[str, str], value : bool) -> None:

        if self.selectedImageIdx != None:
            imageName : str|None = self.selectionMap.selectedIndexToImageName(self.selectedImageIdx)
            if debug : print(f'\t\t imageName:{imageName}')
            if imageName != None : self.imagesManagement.updateImageTag(imageName, key[0], key[1], value)
    
    #### score changed
    #### -----------------------------------------------------------------
    def CBscoreChanged(self, value : int) -> None:

        if self.selectedImageIdx != None:
            imageName : str|None = self.selectionMap.selectedIndexToImageName(self.selectedImageIdx)

            if imageName != None : self.imagesManagement.updateImageScore(imageName, value)

    ### score selection changed
    ### ------------------------------------------------------------------
    def CBscoreSelectionChanged(self: App, listSelectedScore : list[bool]) -> None:
        """called when selection changed."""

        # get {'image name': score}
        imageScores : dict[str, int] = self.imagesManagement.imageScore
        # selected score
        selectedScores : list[int] = []
        for i, selected in enumerate(listSelectedScore) :  
            if selected : selectedScores.append(i)
        # send info to selectionMap
        self.selectionMap.selectByScore(imageScores, selectedScores)
        self.update()
### exposure changed
# ------------------------------------------------------------------------------------------
    def CBexposureChanged(self, value):
        print(f"adjustExposure called with value: {value} AND esxposureActive: {self.exposureActive}")
        defaut = False
        if self.exposureActive == False:
            self.currentExposureValue = value
        if self.exposureActive == False and value==0:
            defaut = True
        if defaut or self.exposureActive :
            if self.selectedImageIdx is None:
                return
            
            imageName = self.selectionMap.selectedIndexToImageName(self.selectedImageIdx)
            print(f"Selected image name: {imageName}")
                
            if not imageName:
                return
            
            # Si l'image originale n'a pas encore été copiée, faites-le maintenant
            if self.original_image is None:
                img = self.imagesManagement.getImage(imageName)
                
                # Convertir en hdrCore.image.Image si nécessaire
                if not isinstance(img, image.Image):
                    img = image.Image(
                        self.imagesManagement.imagePath,
                        imageName,
                        img,
                        image.imageType.SDR,
                        False,
                        image.ColorSpace.sRGB()
                    )
                self.original_image = img
            
            # Créer une copie de l'image originale
            img_copy = copy.deepcopy(self.original_image)

            exposure_processor = processing.exposure()
            processed_image = exposure_processor.compute(img_copy, EV=value)

            if isinstance(processed_image, image.Image):
                self.imagesManagement.images[imageName] = processed_image.colorData
                self.mainWindow.setEditorImage(processed_image.colorData)
            else:
                print(f"Unexpected processed image type: {type(processed_image)}")
### curve & data changed
# ------------------------------------------------------------------------------------------
    def CBcurveChanged(self, controlPoints):
        print(f"adjustCurve called with controlPoints: {controlPoints}")
        
        if self.selectedImageIdx is None:
            return
        
        imageName = self.selectionMap.selectedIndexToImageName(self.selectedImageIdx)
        print(f"Selected image name: {imageName}")
        
        if not imageName:
            return
        
        # Complétez les points de contrôle manquants avec des valeurs par défaut
        full_control_points = {
            'start': [0.0, 0.0],
            'end': [200.0, 100.0],
            'shadows': controlPoints.get('shadows', [10.0, 10.0]),
            'blacks': controlPoints.get('blacks', [30.0, 30.0]),
            'mediums': controlPoints.get('mediums', [50.0, 50.0]),
            'whites': controlPoints.get('whites', [70.0, 70.0]),
            'highlights': controlPoints.get('highlights', [90.0, 90.0])
        }
        
        # Si l'image originale n'a pas encore été copiée, faites-le maintenant
        if self.original_image is None:
            img = self.imagesManagement.getImage(imageName)
            
            # Convertir en hdrCore.image.Image si nécessaire
            if not isinstance(img, image.Image):
                img = image.Image(
                    self.imagesManagement.imagePath,
                    imageName,
                    img,
                    image.imageType.SDR,
                    False,
                    image.ColorSpace.sRGB()
                )
            self.original_image = img
        
        # Créer une copie de l'image originale
        img_copy = copy.deepcopy(self.original_image)

        curve_processor = processing.Ycurve()
        processed_image = curve_processor.compute(img_copy, **full_control_points)

        if isinstance(processed_image, image.Image):
            print(f"Processed image type is correct")
            self.imagesManagement.images[imageName] = processed_image.colorData
            self.mainWindow.setEditorImage(processed_image.colorData)
        else:
            print(f"Unexpected processed image type: {type(processed_image)}")
# ------------------------------------------------------------------------------------------
    def CBcontrastscalingChanged(self, value):
        if self.selectedImageIdx is None:
            return

        imageName = self.selectionMap.selectedIndexToImageName(self.selectedImageIdx)

        if not imageName:
            return

        # Si l'image originale n'a pas encore été copiée, faites-le maintenant
        if self.original_image is None:
            img = self.imagesManagement.getImage(imageName)

            # Convertir en hdrCore.image.Image si nécessaire
            if not isinstance(img, image.Image):
                img = image.Image(
                    self.imagesManagement.imagePath,
                    imageName,
                    img,
                    image.imageType.SDR,
                    False,
                    image.ColorSpace.sRGB()
                )
            self.original_image = img

        # Créer une copie de l'image originale
        img_copy = copy.deepcopy(self.original_image)

        saturation_processor = processing.contrast()
        processed_image = saturation_processor.compute(img_copy, contrast=value)

        if isinstance(processed_image, image.Image):
            print(f"Processed image type is correct")
            self.imagesManagement.images[imageName] = processed_image.colorData
            self.mainWindow.setEditorImage(processed_image.colorData)
        else:
            print(f"Unexpected processed image type: {type(processed_image)}")
            
            
    
    def CBexposureautoChanged(self):
        print(f"adjustExposureAuto clicked")
        
        # if self.selectedImageIdx is None:
        #     return
        
        # imageName = self.selectionMap.selectedIndexToImageName(self.selectedImageIdx)
        # print(f"Selected image name: {imageName}")
        
        # if not imageName:
        #     return
        
        # # Si l'image originale n'a pas encore été copiée, faites-le maintenant
        # if self.original_image is None:
        #     img = self.imagesManagement.getImage(imageName)
            
        #     # Convertir en hdrCore.image.Image si nécessaire
        #     if not isinstance(img, image.Image):
        #         img = image.Image(
        #             self.imagesManagement.imagePath,
        #             imageName,
        #             img,
        #             image.imageType.SDR,
        #             False,
        #             image.ColorSpace.sRGB()
        #         )
        #     self.original_image = img
        
        # # Créer une copie de l'image originale
        # img_copy = copy.deepcopy(self.original_image)

        # exposure_processor = processing.exposure()
        # processed_image = exposure_processor.auto(img_copy)

        # if isinstance(processed_image, image.Image):
        #     self.imagesManagement.images[imageName] = processed_image.colorData
        #     self.mainWindow.setEditorImage(processed_image.colorData)
        # else:
        #     print(f"Unexpected processed image type: {type(processed_image)}")
        pass
    
    def CBexposureactiveChanged(self, active):
        self.exposureActive = active
        if not active:
            # Lorsque désactivé, utiliser la valeur par défaut
            self.CBexposureChanged(self.defaultExposureValue)
        else:
            # Lorsque activé, utiliser la valeur actuelle
            self.CBexposureChanged(self.currentExposureValue)
    ### saturation changed
# ------------------------------------------------------------------------------------------
    def CBsaturationChanged(self, value):
        
        print(f"adjustSaturation called with value: {value} AND saturationActive: {self.saturationActive}")
        defaut = False
        if self.saturationActive == False:
            self.currentSaturationValue = value
        if self.saturationActive == False and value==0:
            defaut = True
        if defaut or self.saturationActive :
            if self.selectedImageIdx is None:
                return
            
            imageName = self.selectionMap.selectedIndexToImageName(self.selectedImageIdx)
                
            if not imageName:
                return
            
            # Si l'image originale n'a pas encore été copiée, faites-le maintenant
            if self.original_image is None:
                img = self.imagesManagement.getImage(imageName)
                
                # Convertir en hdrCore.image.Image si nécessaire
                if not isinstance(img, image.Image):
                    img = image.Image(
                        self.imagesManagement.imagePath,
                        imageName,
                        img,
                        image.imageType.SDR,
                        False,
                        image.ColorSpace.sRGB()
                    )
                self.original_image = img
            
            # Créer une copie de l'image originale
            img_copy = copy.deepcopy(self.original_image)

            saturation_processor = processing.saturation()
            processed_image = saturation_processor.compute(img_copy, saturation=value)

            if isinstance(processed_image, image.Image):
                self.imagesManagement.images[imageName] = processed_image.colorData
                self.mainWindow.setEditorImage(processed_image.colorData)
            else:
                print(f"Unexpected processed image type: {type(processed_image)}")

    def CBsaturationactiveChanged(self, active):
        print(f"ToggleActive {self.saturationActive}")
        self.saturationActive = active
        if not active:
            # Lorsque désactivé, utiliser la valeur par défaut
            self.CBsaturationChanged(self.defaultSaturationValue)
        else:
            # Lorsque activé, utiliser la valeur actuelle
            self.CBsaturationChanged(self.currentSaturationValue)

    def CBsaturationautoChanged(self):
        print(f"adjustSaturationAuto clicked")
        # Logic for automatic saturation adjustment can be implemented here
        pass


