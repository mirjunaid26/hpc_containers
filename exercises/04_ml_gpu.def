Bootstrap: docker
From: pytorch/pytorch:2.4.0-cuda12.4-cudnn9-runtime

%post
    pip install scikit-learn matplotlib

%environment
    export CUDA_VISIBLE_DEVICES=0,1

%runscript
    exec python "$@"

%test
    python -c "import torch; print('Torch version:', torch.__version__)"