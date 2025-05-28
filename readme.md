# build your image
```shell
# build image
bash scripts/docker_build.sh

# save image
docker save -o 9g7b_img.tar 9g7b:v1

# download model: https://www.osredm.com/jiuyuan/CPM-9G-8B/tree/FM_9G/quick_start_4_7_70/inference_7b.md
wget https://thunlp-model.oss-cn-wulanchabu.aliyuncs.com/9G7B_MHA.tar
tar -xvf 9G7B_MHA.tar
rm 9G7B_MHA.tar

# pack up model, image, config and code
tar cvf 9g7b.tar \
    --exclude "9g7b/.git/*" \
    9g7b/
```

# load image and run
```shell
# load image
docker load -i 9g7b_img.tar

# run
bash scripts/docker_run.sh
```
