#!/bin/bash
# prefetch_model.sh — run this ONCE from a JURECA LOGIN node (not via sbatch)
# before submitting job_gpu_llm.slurm.
#
# Why: JURECA compute nodes (where job_gpu_llm.slurm actually runs) have no
# general internet access -- only login nodes do. distilgpt2 has to be
# downloaded here, into the same HF_HOME the Slurm job will read from, so the
# job itself can run fully offline.
set -euo pipefail

export HF_HOME="$PWD/hf_cache"
mkdir -p "$HF_HOME"

echo "Caching distilgpt2 into $HF_HOME ..."
apptainer exec ../02_building/llm.sif python -c "
from transformers import AutoModelForCausalLM, AutoTokenizer
AutoTokenizer.from_pretrained('distilgpt2')
AutoModelForCausalLM.from_pretrained('distilgpt2')
print('distilgpt2 cached successfully.')
"

echo "Done. You can now submit: sbatch job_gpu_llm.slurm"
