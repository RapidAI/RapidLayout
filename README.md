<div align="center">
  <h1><b>📖 Rapid Layout</b></h1>
  <div>&nbsp;</div>
  <b><font size="4"><i>文档版面分析 - 定位标题、段落、表格与图片等版面元素</i></font></b>
  <div>&nbsp;</div>

<a href="https://huggingface.co/spaces/RapidAI/RapidLayoutv1" target="_blank"><img src="https://img.shields.io/badge/%F0%9F%A4%97-Hugging Face Demo-blue"></a>
<a href=""><img src="https://img.shields.io/badge/Python->=3.6-aff.svg"></a>
<a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
<a href="https://pypi.org/project/rapid-layout/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapid-layout"></a>
<a href="https://pepy.tech/project/rapid-layout"><img src="https://static.pepy.tech/personalized-badge/rapid-layout?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
<a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

</div>

### 📝 简介

Rapid Layout 汇集全网开源的版面分析能力，对文档类图像（论文截图、研报等）进行分析，定位其中的**类别与位置**，如标题、段落、表格、图片等版面元素。

**支持场景概览：** 支持表格、中文、英文、论文、研报及通用版面等多种类型，内置 PP 系列、YOLOv8 系列以及推荐的 DocLayout-YOLO 等模型。不同场景版面差异较大，暂无单一模型覆盖所有场景；若业务效果不佳，建议自建训练集微调。完整模型列表与下载见[文档站](https://rapidai.github.io/RapidLayout/)。

如果您觉得本仓库对您有帮助，欢迎给个 ⭐ 支持一下。

### 🎥 效果展示

<div align="center">
    <img src="https://github.com/RapidAI/RapidLayout/releases/download/v0.0.0/layout_vis.jpg" width="40%">
</div>

### 🛠️ 安装

```bash
pip install rapid-layout onnxruntime
```

### 📋 使用

```python
from rapid_layout import RapidLayout, RapidLayoutInput

cfg = RapidLayoutInput()
layout_engine = RapidLayout(cfg=cfg)

img_path = "https://raw.githubusercontent.com/RapidAI/RapidLayout/718b60e927ab893c2fad67c98f753b2105a6f421/tests/test_files/layout.jpg"
results = layout_engine(img_path)
print(results)

results.vis("layout_res.png")
```

终端运行：`rapid_layout test_images/layout.png`

### 📚 文档

完整文档（安装、使用方式、模型列表、GPU/NPU 配置、参考项目等）请移步：[**Rapid Layout 文档**](https://rapidai.github.io/RapidLayout/)

### 🙏 致谢

- [DocLayout-YOLO](https://github.com/opendatalab/DocLayout-YOLO)
- [PaddleOCR 版面分析](https://github.com/PaddlePaddle/PaddleOCR/blob/133d67f27dc8a241d6b2e30a9f047a0fb75bebbe/ppstructure/layout/README_ch.md)
- [360LayoutAnalysis](https://github.com/360AILAB-NLP/360LayoutAnalysis)
- [ONNX-YOLOv8-Object-Detection](https://github.com/ibaiGorordo/ONNX-YOLOv8-Object-Detection)
- [ChineseDocumentPDF](https://github.com/SWHL/ChineseDocumentPDF)

### 🤝 贡献指南

欢迎通过 Issue 反馈问题与建议，或通过 Pull Request 参与代码与文档贡献。完整流程请参阅：[贡献指南](https://rapidai.github.io/RapidLayout/contributing/)。

### 🎖 贡献者

<p align="left">
  <a href="https://github.com/RapidAI/RapidLayout/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=RapidAI/RapidLayout&max=400&columns=10" width="60%"/>
  </a>
</p>

### 📜 引用

若该项目对您的研究有帮助，可考虑引用：

```bibtex
@misc{RapidLayout,
    title={{Rapid Layout}: Document Layout Analysis},
    author={RapidAI Team},
    howpublished = {\url{https://github.com/RapidAI/RapidLayout}},
    year={2024}
}
```

### ⭐️ Star history

[![Stargazers over time](https://starchart.cc/RapidAI/RapidLayout.svg?variant=adaptive)](https://starchart.cc/RapidAI/RapidLayout)

### ⚖️ 开源许可证

本项目采用 [Apache 2.0 license](LICENSE) 开源许可证。
