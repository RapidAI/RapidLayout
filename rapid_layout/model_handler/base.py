# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from abc import ABC, abstractmethod


class BaseModelHandler(ABC):
    @abstractmethod
    def preprocess(self, image):
        """图像预处理抽象方法"""

    @abstractmethod
    def postprocess(self, model_output):
        """模型输出后处理抽象方法"""

    @property
    @abstractmethod
    def input_shape(self):
        """模型输入尺寸属性"""
