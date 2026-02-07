# NPU 使用

详细配置参数参见：[engine_cfg.yaml](https://github.com/RapidAI/RapidLayout/blob/a7ab63ff291bd72e1a98ac2bb11860575514f432/rapid_layout/configs/engine_cfg.yaml)

```python
from rapid_layout import EngineType, ModelType, RapidLayout, RapidLayoutInput

cfg = RapidLayoutInput(
    model_type=ModelType.PP_LAYOUT_CDLA,
    engine_type=EngineType.ONNXRUNTIME,
    engine_cfg={"use_cann": True, "cann_ep_cfg.gpu_id": 0},
)
layout_engine = RapidLayout(cfg=cfg)

img_path = "https://raw.githubusercontent.com/RapidAI/RapidLayout/718b60e927ab893c2fad67c98f753b2105a6f421/tests/test_files/layout.jpg"
results = layout_engine(img_path)
print(results)

results.vis("layout_res.png")
```
