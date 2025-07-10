# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Union


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
    boxes: Optional[List[List[float]]] = None
    class_names: Optional[List[str]] = None
    scores: Optional[List[float]] = None
    elapse: Optional[float] = None
