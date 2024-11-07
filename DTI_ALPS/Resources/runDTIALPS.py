import argparse
import os
import sys

import numpy as np

# Instantiate the parser
parser = argparse.ArgumentParser(description="Python script to facilitate calling DTI-ALPS module from command line. \n"+ 
                                 "This script calls the Slicer module Python code and all the funcionalities are described in the wiki page: "+
                                 "https://slicer-dti-alps.readthedocs.io/en/latest/")

parser.add_argument("inputDTI", type=str,
                    help="Input DTI image file path")
parser.add_argument("inputProjLabel", type=str, nargs='?',
                    help="Input image label that defines de Projection ROI in the DTI image space")
parser.add_argument("inputAssocLabel", type=str, nargs='?',
                    help="Input image label that defines de Association ROI in the DTI image space")
parser.add_argument("--MNISpace", action='store_true',
                    help="Informs whether the input DTI image is already in the MNI space (2 mm resolution). If yes, the input Proj/Assoc paths are changed for the standard MNI labels instead.")
parser.add_argument("--verbose", action='store_true',
                    help="Show more details thoughout the processing.")


args = parser.parse_args()

# Show input details
if args.verbose:
    print("-- DTI-ALPS Initiation:")
    print("Input parameters:")
    print(f"  1. Input DTI: {args.inputDTI}")
    if not args.MNISpace:
        print(f"  2. Input Projection label: {args.inputProjLabel}")
        print(f"  3. Input Association label: {args.inputAssocLabel}")
    else:
        print("  2. Input Projection label: Used MNI standard (--MNISpace is True)")
        print("  3. Input Association label: Used MNI standard (--MNISpace is True)")
    print(f"  4. MNISpace: {args.MNISpace}")


# General variables
module_path = os.path.dirname(slicer.modules.dti_alps.path)
inputDTI = ""
inputProjLabel = ""
inputAssocLabel = ""
dti_alps_obj = slicer.modules.dti_alps.widgetRepresentation().self()

dti_alps_idx = 0


# Load the input data
if args.verbose:
    print("-- DTI-ALPS: Load data")
    print("  1. Load DTI volume...", end="", flush=True)
inputDTI = slicer.util.loadVolume(args.inputDTI)
if args.verbose:
    print("done")

if args.verbose:
    print("-- DTI-ALPS: Load data")
    print("  1. Load Projection and Association label volumes...", end="", flush=True)
if not args.MNISpace:
    inputProjLabel = slicer.util.loadLabelVolume(args.inputProjLabel)
    inputAssocLabel = slicer.util.loadLabelVolume(args.inputAssocLabel)
else:
    inputProjLabel = slicer.util.loadLabelVolume(module_path+os.path.sep+"Resources"+os.path.sep+"MNI"+os.path.sep+"Projection-label-2mm-MNI.nii.gz")
    inputAssocLabel = slicer.util.loadLabelVolume(module_path+os.path.sep+"Resources"+os.path.sep+"MNI"+os.path.sep+"Association-label-2mm-MNI.nii.gz")
if args.verbose:
    print("done")

# Check if input data is in MNI space 2mm
if args.MNISpace:
    if args.verbose:
        print("-- Check input and MNI spacing...", end="", flush=True)
    isMNI = dti_alps_obj.logic.checkMNISpaceInput(inputDTI,inputProjLabel)
    if not isMNI:
        print("ERROR: Input DTI is not in MNI space 2mm")
        sys.exit(1)
    if args.verbose:
        print("done")

# Call Slicer DTI-ALPS module
if args.verbose:
    print("-- DTI-ALPS index calculation")
    print("  1. Calling Slicer DTI-ALPS module...", end="", flush=True)

# Call the DTI-ALPS calculation method
dti_alps_idx = dti_alps_obj.logic.calculateDTIALPS(inputDTI, inputProjLabel, inputAssocLabel)
if args.verbose:
    print("done")

# Output result
print(f"DTI-ALPS index = {dti_alps_idx}")

sys.exit(0)