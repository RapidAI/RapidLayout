# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from ..base import BaseModelHandler
from .post_process import PPPostProcess
from .pre_process import PPPreProcess


class PPModelHandler(BaseModelHandler):
    def __init__(self, labels, conf_thres, iou_thres):
        self.img_size = (800, 608)
        self.pp_preprocess = PPPreProcess(img_size=self.img_size)
        self.pp_postprocess = PPPostProcess(labels, conf_thres, iou_thres)

    def preprocess(self, image):
        return self.pp_preprocess(image)

    def postprocess(self, model_output):
        return self.pp_postprocess(model_output)

    @property
    def input_shape(self):
        return self.img_size
