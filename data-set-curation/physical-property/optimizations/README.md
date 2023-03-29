# Physical Property Optimization Data Sets

The data is sourced from the [ThermoML archive](https://www.nist.gov/mml/acmd/trc/thermoml) using the 
`openff-evaluator` packages data curation tools.

## Curating the Sage and water data set

Run the `curate-water-data-set.py` to extract pure water densities from `ThermoML archive` across a range of temperatures to be combined with the [OpenFF-Sage](https://github.com/openforcefield/openff-sage/tree/main/data-set-curation/physical-property/optimizations) training datasets to create `data-sets/sage-and-water-rho.json`.
