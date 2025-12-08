# Module 4: HPC Integration (GPU & MPI)

This module encapsulates the primary use cases for Apptainer in High Performance Computing.

## GPU Support

Apptainer makes it trivial to use GPUs. You do NOT need to install the NVIDIA driver inside the container. You only need the CUDA toolkit (and cuDNN) inside. The host driver is mounted at runtime.

### The `--nv` flag

To enable GPU support, simply add --nv:

```bash
apptainer exec --nv pytorch.sif python train.py
```

## MPI Support

Apptainer supports the "Hybrid MPI" model. You have an MPI installed on the host (e.g., OpenMPI) and a compatible MPI installed inside the container.

### Execution

You call `mpirun` from the **host**, which then launches apptainer containers.

```bash
mpirun -n 4 apptainer exec my_mpi_app.sif /app/mpi_binary
```

## Bind Paths

By default, Apptainer binds `$HOME`, `/tmp`, and `$PWD`. On HPC, you often need access to scratch storage or shared datasets.

```bash
apptainer exec --bind /scratch/user:/data my_container.sif python script.py
```

This maps `/scratch/user` on the host to `/data` inside the container.

## Exercise: GPU Machine Learning

See `exercises/04_ml_gpu.def` for a PyTorch setup.

To test it (if you have a GPU):
```bash
apptainer exec --nv ml_gpu.sif python -c "import torch; print(torch.cuda.is_available())"
```
