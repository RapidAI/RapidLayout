# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from rapid_layout import RapidLayout
from rapid_layout.utils.typings import EngineType, ModelType, RapidLayoutInput

input_args = RapidLayoutInput(
    engine_type=EngineType.ONNXRUNTIME, model_type=ModelType.DOCLAYOUT_DOCSTRUCTBENCH
)
layout_engine = RapidLayout(cfg=input_args)

img_path = "https://raw.githubusercontent.com/opendatalab/DocLayout-YOLO/refs/heads/main/assets/example/financial.jpg"
results = layout_engine(img_path)
results.vis("layout_res.png")
