#!/bin/bash
#
# Set the job name and wall time limit
#BSUB -J dexpfe[1-469]%60
#BSUB -W 11:00
#
# Set the output and error output paths.
#BSUB -o  %J.o
#BSUB -e  %J.e
#
# Set any gpu options.
#BSUB -q gpuqueue
#BSUB -gpu num=1:j_exclusive=yes:mode=shared:mps=no:
#
#BSUB -M 5

# Enable conda
. ~/.bashrc

conda activate double-exp-vdw
conda env export > "conda-env.yml"

# Launch my program.
module load cuda/11.0
export OPENMM_CPU_THREADS=1

python ../run-calculation.py --input schemas/$LSB_JOBINDEX --force-field force-field.offxml
