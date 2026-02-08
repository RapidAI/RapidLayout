---
comments: true
hide:
#   - navigation
  - toc
---

## Python 脚本运行

**默认用法**（默认模型 `pp_layout_cdla` + `onnxruntime` 引擎）：

```python
from rapid_layout import RapidLayout

layout_engine = RapidLayout()
img_path = "https://raw.githubusercontent.com/RapidAI/RapidLayout/718b60e927ab893c2fad67c98f753b2105a6f421/tests/test_files/layout.jpg"
results = layout_engine(img_path)
print(results)
results.vis("layout_res.png")
```

**指定模型与引擎**（关键字参数）：

```python
from rapid_layout import EngineType, ModelType, RapidLayout

layout_engine = RapidLayout(
    model_type=ModelType.PP_LAYOUT_CDLA,
    engine_type=EngineType.ONNXRUNTIME,
    conf_thresh=0.5,
    iou_thresh=0.5,
)
results = layout_engine(img_path)
print(results)
results.vis("layout_res.png")
```

**使用配置对象**（与上方等价）：

```python
from rapid_layout import EngineType, ModelType, RapidLayout, RapidLayoutInput

cfg = RapidLayoutInput(
    model_type=ModelType.PP_LAYOUT_CDLA,
    engine_type=EngineType.ONNXRUNTIME,
    conf_thresh=0.5,
    iou_thresh=0.5,
)
layout_engine = RapidLayout(cfg=cfg)
results = layout_engine(img_path)
print(results)
results.vis("layout_res.png")
```

## 终端运行

```bash
rapid_layout test_images/layout.png
rapid_layout test_images/layout.png -m pp_layout_cdla --conf_thresh 0.5 --iou_thresh 0.5
```

## 构造函数参数（RapidLayout / RapidLayoutInput）

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `model_type` | ModelType / str | `pp_layout_cdla` | 模型类型 |
| `model_dir_or_path` | str / Path / None | None | 模型路径，不传则按 model_type 解析 |
| `engine_type` | EngineType / str | `onnxruntime` | 推理引擎：`onnxruntime`、`openvino` |
| `engine_cfg` | dict | `{}` | 引擎额外配置 |
| `conf_thresh` | float | 0.5 | 框置信度阈值 [0, 1] |
| `iou_thresh` | float | 0.5 | IoU 阈值 [0, 1] |

## 可视化结果

<div align="center">
    <img src="https://github.com/RapidAI/RapidLayout/releases/download/v0.0.0/layout_vis.jpg" width="80%">
</div>
