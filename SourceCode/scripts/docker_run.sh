docker run --rm --gpus all --name 9g7b --privileged=true -w /app/algorithm \
    -v .:/app/algorithm/ \
    9g7b:v1 bash scripts/run.sh