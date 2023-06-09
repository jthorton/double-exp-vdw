Double exponential vdW functional form 
======================================

This repository contains the scripts, inputs and the results generated as part of the study **A transferable double exponential potential for condensed phase simulation of small molecules.**
The pre-print is freely available at https://doi.org/10.26434/chemrxiv-2023-28r9s


### Structure

This repository is structured into three main directories:

* `data-set-curation` - contains the scripts used to curate the training and test data sets as well as the final test sets.

* `inputs-and-results` - contains the *most up to date* input files required to reproduce this study and the associated output files.
  
* `scripts` - contains the scripts used to generate the input schemas / files, and scripts which perform ancillary data 
  analysis.

### Experimental Data Sets

The experimental data sets used in this project were curated from the [NIST ThermoML](https://trc.nist.gov/ThermoML.html)
archive [FreeSolv](https://github.com/MobleyLab/FreeSolv) and the [Minnesota Solvation Database](https://conservancy.umn.edu/handle/11299/213300).

## Reproducibility

For those looking to reproduce any part of the study, 
the required dependencies are listed in the [environment](environment.yaml) file and can be installed into a virtual environment via conda:

```shell
conda env create --file environment.yaml
```

The environment must then be activated before the scripts can be used:
```shell
conda activate dexp-env
```
To deactivate the environment use:
```shell
conda deactivate
```
Finally, the environment can be removed via:
```shell
conda remove -n dexp-env --all
```

For more information on installing the conda package manager and virtual environments see the conda [guide](https://conda.io/projects/conda/en/latest/user-guide/install/index.html#installation).
