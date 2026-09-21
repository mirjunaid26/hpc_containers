#!/bin/bash
#SBATCH --job-name=matmul-cpu-scratch
#SBATCH --account=training2638
#SBATCH --partition=dc-cpu
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16
#SBATCH --time=00:10:00
#SBATCH --output=matmul_%j.log

apptainer exec ../02_building/conda.sif python3 matmul_cpu.py
