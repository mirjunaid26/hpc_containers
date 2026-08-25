# HPC Containers

Welcome to the advanced Apptainer (formerly Singularity) tutorial. This guide is designed for High Performance Computing (HPC) users, System Admins, and Data Scientists who want to leverage containers for reproducible research.

## Prerequisites
- Basic familiarity with Linux command line.
- Access to a system with Apptainer installed (or Singularity).
- Basic understanding of what a container is (e.g., Docker experience is helpful but not required).

## Table of Contents

1. [Basics & Fundamentals](01_basics.md)
   - Understanding Apptainer architecture.
   - Converting Docker containers.
   - Interactive vs Batch execution.

2. [Python Environment Management](02_python_envs.md)
   - Building custom Python environments.
   - Conda vs System packages.
   - Best practices for image size.

3. [Advanced Definition Files](03_advanced_def.md)
   - The anatomy of a `.def` file.
   - `%post`, `%environment`, `%runscript`, `%test` sections.
   - Multi-stage builds.

4. [HPC Integration (GPU & MPI)](04_hpc_gpu.md)
   - Using NVIDIA GPUs (`--nv`).
   - MPI Support and Bind Paths.
   - Running on Slurm/PBS.

5. [LLM Training on HPC](05_llm_training.md)
   - Setup for HuggingFace & NVIDIA.
   - Cache management.
   - Distributed training basics.

## Exercises

You will find hands-on exercises in the `exercises/` directory. Each module will reference specific files there.
