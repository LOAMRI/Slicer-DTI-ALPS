cmake_minimum_required(VERSION 3.16.3...3.19.7 FATAL_ERROR)

project(DTI ALPS Index)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://www.slicer.org/wiki/Documentation/Nightly/Extensions/DTI_ALPS")
set(EXTENSION_CATEGORY "Diffusion")
set(EXTENSION_CONTRIBUTORS "Antonio Senra Filho (State University of Campinas), André M. Paschoal (State University of Campinas)")
set(EXTENSION_DESCRIPTION "Module to calculate the diffusion tensor image analysis along the perivascular space (DTI-ALPS)")
set(EXTENSION_ICONURL "https://www.example.com/Slicer/Extensions/DTI_ALPS.png")
set(EXTENSION_SCREENSHOTURLS "https://www.example.com/Slicer/Extensions/DTI_ALPS/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a list or "NA" if no dependencies

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(DTI_ALPS)
add_subdirectory(DTI_ALPS)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
