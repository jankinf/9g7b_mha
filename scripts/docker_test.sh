docker run --gpus all --name 9g7b --privileged=true -w /app/algorithm \
    -v .:/app/algorithm/ \
    -it 9g7b:v1 bash

# docker ps -a
# docker rm 9g7b