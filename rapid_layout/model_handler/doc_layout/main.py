# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from ..base import BaseModelHandler
from .post_process import DocLayoutPostProcess
from .pre_process import DocLayoutPreProcess


class DocLayoutModelHandler(BaseModelHandler):
    def __init__(self, labels, conf_thres, iou_thres):
        self.img_size = (1024, 1024)
        self.doclayout_preprocess = DocLayoutPreProcess(img_size=self.img_size)
        self.doclayout_postprocess = DocLayoutPostProcess(labels, conf_thres, iou_thres)

    def preprocess(self, image):
        return self.doclayout_preprocess(image)

    def postprocess(self, preds, ori_img_shape, img_shape):
        return self.doclayout_postprocess(preds, ori_img_shape, img_shape)

    @property
    def input_shape(self):
        return self.img_size
