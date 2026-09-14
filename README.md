# HPC Containers

Welcome to the advanced Apptainer (formerly Singularity) tutorial. This guide is designed for High Performance Computing (HPC) users, System Admins, and Data Scientists who want to leverage containers for reproducible research.

Originally written for a 3-hour hands-on workshop ("Containerizing HPC Workflows with Singularity and Apptainer"), split into two 90-minute sessions.

## Prerequisites
- Basic familiarity with Linux command line.
- Access to a system with Apptainer installed (or Singularity).
- Basic understanding of what a container is (e.g., Docker experience is helpful but not required).

## Workshop materials layout

The hands-on materials are organized into three modules, matching the structure participants get on the cluster:

```
container-workshop/
├── 01_interacting/
│   ├── data/
│   │   └── test.txt
│   └── images/
│       ├── python.sif
│       ├── ubuntu.sif
│       └── ubuntu_22.04.sif
├── 02_building/
│   ├── 01_hello.def    hello.sif
│   ├── 02_conda.def    conda.sif
│   ├── 03_complex.def  complex.sif
│   ├── 04_ml_gpu.def   ml_gpu.sif
│   └── 05_llm.def      llm.sif
└── 03_running_on_hpc/
    ├── job_gpu_llm.slurm
    ├── job_cpu_matmul.slurm
    ├── llm_training_script.py
    └── matmul_cpu.py
```

`01_interacting/` and `02_building/` ship pre-built `.sif` images alongside their source so you can either build from scratch or jump straight to running. `03_running_on_hpc/` assumes the containers in `02_building/` already exist (its Slurm scripts reference them via relative paths, e.g. `../02_building/llm.sif`).

## Table of Contents

1. [Basics & Fundamentals](01_basics.md) — Module 1: Interacting
   - Understanding Apptainer architecture.
   - Converting Docker containers.
   - Interactive vs Batch execution.

2. [Python Environment Management](02_python_envs.md) — Module 2: Building
   - Building custom Python environments.
   - Conda vs System packages.
   - Best practices for image size.

3. [Advanced Definition Files](03_advanced_def.md) — Module 2: Building
   - The anatomy of a `.def` file.
   - `%post`, `%environment`, `%runscript`, `%test` sections.
   - Multi-stage builds.

4. [HPC Integration (GPU & MPI)](04_hpc_gpu.md) — Module 2/3: Building & Running
   - Using NVIDIA GPUs (`--nv`).
   - MPI Support and Bind Paths.
   - Running on Slurm/PBS.

5. [LLM Training on HPC](05_llm_training.md) — Module 2/3: Building & Running
   - Setup for HuggingFace & NVIDIA.
   - Cache management (and why compute nodes without internet access need a pre-fetch step).
   - The LoRA fine-tuning capstone, submitted as a real Slurm batch job.

## Hands-on exercises (8 total, across 3 modules)

**Module 1 — Interacting** (`01_interacting/`)
- Pull, shell, exec, and run pre-built images (`python.sif`, `ubuntu.sif`, `ubuntu_22.04.sif`), including a bind-mount example with `data/test.txt`.

**Module 2 — Building** (`02_building/`)
- `01_hello.def` — your first container: the minimal shape of a definition file.
- `02_conda.def` — a Python/conda data-science environment, pulled pre-built from Docker Hub.
- `03_complex.def` — all five definition-file sections in one image (`%setup`, `%files`, `%environment`, `%post`, `%startscript`, plus `%help`/`%test`), including starting and stopping it as a background instance.
- `04_ml_gpu.def` — a GPU-ready PyTorch container.
- `05_llm.def` — a PyTorch + Transformers/PEFT/bitsandbytes container, used by the Module 3 capstone.

**Module 3 — Running on HPC** (`03_running_on_hpc/`)
- `job_cpu_matmul.slurm` — a plain CPU Slurm batch job (matrix-multiply benchmark), the fast, low-risk way to learn `sbatch`/`squeue` mechanics.
- `job_gpu_llm.slurm` (+ `prefetch_model.sh`) — the LLM fine-tuning capstone: a small LoRA fine-tune of `distilgpt2`, submitted with `--nv` on a GPU node. Since compute nodes have no internet access, the model must be pre-fetched from a login node first — see the comments in `prefetch_model.sh` and `job_gpu_llm.slurm`.

Two deck topics — sharing/distributing containers, and NVIDIA NGC containers — are covered as lecture/demo material without a dedicated exercise folder.

## Suggested 3-hour timeline

Two 90-minute sessions. Times are a guideline, not a contract — see "what's optional" below for what to trim if you're running behind.

**Session 1 — Foundations & Building**

| Time | Content | Type |
|---|---|---|
| 0:00–0:10 | Why Containers in HPC | Lecture |
| 0:10–0:30 | Container Fundamentals + checkpoint quiz | Lecture |
| 0:30–0:50 | Exercise: Interacting (pull/shell/exec/run) + checkpoint | Hands-on |
| 0:50–1:20 | Exercises: `01_hello.def`, `02_conda.def`, `03_complex.def` + Build Verification checkpoint | Hands-on |
| 1:20–1:30 | Sharing & Distributing Containers | Lecture/demo |

**Session 2 — HPC Integration & Capstone**

| Time | Content | Type |
|---|---|---|
| 0:00–0:20 | Running on HPC with Slurm + `job_cpu_matmul.slurm` + checkpoint | Hands-on |
| 0:20–0:35 | NVIDIA NGC Containers | Lecture/demo |
| 0:35–0:65 | Advanced Topics (GPU/MPI/I-O/GUI) + verify pre-built `ml_gpu.sif` with `--nv` + checkpoints | Hands-on/lecture |
| 0:65–0:85 | LLM Capstone: `prefetch_model.sh`, then submit `job_gpu_llm.slurm` early and keep teaching while it queues + checkpoint | Hands-on |
| 0:85–0:90 | Wrap-Up, final self-assessment, Q&A | Lecture |

**A practical note on GPU queue time:** the LoRA fine-tune itself only takes a few seconds once the job starts — the real variable is how long `job_gpu_llm.slurm` sits in the `dc-gpu` queue. Submit it at the *start* of that block, not after explaining it, so queue wait overlaps with instruction time instead of adding to it.

**A practical note on image size:** `04_ml_gpu.def` and `05_llm.def` pull multi-gigabyte base images from Docker Hub. Having every participant build these live risks both wall-clock time and Docker Hub rate limits. Pre-build `ml_gpu.sif` and `llm.sif` onto shared storage before the workshop and let participants run them directly; reserve the live `apptainer build --fakeroot` experience for the three cheap ones (`01_hello.def`, `02_conda.def`, `03_complex.def`).

### What's essential vs. optional

**Core (don't cut):** Why Containers + Fundamentals, the Interacting exercise, `01_hello.def`, `03_complex.def` (the highest-density teaching exercise — all five def-file sections in one artifact), the CPU Slurm job, and the final self-assessment/wrap-up.

**Important but trimmable:** `02_conda.def` (can become an instructor walkthrough instead of everyone building it live), NGC Containers (compress to a few slides if short on time), Sharing & Distributing (a couple of commands shown, not a full lab).

**Stretch / first to cut:** live-building `04_ml_gpu.def` and `05_llm.def` (pre-build these regardless — see above), the full GPU LLM capstone if the room is running late (fall back to an instructor demo with a pre-captured log), and the MPI/GUI portions of Advanced Topics, which are slide-only material with no dedicated exercise behind them.