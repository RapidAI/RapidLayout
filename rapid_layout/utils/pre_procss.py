# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path
from typing import Union

import cv2
import numpy as np

InputType = Union[str, np.ndarray, bytes, Path]


def transform(data, ops=None):
    """transform"""
    if ops is None:
        ops = []

    for op in ops:
        data = op(data)
        if data is None:
            return None
    return data


def create_operators(op_param_dict):
    ops = []
    for op_name, param in op_param_dict.items():
        if param is None:
            param = {}
        op = eval(op_name)(**param)
        ops.append(op)
    return ops


class Resize:
    def __init__(self, size=(640, 640)):
        self.size = size

    def resize_image(self, img):
        resize_h, resize_w = self.size
        ori_h, ori_w = img.shape[:2]  # (h, w, c)
        ratio_h = float(resize_h) / ori_h
        ratio_w = float(resize_w) / ori_w
        img = cv2.resize(img, (int(resize_w), int(resize_h)))
        return img, [ratio_h, ratio_w]

    def __call__(self, data):
        img = data["image"]
        if "polys" in data:
            text_polys = data["polys"]

        img_resize, [ratio_h, ratio_w] = self.resize_image(img)
        if "polys" in data:
            new_boxes = []
            for box in text_polys:
                new_box = []
                for cord in box:
                    new_box.append([cord[0] * ratio_w, cord[1] * ratio_h])
                new_boxes.append(new_box)
            data["polys"] = np.array(new_boxes, dtype=np.float32)
        data["image"] = img_resize
        return data


class NormalizeImage:
    def __init__(self, scale=None, mean=None, std=None, order="chw"):
        if isinstance(scale, str):
            scale = eval(scale)

        self.scale = np.float32(scale if scale is not None else 1.0 / 255.0)
        mean = mean if mean is not None else [0.485, 0.456, 0.406]
        std = std if std is not None else [0.229, 0.224, 0.225]

        shape = (3, 1, 1) if order == "chw" else (1, 1, 3)
        self.mean = np.array(mean).reshape(shape).astype("float32")
        self.std = np.array(std).reshape(shape).astype("float32")

    def __call__(self, data):
        img = np.array(data["image"])
        assert isinstance(img, np.ndarray), "invalid input 'img' in NormalizeImage"
        data["image"] = (img.astype("float32") * self.scale - self.mean) / self.std
        return data


class ToCHWImage:
    def __init__(self, **kwargs):
        pass

    def __call__(self, data):
        img = np.array(data["image"])
        data["image"] = img.transpose((2, 0, 1))
        return data


class KeepKeys:
    def __init__(self, keep_keys):
        self.keep_keys = keep_keys

    def __call__(self, data):
        data_list = []
        for key in self.keep_keys:
            data_list.append(data[key])
        return data_list
