#!/bin/bash
#SBATCH -J dexp
#SBATCH -p standard
#SBATCH -t 200:00:00
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=10000mb
#SBATCH --account dmobley_lab
#SBATCH --export ALL
#SBATCH --mail-user=pbehara@uci.edu
#SBATCH --tmp=20GB



source $HOME/.bashrc
conda activate /dfs6/pub/pbehara/bin/conda/smirnofee


export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1

ForceBalance.py optimize.in

echo "All done"
