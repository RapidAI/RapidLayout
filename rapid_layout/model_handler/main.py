# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from typing import Any

import numpy as np
from omegaconf import DictConfig

from ..inference_engine.base import InferSession
from ..utils.typings import RapidLayoutOutput
from .doc_layout import DocLayoutModelHandler
from .pp import PPModelHandler
from .yolov8 import YOLOv8ModelHandler


class ModelHandler:
    def __init__(self, cfg: DictConfig, session: InferSession):
        self.model_processors = self._init_handler(cfg, session)

    def _init_handler(self, cfg: DictConfig, session: InferSession) -> Any:
        model_type = cfg.model_type.value
        if model_type.startswith("pp"):
            return PPModelHandler(
                session.characters, cfg.conf_thresh, cfg.iou_thresh, session
            )

        if model_type.startswith("yolov8"):
            return YOLOv8ModelHandler(
                session.characters, cfg.conf_thresh, cfg.iou_thresh, session
            )

        if model_type.startswith("doclayout"):
            return DocLayoutModelHandler(
                session.characters, cfg.conf_thresh, cfg.iou_thresh, session
            )

        raise ValueError(f"{model_type.value} is not supported!")

    def __call__(self, img: np.ndarray) -> RapidLayoutOutput:
        return self.model_processors(img)
