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

### A version-compatibility gotcha we hit

`05_llm.def` installs `transformers`, `datasets`, `accelerate`, `bitsandbytes`, and `peft` with no version pins, so `pip` always grabs whatever is newest. That bit us on JURECA: the latest `transformers` at the time required `torch>=2.5`, but our base image (`pytorch/pytorch:2.4.0-...`) only had `torch 2.4.0` -- `transformers` didn't fail the build, it just silently disabled its PyTorch integration ("PyTorch was not found"), which defeats the point of the exercise. Fixed by bumping the base image to `pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime` (torch 2.6.0, still Ubuntu 22.04-based).

The `%test` block now also explicitly imports `torch` and asserts `transformers.utils.is_torch_available()`, so a future unpinned rebuild that drifts out of compatibility again fails loudly at `apptainer test` time instead of silently degrading. Since these libraries move fast, if you rebuild this months from now and hit a similar failure, pinning exact versions (`pip install "transformers==X.Y.Z" ...`) trades a bit of freshness for long-term reproducibility.

### Running the Example

```bash
apptainer exec --nv exercises/05_llm.sif python exercises/llm_training_script.py
```