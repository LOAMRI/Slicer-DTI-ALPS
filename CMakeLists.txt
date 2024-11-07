cmake_minimum_required(VERSION 3.16.3...3.27 FATAL_ERROR)

project(Slicer-DTI-ALPS)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "https://www.slicer.org/wiki/Documentation/Nightly/Extensions/DTI_ALPS")
set(EXTENSION_CATEGORY "Diffusion")
set(EXTENSION_CONTRIBUTORS "Antonio Senra Filho (State University of Campinas), André M. Paschoal (State University of Campinas)")
set(EXTENSION_DESCRIPTION "Module that calculates the diffusion tensor image analysis along the perivascular space (DTI-ALPS) index")
set(EXTENSION_ICONURL "https://www.slicer.org/w/img_auth.php/6/68/DTIALPS-logo.png")
set(EXTENSION_SCREENSHOTURLS "https://www.slicer.org/w/img_auth.php/f/f5/DTI-ALPS-sc-1.png https://www.slicer.org/w/img_auth.php/9/92/DTI-ALPS-sc-2.png https://www.slicer.org/w/img_auth.php/0/0b/DTI-ALPS-sc-3-proj-label.png https://www.slicer.org/w/img_auth.php/2/2f/DTI-ALPS-sc-4-assoc-label.png")
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
