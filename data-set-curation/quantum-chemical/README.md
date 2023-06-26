# Quantum Chemical Data Sets

This directory contains the scripts used to curate the different quantum chemical *training* sets from
data stored in the [QCArchive](https://qcarchive.molssi.org/), as well as the final curated data sets.

**Note**: As the QCArchive is a constantly evolving and updating collection it is possible that running the
          scripts provided here will yield slightly different curated collections depending on if new results
          have become available. For full reproducibility we have in the `data-sets` directory provided JSON
          records which encode the **exact** ids of QC record used during training. The JSON is an [OpenFF-QCSubmit](https://docs.openforcefield.org/projects/qcsubmit/en/latest/api.html#results) 
results object.

## Curating the data sets
- `Dataset-curation-FB-input-creation-notebook.ipynb`: Build the training datasets from QCArchive using `openff-qcsubmit` and the dataset curation tools. Set up the folders and inputs required for the valence optimization via ForceBalance.

## Curated data sets

- `reduced-set-opt-set.json`: A dataset of optimised geometries.
- `reduced-set-td-set.json`: A dataset of torsion drives for proper torsions.
- `*smirks.json`: List of smirks of the parameters to be optimized.

## ForceBalance sample run

`toy-fb-run`: This directory contains a sample run of forcebalance forcefield fitting run with two targets. It is advised to run the full FB optimization on a HPC cluster, using slurmscripts (or equivalent queue management package). The ForceBalance inputs for all the optimization runs were provided in `/inputs-and-results/training`.
