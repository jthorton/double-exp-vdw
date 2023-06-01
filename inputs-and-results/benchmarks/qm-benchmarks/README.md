# QM Benchmarks on optimized geometries

The benchmark scripts from Lim-Hahn's work (as mentioned in acknowledgment) as adapted in the Sage fitting repo, https://github.com/openforcefield/openff-sage/tree/main/inputs-and-results/benchmarks/qc-opt-geo, were used here. Additional slurmscripts are provided to run them on a HPC cluster, and the outputs were also attached. Some changes in the scripts include the application of an element filter to exclude {F, P, S, I} from the benchmark set (the QCArchive reference name for the benchmark set is `OpenFF Industry Benchmark Season 1 v1.1`).


This directory contains the scripts needed to compute the ddE, RMSD, and TDF metrics for a set
of force fields against a QCArchive optimization data collection such as the `OpenFF Full Optimization Benchmark 1` 
QCArchive data set as was used in the [Lim and Hahn study](https://doi.org/10.26434/chemrxiv.12551867.v2) (see the 
Acknowledgments section below for more details).

## Running the benchmarks

1) Run the `01-setup.py` script to retrieve the relevant QC data from the QCArchive and filter out
   and incomplete or undesirable (e.g. records whereby the molecule connectivity changed during 
   the QM minimization) records. The dataset to retrieve and benchmark against must be specified.
   For the Lim and Hahn study:
   
   ```shell
   python 01-setup.py "OpenFF Full Optimization Benchmark 1"
   ```
   
   or for the Industrial partner benchmarks:

   ```shell
   python 01-setup.py "OpenFF Industry Benchmark Season 1 v1.1"
   ```

2) 

    a. Run the `02-a-chunk-qm.py` script to split the `01-processed-qm.sdf` file produced by step 1) into
       many smaller chunks. This allows the next step to be parallelized across many different CPUs / workers.
       By default the split chuncks will be stored in a new `02-chunks` directory.

    b. Perform an MM energy minimization for each of the chunked files and for each force field of interest, e.g.:

   ```shell
   python 02-b-minimize.py -ff openff-2.0.0.offxml \ 
                           -i 02-chunks/01-processed-qm-1.sdf \
                           -o 02-outputs/openff-2-0-0-1.sdf
   ```

3) a. Using the MM minimized structures from step 2 compute the metrics RMSD/ddE/TFD.

   ```shell
   python 03-a-compute-metrics.py --input "03-force-fields.json" --index 1 \
               --output 03-outputs/03-metrics-1.csv
   ```
   b. Concatenate the metrics files in csv format generated above 
   ```shell
   python 03-b-join-metrics.py 03-outputs/* -o 03-metrics.csv
   ```

4) Plot the metrics by running the `04-plot-metrics.py` script, which will be stored in `04-outputs`. The directory `04-outputs/full` contains the metrics on overall set and the other directories are subsets of R-groups.

# File Manifest

 01-processed-qm.json - File containing the exact optimization record ids used in this benchmark.
 01-processed-qm.sdf.tar.gz - SDF file of the QM optimized final geometries for the corresponding records in the json file.
 01-setup.py - Script to download and process the QM from QCArchive using `openff-qcsubmit`.
 02-a-chunk-qm.py - Script to split the SDF file containing QM geometries into chunks for parallel MM optimizations.
 02-chunks.tar.gz - Compressed directory that contains the QM chunk files created.
 02-outputs.tar.gz - Compressed directory that contains the MM optimizations of forcefields mentioned in `03-force-fields.json` file.
 03-a-compute-metrics.py - Script to compute the metrics RMSD/TFD/ddE using the QM and MM optimized final geometries.
 03-b-join-metrics.py - Script to combine the metrics from the chunks of csv files.
 03-force-fields.json - File containing the force field and geometry file paths.
 03-metrics.csv - Combined metrics file that contains RMSD/TFD/ddE data for all the conformers in the benchmark set.
 03-outputs.tar.gz - Compressed directory that contains the metrics evaluated in csv files for respective chunks of data.
 04-outputs/ - Directory that contains the plot outputs from the script `03-plot-metrics.py`.
 04-plot-metrics.py - Script to plot the metrics RMSD/TFD/ddE on the whole dataset and on subsets of R-groups.
 slurmscript-step02-b-03-a - Slurm script to run the MM optimizations in parallel as an array job and compute the metrics with the optimized geometries.
 slurmscript-step03b-04 - Slurm script to combine the metrics files and plot the metrics.


## Acknowledgments

The scripts in this directory are based off of those found in the `benchmarkff` repository
at commit hash [`6351878`](https://github.com/MobleyLab/benchmarkff/tree/6351878) which was produced 
by Victoria Lim under the following license:

    MIT License
    
    Copyright (c) 2019 Victoria Lim
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.


