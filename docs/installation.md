# 安装

由于模型较小，预先将中文版面分析模型（`layout_cdla.onnx`）打包进了 whl 包内，若仅做中文版面分析，可直接安装使用：

```bash
pip install rapid-layout onnxruntime
```

若需使用 GPU 推理，请参见 [GPU 推理](gpu-inference.md) 进行 `onnxruntime-gpu` 的安装与配置。
