#!/usr/bin/env bash
mkdir -p models
# All real-time models
# https://github.com/facebookresearch/Detic/blob/main/docs/MODEL_ZOO.md#real-time-models

# Swin Transformer model
wget https://dl.fbaipublicfiles.com/detic/Detic_LCOCOI21k_CLIP_SwinB_896b32_4x_ft4x_max-size.pth -O models/Detic_LCOCOI21k_CLIP_SwinB_896b32_4x_ft4x_max-size.pth
# ConvNet model
wget https://dl.fbaipublicfiles.com/detic/Detic_LCOCOI21k_CLIP_CXT21k_640b32_4x_ft4x_max-size.pth -O models/Detic_LCOCOI21k_CLIP_CXT21k_640b32_4x_ft4x_max-size.pth
# Res50 model
wget https://dl.fbaipublicfiles.com/detic/Detic_LCOCOI21k_CLIP_R5021k_640b32_4x_ft4x_max-size.pth -O models/Detic_LCOCOI21k_CLIP_R5021k_640b32_4x_ft4x_max-size.pth
# Res18 model
wget https://dl.fbaipublicfiles.com/detic/Detic_LCOCOI21k_CLIP_R18_640b32_4x_ft4x_max-size.pth -O models/Detic_LCOCOI21k_CLIP_R18_640b32_4x_ft4x_max-size.pth
