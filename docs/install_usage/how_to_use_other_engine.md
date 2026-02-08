---
comments: true
hide:
#   - navigation
  - toc
---

## 引言

版面分析支持多种推理引擎与设备：

- **ONNX Runtime**：默认引擎，支持 CPU / CUDA / DirectML / CANN，需按需安装对应包。
- **OpenVINO**：可选，`pip install openvino` 后通过 `engine_type=EngineType.OPENVINO` 使用。

默认依赖为 CPU 版 `onnxruntime`；使用 GPU 推理需手动安装 `onnxruntime-gpu`。详细使用和评测可参见 [AI Studio](https://aistudio.baidu.com/projectdetail/8094594)。

## 使用 ONNX Runtime + GPU (CUDA)

```bash
pip install rapid_layout
# 请确保 onnxruntime-gpu 与当前 GPU/CUDA 版本对应
# 参见 https://onnxruntime.ai/docs/execution-providers/CUDA-ExecutionProvider.html#requirements
pip install onnxruntime-gpu
```

```python linenums="1"
from rapid_layout import EngineType, ModelType, RapidLayout, RapidLayoutInput

cfg = RapidLayoutInput(
    model_type=ModelType.PP_LAYOUT_CDLA,
    engine_type=EngineType.ONNXRUNTIME,
    engine_cfg={"use_cuda": True, "cuda_ep_cfg": {"device_id": 0}},
)
layout_engine = RapidLayout(cfg=cfg)

img_path = "https://raw.githubusercontent.com/RapidAI/RapidLayout/718b60e927ab893c2fad67c98f753b2105a6f421/tests/test_files/layout.jpg"
results = layout_engine(img_path)
print(results)
results.vis("layout_res.png")
```

多卡时可通过 `cuda_ep_cfg.device_id` 指定卡号（与 [engine_cfg.yaml](https://github.com/RapidAI/RapidLayout/blob/main/rapid_layout/configs/engine_cfg.yaml) 中 `cuda_ep_cfg.device_id` 一致）。

## 使用 OpenVINO

```bash
pip install rapid-layout onnxruntime openvino
```

```python linenums="1"
from rapid_layout import EngineType, ModelType, RapidLayout

layout_engine = RapidLayout(
    model_type=ModelType.PP_LAYOUT_CDLA,
    engine_type=EngineType.OPENVINO,
)
img_path = "https://raw.githubusercontent.com/RapidAI/RapidLayout/718b60e927ab893c2fad67c98f753b2105a6f421/tests/test_files/layout.jpg"
results = layout_engine(img_path)
print(results)
results.vis("layout_res.png")
```

OpenVINO 设备与线程等配置见 [engine_cfg.yaml](https://github.com/RapidAI/RapidLayout/blob/main/rapid_layout/configs/engine_cfg.yaml) 中 `openvino` 段。

## 使用 NPU (CANN)

详细配置参数参见：[engine_cfg.yaml](https://github.com/RapidAI/RapidLayout/blob/main/rapid_layout/configs/engine_cfg.yaml)

```python linenums="1"
from rapid_layout import EngineType, ModelType, RapidLayout, RapidLayoutInput

cfg = RapidLayoutInput(
    model_type=ModelType.PP_LAYOUT_CDLA,
    engine_type=EngineType.ONNXRUNTIME,
    engine_cfg={"use_cann": True, "cann_ep_cfg": {"device_id": 0}},
)
layout_engine = RapidLayout(cfg=cfg)

img_path = "https://raw.githubusercontent.com/RapidAI/RapidLayout/718b60e927ab893c2fad67c98f753b2105a6f421/tests/test_files/layout.jpg"
results = layout_engine(img_path)
print(results)
results.vis("layout_res.png")
```
