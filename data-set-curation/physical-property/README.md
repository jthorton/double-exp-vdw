# Physical Property Data Sets


This directory contains a Jupyter notebook ([physical-data-set-curation.ipynb](physical-data-set-curation.ipynb)) which can be used to generate the physical property optimisation and benchmarking datasets.

## Physical data sets Manifest
These datasets are provided for reproducibility and are the exact versions used in the training and benchmarking of the DE-FF.

- [sage-train-v1.json](physical-data-sets/sage-train-v1.json) - A [Nonbonded](https://github.com/SimonBoothroyd/nonbonded) dataset containing the physical properties used to train the OpenFF Sage force field.
- [pure_water_rho.json](physical-data-sets/pure_water_rho.json) - A Nonbonded dataset of pure water densities. 
- [sage_and_water_rho.json](physical-data-sets/sage_and_water_rho.json) - A [OpenFF-Evaluator](https://github.com/openforcefield/openff-evaluator) dataset of sage and pure water training data.
- [sage-fsolv-test-v1.json](physical-data-sets/sage-fsolv-test-v1.json) - A Nonbonded dataset of hydration free energies used to benchmark the Openff Sage force field extracted from [FreeSolv](https://github.com/MobleyLab/FreeSolv).
- [fsolv-filtered.json](physical-data-sets/fsolv-filtered.json) - A filtered version of the OpenFF Sage FreeSolv test set for the DE-FF in OpenFF-Evaluator format.
- [filtered-mnsol.txt](physical-data-sets/filtered-mnsol.txt) - A text file containing the ids and substances of non-aqueous solvation free energies extracted from MNsol and used to benchmark the DE-FF.

