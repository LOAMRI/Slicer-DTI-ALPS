# Slicer Diffusion Tensor Image Analysis Along the Perivascular Space (DTI-ALPS)

![project logo](../DTI_ALPS.png){ width="250" .center}

Welcome to the Slicer Diffusion Tensor Image Analysis Along the Perivascular Space (DTI-ALPS)!

This 3D Slicer extension was designed to assist users in processing Diffusion Tensor Imaging (DTI) for the `DTI-ALPS` index calculation. 


The full documentation of the usage, implementation and updates in the `DTI-ALPS` index is given in this repository and posted online using a [web-based host](https://slicer-dti-alps.readthedocs.io/en/latest/). 

## Output examples

The `Slicer DTI-ALPS` extension is a simple way to collect the `DTI-ALPS` index using a GUI interface. The images below represents some examples:

![DTI-ALPS example](assets/DTI-ALPS-NMO-patients.png){ width="600" .center}
DTI-ALPS index application in evaluating Neuromyelitis optica (NMO) patients

![GUI example](assets/DTI-ALPS-sc-2.png){ width="600" .center}
DTI-ALPS index GUI that simplify the image parameters and methods calculation

## Modules

### DTI-ALPS

This module is able to calculate the `DTI-ALPS` index from a standard Diffusion-Tensor (DTI) MRI image. In this case, it is needed to use the tensorial image that was already reconstructed by other toolkit. For instance, the 3D Slicer `DMRI Diffusion` extension can assist you to collect the DTI image for this step.


## Cite this tool

We hope that the `DTI-ALPS` can be helpful for your applications. If possible, recall to cite at least one of the following publications:

* Senra Filho, A. C. da S.; Paschoal, A. M. "DTI-ALPS index as complementary information for Neuromyelitis Optica patients: a preliminary evaluation". ISMR & ISMRT Annual Meeting (2025)

## License

This project is under MIT license and following details are given at the [LICENSE](https://github.com/LOAMRI/Slicer-DTI-ALPS/blob/main/LICENSE) file in the project repository.