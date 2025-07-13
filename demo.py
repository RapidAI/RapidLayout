# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from rapid_layout import EngineType, ModelType, RapidLayout, RapidLayoutInput

layout_engine = RapidLayout()

img_path = "https://raw.githubusercontent.com/RapidAI/RapidLayout/refs/heads/develop/tests/test_files/layout.jpg"
results = layout_engine(img_path)
print(results)

results.vis("layout_res.png")
