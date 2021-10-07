Double exponential vdW functional form 
======================================

This repository contains the scripts, inputs and the results generated as part of the *...* publication.

**Warning:** This repository, its structure and contents, are currently in a state of flux and incompleteness while the 
study is ongoing. We *do not* guarantee the scientific correctness of anything found within, nor do we yet recommend 
using any force field parameters found here.

### Structure

This repository is structured into four main directories:

* `data-set-curation` - contains the script used to curate the training and test data sets.

* `inputs-and-results` - contains the *most up to date* input files required to reproduce this study. **See the Reproduction** section of this README for more information. The project structure was for the most part generated automatically using the [`nonbonded`](https://github.com/SimonBoothroyd/nonbonded) package.
  
* `schema` - contains schemas which define most parts of the project, including definitions of
  which optimizations and benchmarks were performed.
  
* `scripts` - contains the script used to generate the input schemas / files, and scripts which perform ancillary data 
  analysis.

### Experimental Data Sets

The experimental data sets used in this project were curated from the [NIST ThermoML](https://trc.nist.gov/ThermoML.html)
archive. The citations for the individual measurements can be found in `DATA_CITATIONS.bib` 

### Reproduction

The exact inputs used and outputs reported (including the conda environment used to generate them) in the publication 
have been included as tagged releases to this repository. 

For those looking to reproduce the study, the required dependencies may be obtained directly using conda:

```bash
conda env create --name double-exp-vdw --file environment.yaml
```

#### Optimizations

In most cases the optimizations can be re-run using the following commands

```bash
cd inputs-and-results/optimizations/XXX/
nonbonded optimization run
nonbonded optimization analyze
```

while the QM optimizations may be re-run, e.g., according to

```bash
cd inputs-and-results/optimizations/vdw-v1-td-opt-vib-v1/
ForceBalance optimize.in
``` 

A more complete set of instructions for performing QM fits with ForceBalance can be found [here](https://github.com/openforcefield/openforcefield-forcebalance)

#### Benchmarks

A comprehensive set of instructions for re-running the benchmarks can be found in the `inputs-and-results/benchmarks` 
directory.