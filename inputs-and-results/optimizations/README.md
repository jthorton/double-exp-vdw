# Optimizations


Contained within this directory are the main inputs (or instructions on how they may be generated)
for training the matrix of force fields against both physical property and QC data.

Currently, the inputs for the vdW fits against physical property data sets are provided, while the
inputs for the valence fits will need to be generated manually due to their size.

Optimizations and their description:
1. `dexp-valence-fit`: Valence parameters refit for the output of `dexp-all-fit`, dataset includes all elements except for {F, P, S, I}.

2. `dexp-valence-fit-scale14-optimized`: Same as `dexp-valence-fit` but also optimizes the 1-4 non-bonded scale factor `scale14`.

3. `sage-refit`: Sage (LJ) refit on the same reduced set of training targets as in `dexp-valence-fit` (reduced set here means excluding elements {F, P, S, I}).

4. `dexp-tip4p-b68`: Non-bonded fitting of the DE-TIP4P water model using ForceBalance for a reduced set of targets
starting from a curve fit of the B68 model. 

5. `dexp-all-fit`: Non-bonded fitting of the DE general force field including the optimised DE-TIP4P-B68 water model.