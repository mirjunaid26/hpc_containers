#!/bin/bash
#SBATCH --job-name=matmul-cpu-scratch
#SBATCH --account=training2638
#SBATCH --partition=dc-cpu
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16
#SBATCH --time=00:10:00
#SBATCH --output=matmul_%j.log

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

IMAGES_DIR=/p/project1/training2638/container-workshop/02_building
SCRIPT_DIR=/p/project1/training2638/container-workshop/03_running_on_hpc

apptainer exec \
    "${IMAGES_DIR}/ml_gpu.sif" \
    python "${SCRIPT_DIR}/matmul_cpu.py" --size 4000 --repeats 3
