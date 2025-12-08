# Module 5: Training Large Language Models (LLMs)

Training LLMs on HPC requires careful management of large models, datasets, and massive GPU resources. Apptainer is excellent for this because it allows you to bring a consistent software stack (PyTorch, Drivers, Helper libraries) to the cluster.

## 1. The Base Image: NVIDIA NGC

For LLMs, we highly recommend starting with NVIDIA's NGC containers. They come optimized with PyTorch, CUDA, cuDNN, and often Transformer libraries.

```singularity
Bootstrap: docker
From: nvcr.io/nvidia/pytorch:23.08-py3
```

## 2. Managing HuggingFace Cache

HuggingFace models (like Llama-2, Mistral) are large. By default, they download to `~/.cache/huggingface`. In HPC, your `$HOME` often has a quota.

**Solution**: Use a bind path to a scratch directory.

```bash
mkdir -p /scratch/user/hf_cache
export HF_HOME=/scratch/user/hf_cache
# Or bind it at runtime
apptainer exec --bind /scratch/user/hf_cache:/root/.cache/huggingface llm_container.sif python train.py
```

## 3. Distributed Training (Accelerate / Deepspeed)

When using multiple GPUs (often required for LLMs), you need to ensure the container can see all of them and communicate.

- **MPI**: If using multi-node training.
- **Torch Distributed**: Often just works if `--nv` is passed and all GPUs are visible.

## Exercise: LLM Setup

We will build a container ready for fine-tuning a model using `bitsandbytes` (quantization) and `PEFT` (Parameter-Efficient Fine-Tuning).

See `exercises/05_llm.def`.

### Running the Example

```bash
apptainer exec --nv exercises/05_llm.sif python exercises/llm_training_script.py
```
