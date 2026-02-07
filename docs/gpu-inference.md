# GPU 推理

- 版面分析模型输入图像尺寸固定，可使用 `onnxruntime-gpu` 进行加速。
- `rapid_layout` 默认依赖 CPU 版 `onnxruntime`，使用 GPU 推理需手动安装 `onnxruntime-gpu`。
- 详细使用与评测可参见 [AI Studio](https://aistudio.baidu.com/projectdetail/8094594)。

## 安装

```bash
pip install rapid_layout
pip uninstall onnxruntime

# 请确保 onnxruntime-gpu 与当前 GPU/CUDA 版本对应
# 参见 https://onnxruntime.ai/docs/execution-providers/CUDA-ExecutionProvider.html#requirements
pip install onnxruntime-gpu
```

## 使用

```python
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
