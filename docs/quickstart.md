# 快速开始

## 安装

```bash
pip install rapid-layout onnxruntime
```

## 第一个示例

```python
from rapid_layout import EngineType, ModelType, RapidLayout, RapidLayoutInput

cfg = RapidLayoutInput()
layout_engine = RapidLayout(cfg=cfg)

img_path = "https://raw.githubusercontent.com/RapidAI/RapidLayout/718b60e927ab893c2fad67c98f753b2105a6f421/tests/test_files/layout.jpg"
results = layout_engine(img_path)
print(results)

results.vis("layout_res.png")
```

更多用法见 [使用方式](usage.md)，支持的模型见 [支持的模型](models.md)。
