#!/bin/bash
# a sample job submission script to submit an MPI job to the sandyb partition on Midway1

# set the job name to Black Scholes
#SBATCH --job-name=black_scholes

# send output to bs.out
#SBATCH --output=bs.out

# receive an email when job starts, ends, and fails
#SBATCH --mail-type=BEGIN,END,DAIL

# this job requests node
#SBATCH --ntasks=1

# and request 8 cpus per task for OpenMP threads
#SBATCH --cpus-per-task=8


# set OMP_NUM_THREADS to the number of --cpus-per-task we asked for
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

# Run the process with mpirun. Notice -n is not required. mpirun will
# automatically figure out how many processes to run from the slurm options
### openmp executable
./BSpar.cpp.exec
