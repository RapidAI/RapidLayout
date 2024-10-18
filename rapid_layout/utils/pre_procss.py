# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path
from typing import Optional, Tuple, Union

import cv2
import numpy as np

InputType = Union[str, np.ndarray, bytes, Path]


class PPPreProcess:

    def __init__(self, img_size: Tuple[int, int]):
        self.size = img_size
        self.mean = np.array([0.485, 0.456, 0.406])
        self.std = np.array([0.229, 0.224, 0.225])
        self.scale = 1 / 255.0

    def __call__(self, img: Optional[np.ndarray] = None) -> np.ndarray:
        if img is None:
            raise ValueError("img is None.")

        img = self.resize(img)
        img = self.normalize(img)
        img = self.permute(img)
        img = np.expand_dims(img, axis=0)
        return img.astype(np.float32)

    def resize(self, img: np.ndarray) -> np.ndarray:
        resize_h, resize_w = self.size
        img = cv2.resize(img, (int(resize_w), int(resize_h)))
        return img

    def normalize(self, img: np.ndarray) -> np.ndarray:
        return (img.astype("float32") * self.scale - self.mean) / self.std

    def permute(self, img: np.ndarray) -> np.ndarray:
        return img.transpose((2, 0, 1))


class YOLOv8PreProcess:

    def __init__(self, img_size: Tuple[int, int]):
        self.img_size = img_size

    def __call__(self, image: np.ndarray) -> np.ndarray:
        input_img = cv2.resize(image, self.img_size)
        input_img = input_img / 255.0
        input_img = input_img.transpose(2, 0, 1)
        input_tensor = input_img[np.newaxis, :, :, :].astype(np.float32)
        return input_tensor


class DocLayoutPreProcess:

    def __init__(self, img_size: Tuple[int, int]):
        self.img_size = img_size

    def __call__(self, image: np.ndarray) -> np.ndarray:
        input_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        input_img = cv2.resize(image, self.img_size)
        input_img = input_img / 255.0
        input_img = input_img.transpose(2, 0, 1)
        input_tensor = input_img[np.newaxis, :, :, :].astype(np.float32)
        return input_tensor
