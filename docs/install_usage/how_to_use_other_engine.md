---
comments: true
hide:
#   - navigation
  - toc
---

## 引言

因为版面分析模型输入图像尺寸固定，故可使用`onnxruntime-gpu`来提速。因为`rapid_layout`库默认依赖是CPU版`onnxruntime`，如果想要使用GPU推理，需要手动安装`onnxruntime-gpu`。详细使用和评测可参见[AI Studio](https://aistudio.baidu.com/projectdetail/8094594)

## 使用GPU

```bash
pip install rapid_layout

# 请确保 onnxruntime-gpu 与当前 GPU/CUDA 版本对应
# 参见 https://onnxruntime.ai/docs/execution-providers/CUDA-ExecutionProvider.html#requirements
pip install onnxruntime-gpu
```

## 使用

```python linenums="1"
from rapid_layout import EngineType, ModelType, RapidLayout, RapidLayoutInput

cfg = RapidLayoutInput(
    model_type=ModelType.PP_LAYOUT_CDLA,
    engine_type=EngineType.ONNXRUNTIME,
    engine_cfg={"use_cuda": True, "cuda_ep_cfg.gpu_id": 1},
)
layout_engine = RapidLayout(cfg=cfg)

img_path = "https://raw.githubusercontent.com/RapidAI/RapidLayout/718b60e927ab893c2fad67c98f753b2105a6f421/tests/test_files/layout.jpg"
results = layout_engine(img_path)
print(results)

results.vis("layout_res.png")
```

## 使用NPU

详细配置参数参见：[engine_cfg.yaml](https://github.com/RapidAI/RapidLayout/blob/a7ab63ff291bd72e1a98ac2bb11860575514f432/rapid_layout/configs/engine_cfg.yaml)

```python linenums="1"
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
