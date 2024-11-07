cmake_minimum_required(VERSION 3.16.3...3.27 FATAL_ERROR)

project(Slicer-DTI-ALPS)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://slicer-dti-alps.readthedocs.io/en/latest/")
set(EXTENSION_CATEGORY "Diffusion")
set(EXTENSION_CONTRIBUTORS "Antonio Senra Filho (State University of Campinas), André M. Paschoal (State University of Campinas)")
set(EXTENSION_DESCRIPTION "Slicer extension to provide a module that calculates the diffusion tensor image analysis along the perivascular space (DTI-ALPS) index")
set(EXTENSION_ICONURL "https://raw.githubusercontent.com/LOAMRI/Slicer-DTI-ALPS/main/DTI_ALPS.png")
set(EXTENSION_SCREENSHOTURLS
  "https://raw.githubusercontent.com/LOAMRI/Slicer-DTI-ALPS/refs/heads/main/docs/assets/DTI-ALPS-NMO-patients.png"
  "https://raw.githubusercontent.com/LOAMRI/Slicer-DTI-ALPS/refs/heads/main/docs/assets/DTI-ALPS-sc-2.png"
)
set(EXTENSION_DEPENDS "NA") # Specified as a list or "NA" if no dependencies

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(DTI_ALPS)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
