#!/bin/bash
# a sample job submission script to submit an MPI job to the sandyb partition on Midway1
# please change the --partition option if you want to use another partition on Midway1

# set the job name to day3ex
#SBATCH --job-name=day3ex

# send output to day3ex.out
#SBATCH --output=day3ex.out

# receive an email when job starts, ends, and fails
#SBATCH --mail-type=BEGIN,END,DAIL

# this job requests 4 cores. Cores can be selected from various nodes.
#SBATCH --ntasks=4

# there are many partitions on Midway1 and it is important to specify which
# partition you want to run your job on. Not having the following option, the
# sandby partition on Midway1 will be selected as the default partition
#SBATCH --partition=sandyb

# load the openmpi module
module load openmpi

# Run the process with mpirun. Notice -n is not required. mpirun will
# automatically figure out how many processes to run from the slurm options
mpirun ./broadcast.cpp.exec
mpirun ./allreduce.cpp.exec
mpirun ./scatter.cpp.exec
mpirun ./pimpi.cpp.exec
