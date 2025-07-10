# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import numpy as np

from ..inference_engine.base import InferSession
from ..utils.typings import RapidLayoutOutput
from .doc_layout import DocLayoutModelHandler
from .pp import PPModelHandler
from .yolov8 import YOLOv8ModelHandler


class ModelHandler:
    def __init__(self, labels, conf_thres, iou_thres, session: InferSession):
        self.model_processors = {
            "pp": PPModelHandler(labels, conf_thres, iou_thres),
            "yolov8": YOLOv8ModelHandler(labels, conf_thres, iou_thres),
            "doclayout": DocLayoutModelHandler(labels, conf_thres, iou_thres),
        }
        self.session = session

    def __call__(self, img: np.ndarray) -> RapidLayoutOutput:
        return self.model_processors(img)
