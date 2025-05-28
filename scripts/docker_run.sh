docker run --rm --gpus all --name 9g7b --privileged=true -w /app/algorithm \
    -v .:/app/algorithm/ \
    9g7b:v1 bash scripts/run.sh

# docker commit 9g7b 9g7b:v2