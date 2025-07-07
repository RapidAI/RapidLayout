# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path
from typing import Tuple, Union

import cv2
import numpy as np

InputType = Union[str, np.ndarray, bytes, Path]


class YOLOv8PreProcess:
    def __init__(self, img_size: Tuple[int, int]):
        self.img_size = img_size

    def __call__(self, image: np.ndarray) -> np.ndarray:
        input_img = cv2.resize(image, self.img_size)
        input_img = input_img / 255.0
        input_img = input_img.transpose(2, 0, 1)
        input_tensor = input_img[np.newaxis, :, :, :].astype(np.float32)
        return input_tensor
