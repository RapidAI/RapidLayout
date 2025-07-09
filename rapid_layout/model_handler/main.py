# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from .doc_layout import DocLayoutModelHandler
from .pp import PPModelHandler
from .yolov8 import YOLOv8ModelHandler


class ModelHandler:
    def __init__(self, labels, conf_thres, iou_thres):
        self.model_processors = {
            "pp": PPModelHandler(labels, conf_thres, iou_thres),
            "yolov8": YOLOv8ModelHandler(labels, conf_thres, iou_thres),
            "doclayout": DocLayoutModelHandler(labels, conf_thres, iou_thres),
        }

    def __call__(self, model_name, image, model_output):
        processor = self.model_processors.get(model_name)
        if not processor:
            raise ValueError(f"不支持的模型: {model_name}")

        preprocessed_img = processor.preprocess(image)
        postprocessed_result = processor.postprocess(model_output)

        return {
            "input_shape": processor.input_shape,
            "preprocessed_image": preprocessed_img,
            "postprocessed_result": postprocessed_result,
        }
