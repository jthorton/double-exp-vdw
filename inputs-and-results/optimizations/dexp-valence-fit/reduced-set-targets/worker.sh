#!/usr/bin/env bash
#SBATCH -J fit-worker
#SBATCH -p free
#SBATCH -t 24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=3gb
#SBATCH --array=1-100
#SBATCH --account dmobley_lab
#SBATCH --export ALL
#SBATCH -o worker_logs/slurm-%A_%a.out
#SBATCH --requeue

# the max jobs for my user is 150
source $HOME/.bashrc
conda activate /dfs6/pub/pbehara/bin/conda/smirnofee
host="$(cat ./host)"
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1

tmpdir=/dev/shm/pbehara/fb-worker
mkdir -p $tmpdir
for i in $(seq  $SLURM_NTASKS ); do
	
	work_queue_worker --cores 1 -s $(mktemp -d -p $tmpdir ) --memory=$(( 4096 * 2 )) --gpus=0 $host 55145 &
done
wait
