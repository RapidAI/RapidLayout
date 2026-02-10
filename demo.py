# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from rapid_layout import EngineType, ModelType, RapidLayout

layout_engine = RapidLayout(
    engine_type=EngineType.ONNXRUNTIME,
    model_type=ModelType.PP_DOC_LAYOUTV2,
)

img_url = "https://www.modelscope.cn/models/RapidAI/RapidLayout/resolve/master/resources/test_files/pp_doc_layoutv2_layout.jpg"
results = layout_engine(img_url)
print(results)

results.vis("layout_res.png")
