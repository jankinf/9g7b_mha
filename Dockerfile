FROM pytorch/pytorch:2.3.0-cuda12.1-cudnn8-devel

WORKDIR /app/algorithm

COPY ./requirements.txt /app/algorithm

ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3-pip \
    python3-dev \
    build-essential \
    git \
    gcc \
    g++ \
    wget \
    make \
    pipx \
    && rm -rf /var/lib/apt/lists/* \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && python3 -m pip install --no-cache-dir -r requirements.txt \
    && python3 -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"