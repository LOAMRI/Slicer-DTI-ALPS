"""
MIT License

Copyright (c) 2024 Antonio Carlos da Silva Senra Filho and André Monteiro Paschoal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import logging
import os
from typing import Annotated, Optional

import vtk

import numpy as np

import slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin
from slicer.parameterNodeWrapper import (
    parameterNodeWrapper,
    WithinRange,
)

from slicer import vtkMRMLDiffusionTensorVolumeNode
from slicer import vtkMRMLLabelMapVolumeNode


#
# DTI_ALPS
#

class DTI_ALPS(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "DTI ALPS" 
        self.parent.categories = ["Diffusion"]
        self.parent.dependencies = []
        self.parent.contributors = ["Antonio Carlos da Silva Senra Filho (State University of Campinas), André Monteiro Paschoal (State University of Campinas)"]
        self.parent.helpText = """
This is a module that calculates the DTI-ALPS index from DTI images. More details are found at the <a href=https://slicer-dti-alps.readthedocs.io/en/latest">documentation page</a>
"""
        # TODO: replace with organization, grant and thanks
        self.parent.acknowledgementText = """
This module was originally developed by Antonio Senra Filho, State University of Campinas (Unicamp) and it was supervised by André M. Paschoal, State University of Campinas (Unicamp). The financial resource was funded by the State University of Campinas, 2024.
"""
        # Additional initialization step after application startup is complete
        slicer.app.connect("startupCompleted()", registerSampleData)


#
# Register sample data sets in Sample Data module
#

def registerSampleData():
    """
    Add data sets to Sample Data module.
    """
    # It is always recommended to provide sample data for users to make it easy to try the module,
    # but if no sample data is available then this method (and associated startupCompeted signal connection) can be removed.

    import SampleData
    iconsPath = os.path.join(os.path.dirname(__file__), 'Resources/Icons')

    # To ensure that the source code repository remains small (can be downloaded and installed quickly)
    # it is recommended to store data sets that are larger than a few MB in a Github release.

    # DTI_ALPS1
    SampleData.SampleDataLogic.registerCustomSampleDataSource(
        # Category and sample name displayed in Sample Data module
        category='DTI_ALPS',
        sampleName='DTI_ALPS1',
        # Thumbnail should have size of approximately 260x280 pixels and stored in Resources/Icons folder.
        # It can be created by Screen Capture module, "Capture all views" option enabled, "Number of images" set to "Single".
        thumbnailFileName=os.path.join(iconsPath, 'DTI_ALPS1.png'),
        # Download URL and target file name
        uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95",
        fileNames='DTI_ALPS1.nrrd',
        # Checksum to ensure file integrity. Can be computed by this command:
        #  import hashlib; print(hashlib.sha256(open(filename, "rb").read()).hexdigest())
        checksums='SHA256:998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95',
        # This node name will be used when the data set is loaded
        nodeNames='DTI_ALPS1'
    )

    # DTI_ALPS2
    SampleData.SampleDataLogic.registerCustomSampleDataSource(
        # Category and sample name displayed in Sample Data module
        category='DTI_ALPS',
        sampleName='DTI_ALPS2',
        thumbnailFileName=os.path.join(iconsPath, 'DTI_ALPS2.png'),
        # Download URL and target file name
        uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
        fileNames='DTI_ALPS2.nrrd',
        checksums='SHA256:1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97',
        # This node name will be used when the data set is loaded
        nodeNames='DTI_ALPS2'
    )


#
# DTI_ALPSParameterNode
#

@parameterNodeWrapper
class DTI_ALPSParameterNode:
    """
    The parameters needed by module.

    inputVolume - The DTI volume to calculate the DTI-ALPS index.
    inputProjectionLabel - The image label that defines the Projection area
    inputAssociationLabel - The image label that defines the Association area
    """
    inputVolume: vtkMRMLDiffusionTensorVolumeNode
    inputProjectionLabel: vtkMRMLLabelMapVolumeNode
    inputAssociationLabel: vtkMRMLLabelMapVolumeNode


#
# DTI_ALPSWidget
#

class DTI_ALPSWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    """Uses ScriptedLoadableModuleWidget base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent=None) -> None:
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        ScriptedLoadableModuleWidget.__init__(self, parent)
        VTKObservationMixin.__init__(self)  # needed for parameter node observation
        self.logic = None
        self._parameterNode = None
        self._parameterNodeGuiTag = None

    def setup(self) -> None:
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        ScriptedLoadableModuleWidget.setup(self)

        # Load widget from .ui file (created by Qt Designer).
        # Additional widgets can be instantiated manually and added to self.layout.
        uiWidget = slicer.util.loadUI(self.resourcePath('UI/DTI_ALPS.ui'))
        self.layout.addWidget(uiWidget)
        self.ui = slicer.util.childWidgetVariables(uiWidget)

        # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
        # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
        # "setMRMLScene(vtkMRMLScene*)" slot.
        uiWidget.setMRMLScene(slicer.mrmlScene)

        # Create logic class. Logic implements all computations that should be possible to run
        # in batch mode, without a graphical user interface.
        self.logic = DTI_ALPSLogic()

        # Connections

        # These connections ensure that we update parameter node when scene is closed
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

        # Buttons
        self.ui.applyButton.connect('clicked(bool)', self.onApplyButton)

        # Make sure parameter node is initialized (needed for module reload)
        self.initializeParameterNode()

    def cleanup(self) -> None:
        """
        Called when the application closes and the module widget is destroyed.
        """
        self.removeObservers()

    def enter(self) -> None:
        """
        Called each time the user opens this module.
        """
        # Make sure parameter node exists and observed
        self.initializeParameterNode()

    def exit(self) -> None:
        """
        Called each time the user opens a different module.
        """
        # Do not react to parameter node changes (GUI will be updated when the user enters into the module)
        if self._parameterNode:
            self._parameterNode.disconnectGui(self._parameterNodeGuiTag)
            self._parameterNodeGuiTag = None
            self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self._checkCanApply)

    def onSceneStartClose(self, caller, event) -> None:
        """
        Called just before the scene is closed.
        """
        # Parameter node will be reset, do not use it anymore
        self.setParameterNode(None)

    def onSceneEndClose(self, caller, event) -> None:
        """
        Called just after the scene is closed.
        """
        # If this module is shown while the scene is closed then recreate a new parameter node immediately
        if self.parent.isEntered:
            self.initializeParameterNode()

    def initializeParameterNode(self) -> None:
        """
        Ensure parameter node exists and observed.
        """
        # Parameter node stores all user choices in parameter values, node selections, etc.
        # so that when the scene is saved and reloaded, these settings are restored.

        self.setParameterNode(self.logic.getParameterNode())

    def setParameterNode(self, inputParameterNode: Optional[DTI_ALPSParameterNode]) -> None:
        """
        Set and observe parameter node.
        Observation is needed because when the parameter node is changed then the GUI must be updated immediately.
        """

        if self._parameterNode:
            self._parameterNode.disconnectGui(self._parameterNodeGuiTag)
            self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self._checkCanApply)
        self._parameterNode = inputParameterNode
        if self._parameterNode:
            # Note: in the .ui file, a Qt dynamic property called "SlicerParameterName" is set on each
            # ui element that needs connection.
            self._parameterNodeGuiTag = self._parameterNode.connectGui(self.ui)
            self.addObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self._checkCanApply)
            self._checkCanApply()

    def _checkCanApply(self, caller=None, event=None) -> None:
        # TODO: Mudar logica quando tiver o checkbox que a imagem está no espaço MNI padrão
        self.ui.applyButton.enabled = True

    def onApplyButton(self) -> None:
        """
        Run processing when user clicks "Apply" button.
        """
        with slicer.util.tryWithErrorDisplay("Failed to compute results.", waitCursor=True):

            # Compute DTI-ALPS index
            self.logic.process(self.ui.inputDTISelector.currentNode(), self.ui.inputProjLabelSelector.currentNode(),
                               self.ui.inputAssocLabelSelector.currentNode(), self.ui.MNISpaceCheckBox.checked)
            self.ui.dti_alps_output.text = str(self.logic.dti_alps)

