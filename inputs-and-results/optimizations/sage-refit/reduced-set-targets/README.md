# Valence parameters fit

Fitting the valence parameters after obtaining the optimized double-exp-vdW terms from the non-bonded parameters fit. These are the inputs of a forcebalance forcefield fitting run generated using the scripts in `data-set-curation/quantum-chemical`. The targets include optimized geometries with the objective to reduce the differences between the QM and MM internal coordinates, and torsion profile targets with the objective to reduce the disagreement between the torsion energy profiles.

# File Manifest

 forcefield - Directory containing the initial forcefield.
 optimize.in - Input file detailing the optimization hyperparameters and the targets to be used in fitting, their paths.
 result - Directory containing the final optimized forcefield.
 slurm_output.tar.gz - Compressed output of the forcefield fitting run.
 targets.tar.gz - Compressed directory containing the QM targets used in fitting this forcefield.
