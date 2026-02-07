---
comments: true
title: 快速开始
hide:
  - navigation
  - toc
---

## 安装

```bash
pip install rapid-layout onnxruntime
```

## 运行

=== "Python脚本运行"

    ```python linenums="1"
    from rapid_layout import EngineType, ModelType, RapidLayout, RapidLayoutInput

    cfg = RapidLayoutInput()
    layout_engine = RapidLayout(cfg=cfg)

    img_path = "https://raw.githubusercontent.com/RapidAI/RapidLayout/718b60e927ab893c2fad67c98f753b2105a6f421/tests/test_files/layout.jpg"
    results = layout_engine(img_path)
    print(results)

    results.vis("layout_res.png")
    ```

=== "终端运行"

    ```bash linenums="1"
    rapid_layout test_images/layout.png
    ```

## 可视化结果

<div align="center">
    <img src="https://github.com/RapidAI/RapidLayout/releases/download/v0.0.0/layout_vis.jpg" width="60%">
</div>
