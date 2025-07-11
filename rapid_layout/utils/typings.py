# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Union

import numpy as np

from .logger import Logger
from .utils import save_img

logger = Logger(logger_name=__name__).get_log()


class ModelType(Enum):
    PP_LAYOUT_CDLA = "pp_layout_cdla"
    PP_LAYOUT_PUBLAYNET = "pp_layout_publaynet"
    PP_LAYOUT_TABLE = "pp_layout_table"
    YOLOV8N_LAYOUT_PAPER = "yolov8n_layout_paper"
    YOLOV8N_LAYOUT_REPORT = "yolov8n_layout_report"
    YOLOV8N_LAYOUT_PUBLAYNET = "yolov8n_layout_publaynet"
    YOLOV8N_LAYOUT_GENERAL6 = "yolov8n_layout_general6"
    DOCLAYOUT_DOCSTRUCTBENCH = "doclayout_docstructbench"
    DOCLAYOUT_D4LA = "doclayout_d4la"
    DOCLAYOUT_DOCSYNTH = "doclayout_docsynth"


class EngineType(Enum):
    ONNXRUNTIME = "onnxruntime"


@dataclass
class RapidLayoutInput:
    model_type: ModelType = ModelType.PP_LAYOUT_CDLA
    model_dir_or_path: Union[str, Path, None, Dict[str, str]] = None

    engine_type: EngineType = EngineType.ONNXRUNTIME
    engine_cfg: dict = field(default_factory=dict)

    conf_thresh: float = 0.5
    iou_thresh: float = 0.5


@dataclass
class RapidLayoutOutput:
    img: Optional[np.ndarray] = None
    boxes: Optional[List[List[float]]] = None
    class_names: Optional[List[str]] = None
    scores: Optional[List[float]] = None
    elapse: Optional[float] = None

    def vis(self, save_path: Union[str, Path, None] = None) -> Optional[np.ndarray]:
        if self.img is None or self.boxes is None:
            logger.warning("No image or boxes to visualize.")
            return None

        from .vis_res import VisLayout

        vis_img = VisLayout.draw_detections(
            self.img,
            np.array(self.boxes),
            np.array(self.scores),
            np.array(self.class_names),
        )
        if save_path is not None and vis_img is not None:
            save_img(save_path, vis_img)
            logger.info(f"Visualization saved as {save_path}")

        return vis_img
