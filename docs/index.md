---
comments: true
hide:
  - navigation
  - toc
---

<div align="center">
  <div align="center">
    <h1><b>Rapid Layout</b></h1>
  </div>

<a href="https://huggingface.co/spaces/RapidAI/RapidLayoutv1" target="_blank"><img src="https://img.shields.io/badge/%F0%9F%A4%97-Hugging Face Demo-blue"></a>
<a href=""><img src="https://img.shields.io/badge/Python->=3.6-aff.svg"></a>
<a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
<a href="https://pypi.org/project/rapid-layout/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapid-layout"></a>
<a href="https://pepy.tech/project/rapid-layout"><img src="https://static.pepy.tech/personalized-badge/rapid-layout?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
<a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

</div>

### 简介

该项目主要是汇集全网开源的版面分析的项目，具体来说，就是分析给定的文档类别图像（论文截图、研报等），定位其中类别和位置，如标题、段落、表格和图片等各个部分。

!!! warning "注意"
    由于不同场景下的版面差异较大，现阶段不存在一个模型可以搞定所有场景。如果实际业务需要，以下模型效果不好的话，建议构建自己的训练集微调。

目前支持的版面分析模型概览见 [支持的模型](models.md)，安装与使用见 [安装](installation.md)、[使用方式](usage.md)。

### TODO

- [ ] [PP-DocLayout](https://github.com/PaddlePaddle/PaddleX/blob/release/3.0-rc/docs/module_usage/tutorials/ocr_modules/layout_detection.md)整理

### 快速链接

- [快速开始](quickstart.md) — 安装与第一个示例
- [在线 Demo](online_demo.md) — Hugging Face 体验
- [安装](installation.md) — 详细安装说明
- [使用方式](usage.md) — Python 与终端用法
- [GPU 推理](gpu-inference.md) — 使用 GPU 加速
- [NPU 使用](npu-usage.md) — NPU 配置
- [参考项目](references.md) — 相关开源项目
