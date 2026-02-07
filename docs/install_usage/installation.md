---
comments: true
hide:
#   - navigation
  - toc
---

由于模型较小，预先将中文版面分析模型（`layout_cdla.onnx`）打包进了 whl 包内，若仅做中文版面分析，可直接安装使用：

```bash
pip install rapid-layout onnxruntime
```