#
# DTI_ALPSLogic
#
class DTI_ALPSLogic(ScriptedLoadableModuleLogic):
    """This class should implement all the actual
    computation done by your module.  The interface
    should be such that other python code can import
    this class and make use of the functionality without
    requiring an instance of the Widget.
    Uses ScriptedLoadableModuleLogic base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    dti_alps = 0.0

    def __init__(self) -> None:
        """
        Called when the logic class is instantiated. Can be used for initializing member variables.
        """
        ScriptedLoadableModuleLogic.__init__(self)

    def getParameterNode(self):
        return DTI_ALPSParameterNode(super().getParameterNode())

    def checkLabelNode(self, nodeName):
        try:
            slicer.util.getNode(nodeName) 
        except slicer.util.MRMLNodeNotFoundException as error:
            return False
        
        return True

    def checkMNISpaceInput(self, inputDTIVolume, referenceMNI):
        in_array = slicer.util.arrayFromVolume(inputDTIVolume)
        ref_array = slicer.util.arrayFromVolume(referenceMNI)

        # Comparing the image size (numpy shape) to unsure the same image space
        # DTI has a 3x3 matrix at the final part, thus we are have to compare only the 3 part of the image shape
        if in_array.shape[:3]==ref_array.shape:
            return True
        else:
            return False

    def calculateDTIALPS(self, inputDTIVolume, inputProjLabel, inputAssocLabel):
        dti_vol = slicer.util.arrayFromVolume(inputDTIVolume)
        proj_vol = slicer.util.arrayFromVolume(inputProjLabel)
        assoc_vol = slicer.util.arrayFromVolume(inputAssocLabel)

        proj_points = np.where( proj_vol != 0 )
        assoc_points = np.where( assoc_vol != 0)

        dti_proj_vals = dti_vol[proj_points]
        dti_assoc_vals = dti_vol[assoc_points]

        # DTI-ALPS calculation: mean(Dxx-proj, Dxx-assoc)/mean(Dyy-proj, Dzz-assoc)
        # Recall that the diffusion tensor ir represented as: 
        # D = [ Dxx Dxy Dxz
        #       Dyx Dyy Dyz
        #       Dzx Dzy Dzz ]
        dxx_proj = {
            "diff_value": 0,
            "points": 0
        }
        dyy_proj = {
            "diff_value": 0,
            "points": 0
        }
        dxx_assoc = {
            "diff_value": 0,
            "points": 0
        }
        dzz_assoc = {
            "diff_value": 0,
            "points": 0
        }
        for voxel in dti_proj_vals:
            dxx_proj["diff_value"] += voxel[0][0]
            dyy_proj["diff_value"] += voxel[1][1]
            dxx_proj["points"] += 1
            dyy_proj["points"] += 1

        for voxel in dti_assoc_vals:
            dxx_assoc["diff_value"] += voxel[0][0]
            dzz_assoc["diff_value"] += voxel[2][2]
            dxx_assoc["points"] += 1
            dzz_assoc["points"] += 1

        # DTI-ALPS index calculations
        mean_numerator = ((dxx_proj["diff_value"]/dxx_proj["points"])+(dxx_assoc["diff_value"]/dxx_assoc["points"]))/2.0
        mean_denominator = ((dyy_proj["diff_value"]/dyy_proj["points"])+(dzz_assoc["diff_value"]/dzz_assoc["points"]))/2.0
        
        return mean_numerator/mean_denominator

    def process(self,
                inputDTIVolume: vtkMRMLDiffusionTensorVolumeNode,
                inputProjLabel: vtkMRMLLabelMapVolumeNode,
                inputAssocLabel: vtkMRMLLabelMapVolumeNode,
                MNISpaceCheck: bool = False) -> None:
        """
        Run the processing algorithm.
        Can be used without GUI widget.
        :param inputDTIVolume: DTI volume to be the source of DTI-ALPS index calculation
        :param inputProjLabel: The Projection ROI area
        :param inputAssocLabel: The Association ROI area
        :param MNISpaceCheck: Informs if the input volume is in MNI space (2 mm) to use standard Proj/Assoc labels
        """

        if not MNISpaceCheck:
            if not inputDTIVolume or not inputProjLabel or not inputAssocLabel:
                raise ValueError("Input DTI, Projection and/or Association labels are not valid")

        import time
        startTime = time.time()
        logging.info('Processing started')

        if MNISpaceCheck:
            logging.info("MNI space processing started.")
            module_path = os.path.dirname(slicer.modules.dti_alps.path)

            proj_mni_label, assoc_mni_label = "", ""
            if not self.checkLabelNode("Projection-label-2mm-MNI"):
                proj_mni_label = slicer.util.loadNodeFromFile(module_path+os.path.sep+"Resources"+os.path.sep+"MNI"+os.path.sep+"Projection-label-2mm-MNI.nii.gz")
            else:
                proj_mni_label = slicer.util.getNode("Projection-label-2mm-MNI")

            if not self.checkLabelNode("Association-label-2mm-MNI"):
                assoc_mni_label = slicer.util.loadNodeFromFile(module_path+os.path.sep+"Resources"+os.path.sep+"MNI"+os.path.sep+"Association-label-2mm-MNI.nii.gz")
            else:
                assoc_mni_label = slicer.util.getNode("Association-label-2mm-MNI")

            logging.info("--> Checking if the input image shape is in MNI coordinates...")
            # Choosing one of labels to represent the MNI space (both are already in MNI space)
            if not self.checkMNISpaceInput(inputDTIVolume, proj_mni_label):
                logging.error("Input DTI image is not in MNI space. Please resample the input DTI image to MNI before calling this option.")
                raise ValueError("Input DTI image is not in MNI space. Please resample the input DTI image to MNI before calling this option.")
            
            logging.info("Calculating DTI-ALPS in MNI space...")
            self.dti_alps = self.calculateDTIALPS(inputDTIVolume, proj_mni_label, assoc_mni_label)
            logging.info(f'DTI-ALPS index: {self.dti_alps:.6f}')
            print("DTI-ALPS index: ", self.dti_alps)

            # Finish the process logic
            stopTime = time.time()
            logging.info(f'Processing completed in {stopTime-startTime:.2f} seconds')

            return True
        
        logging.info("Calculating DTI-ALPS in native space...")
        self.dti_alps = self.calculateDTIALPS(inputDTIVolume, inputProjLabel, inputAssocLabel) 
        logging.info("Calculating DTI-ALPS in native space...done")               

        logging.info(f'DTI-ALPS index: {self.dti_alps:.6f}')
        print("DTI-ALPS index: ", self.dti_alps)

        stopTime = time.time()
        logging.info(f'Processing completed in {stopTime-startTime:.2f} seconds')

        return True


#
# DTI_ALPSTest
#
class DTI_ALPSTest(ScriptedLoadableModuleTest):
    """
    This is the test case for your scripted module.
    Uses ScriptedLoadableModuleTest base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def setUp(self):
        """ Do whatever is needed to reset the state - typically a scene clear will be enough.
        """
        slicer.mrmlScene.Clear()

    def runTest(self):
        """Run as few or as many tests as needed here.
        """
        self.setUp()
        self.test_DTI_ALPS1()

    def test_DTI_ALPS1(self):
        """ Ideally you should have several levels of tests.  At the lowest level
        tests should exercise the functionality of the logic with different inputs
        (both valid and invalid).  At higher levels your tests should emulate the
        way the user would interact with your code and confirm that it still works
        the way you intended.
        One of the most important features of the tests is that it should alert other
        developers when their changes will have an impact on the behavior of your
        module.  For example, if a developer removes a feature that you depend on,
        your test should break so they know that the feature is needed.
        """

        self.delayDisplay("Starting the test")

        # Get/create input data

        import SampleData
        registerSampleData()
        inputVolume = SampleData.downloadSample('DTI_ALPS1')
        self.delayDisplay('Loaded test data set')

        inputScalarRange = inputVolume.GetImageData().GetScalarRange()
        self.assertEqual(inputScalarRange[0], 0)
        self.assertEqual(inputScalarRange[1], 695)

        outputVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode")
        threshold = 100

        # Test the module logic

        logic = DTI_ALPSLogic()

        # Test algorithm with non-inverted threshold
        logic.process(inputVolume, outputVolume, threshold, True)
        outputScalarRange = outputVolume.GetImageData().GetScalarRange()
        self.assertEqual(outputScalarRange[0], inputScalarRange[0])
        self.assertEqual(outputScalarRange[1], threshold)

        # Test algorithm with inverted threshold
        logic.process(inputVolume, outputVolume, threshold, False)
        outputScalarRange = outputVolume.GetImageData().GetScalarRange()
        self.assertEqual(outputScalarRange[0], inputScalarRange[0])
        self.assertEqual(outputScalarRange[1], inputScalarRange[1])

        self.delayDisplay('Test passed')
