# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from ..base import BaseModelHandler
from .post_process import YOLOv8PostProcess
from .pre_process import YOLOv8PreProcess


class YOLOv8ModelHandler(BaseModelHandler):
    def __init__(self, labels, conf_thres, iou_thres):
        self.img_size = (640, 640)
        self.yolov8_preprocess = YOLOv8PreProcess(img_size=self.img_size)
        self.yolov8_postprocess = YOLOv8PostProcess(labels, conf_thres, iou_thres)

    def preprocess(self, image):
        return self.yolov8_preprocess(image)

    def postprocess(self, model_output):
        return self.yolov8_postprocess(model_output)

    @property
    def input_shape(self):
        return self.img_size
