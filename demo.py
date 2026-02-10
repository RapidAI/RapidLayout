# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from rapid_layout import EngineType, ModelType, RapidLayout

layout_engine = RapidLayout(
    engine_type=EngineType.ONNXRUNTIME,
    model_type=ModelType.PP_DOC_LAYOUTV2,
)

img_path = "tests/test_files/pp_doc_layoutv2_layout.jpg"
results = layout_engine(img_path)
print(results)

results.vis("layout_res.png")
