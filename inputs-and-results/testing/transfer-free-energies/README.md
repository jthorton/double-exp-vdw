# Transfer free energies

Scripts required to run the aqueous / non-aqueous solvation free energies with the `absolv` package are included.

- [setup-transfer.py](setup-transfer.py): Build the schemas and directories required by `absolv` to run the solvation calculations, this also sets the lambda scaling.
- [run-calculation.py](run-calculation.py): Run the calculation given a directory path.
- [plot_transfer_free_energies.ipynb](plot_transfer_free_energies.ipynb): A notebook to gather the results of the absolv calculations and run the analysis and generate figures.

# Results
Aggregated results of the DE-FF solvation/transfer free energy calculation are included as csv files due to the size of the individual outputs.

## File format

The csv files provide a single result per line and include the smiles strings and role of each molecule in the mixture along with the DE-FF calculated free energy and uncertainty.
- [dexp-hydration.csv](dexp-hydration.csv): DE-FF hydration free energies calculated for the [filtered FreeSolv dataset](../../../data-set-curation/physical-property/physical-data-sets/fsolv-filtered.json)
- [dexp-mnsol.csv](dexp-mnsol.csv): DE-FF non-aqueous solvation free energies calculated for the substances from the [MNSol dataset](../../../data-set-curation/physical-property/physical-data-sets/filtered-mnsol.txt)
- [dexp-transfer.csv](dexp-transfer.csv): DE-FF transfer free energies from the combined aqueous and non-aqueous solvation free energy datasets.