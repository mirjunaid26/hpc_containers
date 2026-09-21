#!/bin/bash
#SBATCH --job-name=llm-train
#SBATCH --account=training2638
#SBATCH --partition=dc-gpu
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --time=00:30:00
#SBATCH --output=llm_train_%j.log

# Keep HuggingFace downloads off $HOME (quota) -- see 05_llm_training.md.
# Must match the HF_HOME used by prefetch_model.sh.
export HF_HOME=$PWD/hf_cache

# Compute nodes on this cluster have no internet -- run prefetch_model.sh
# from a login node BEFORE submitting this job, then force offline mode so
# this job never even tries to reach huggingface.co.
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1

apptainer exec --nv ../02_building/llm.sif python llm_training_script.py
