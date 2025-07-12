# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from rapid_layout import EngineType, ModelType, RapidLayout, RapidLayoutInput

cfg = RapidLayoutInput()
layout_engine = RapidLayout(cfg=cfg)

img_path = "https://raw.githubusercontent.com/opendatalab/DocLayout-YOLO/refs/heads/main/assets/example/financial.jpg"
results = layout_engine(img_path)
print(results)

results.vis("layout_res.png")
