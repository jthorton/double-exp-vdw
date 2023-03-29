# Physical Property Benchmark Data Sets

The benchmark experimental solvation/ transfer free energy physical property datasets were curated by filtering those 
used in the [OpenFF-Sage](https://github.com/openforcefield/openff-sage/tree/2.0.0-rc.1/data-set-curation/physical-property/benchmarks) paper.
The datasets were filtered to only include elements which were covered by the training data, that is `H, C, N, O, Cl, Br`.

We have included:

- `fsolv-filtered.json`: An `openff-evaluator` style dataset of hydration free energies taken from FreeSolv
- `filtered-mnsol.txt`: A text file describing a non-aqueous solvation energy extracted from the Minnesota Solvation Database, the value is not included due to license issues.
- 
