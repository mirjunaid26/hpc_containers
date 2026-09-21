#!/usr/bin/env python3
"""
matmul_cpu.py — Workshop demo: CPU matrix multiplication with NumPy.

Purpose
-------
A short, self-contained CPU workload for demonstrating Slurm + Apptainer on a
CPU partition — no GPU, no external downloads, just NumPy doing real work.
Also useful for the "match --cpus-per-task to threads actually used" lesson:
this script prints how many threads NumPy sees, so participants can see the
effect of getting that Slurm setting wrong.

Expected invocation (see the matching sbatch script):
    apptainer exec exercises/conda_env.sif python matmul_cpu.py --size 4000
"""

import argparse
import os
import time

import numpy as np


def main():
    parser = argparse.ArgumentParser(description="CPU matrix multiplication demo")
    parser.add_argument("--size", type=int, default=4000, help="Matrix dimension N (N x N)")
    parser.add_argument("--repeats", type=int, default=3, help="Number of multiplications to time")
    args = parser.parse_args()

    print("=" * 50)
    print("CPU Matmul Demo")
    print("=" * 50)
    print(f"Matrix size:         {args.size} x {args.size}")
    print(f"Repeats:             {args.repeats}")
    print(f"OMP_NUM_THREADS:     {os.environ.get('OMP_NUM_THREADS', '(not set)')}")
    print(f"SLURM_CPUS_PER_TASK: {os.environ.get('SLURM_CPUS_PER_TASK', '(not set)')}")
    print(f"NumPy version:       {np.__version__}")

    rng = np.random.default_rng(42)
    a = rng.random((args.size, args.size), dtype=np.float64)
    b = rng.random((args.size, args.size), dtype=np.float64)

    flops_per_matmul = 2 * args.size ** 3  # multiply-add per output element

    print("\nRunning warm-up multiplication...")
    _ = a @ b

    times = []
    for i in range(args.repeats):
        start = time.perf_counter()
        c = a @ b
        elapsed = time.perf_counter() - start
        times.append(elapsed)
        gflops = flops_per_matmul / elapsed / 1e9
        print(f"  Run {i + 1}: {elapsed:.3f} s  ({gflops:.1f} GFLOP/s)")

    avg = sum(times) / len(times)
    print(f"\nAverage time: {avg:.3f} s over {args.repeats} runs")
    print(f"Result checksum (sanity check): {c.sum():.4f}")
    print("Done.")


if __name__ == "__main__":
    main()
