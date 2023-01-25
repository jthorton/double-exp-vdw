1. `dexp-valence-fit`: valence parameters refit for the output FF from optimized double exponential non-bonded parameters, which were trained on Sage empirical data which includes all elements except for {F, P, S, I}.

2. `dexp-valence-fit-scale14-optimized`: scaling factor `scale14` optimized along with other valence parameters from `dexp-valence-fit`, on the same set of training targets.

3. `sage-refit`: Sage refit on the same reduced set of training targets as in 1 (reduced set here means excluding elements {F, P, S, I}).

# Optimizations


Contained within this directory are the main inputs (or instructions on how they may be generated)
for training the matrix of force fields against both physical property and QC data.

Currently, the inputs for the vdW fits against physical property data sets are provided, while the
inputs for the valence fits will need to be generated manually due to their size.

## Running the vdW fits

Each of the physical property fits can be re-run using the

```shell
nonbonded optimization run --restart true
```

command. The ``--restart true`` flag will ensure that the optimization is correctly restarted if you
are trying to continue from a previous attempt which failed for whatever reason.

The outputs of the fit can be analyzed and plotted using:

```shell
nonbonded optimization analyze
nonbonded optimization plot
```

which will produce a set of analyzed outputs in a new `analysis` directory, and a set of corresponding
plots, including a trace of the objective function and RMSE metrics from before and after the fit, will
be generated in a new `plots` directory.
