<div align="center">
  <div align="center">
    <h1><b>📖 Rapid Layout</b></h1>
  </div>

<a href="https://huggingface.co/spaces/SWHL/RapidLayout" target="_blank"><img src="https://img.shields.io/badge/%F0%9F%A4%97-Hugging Face Demo-blue"></a>
<a href="https://www.modelscope.cn/studios/liekkas/RapidLayout" target="_blank"><img src="https://img.shields.io/badge/ModelScope-Demo-blue"></a>
<a href="https://aistudio.baidu.com/app/highcode/37154" target="_blank"><img src="https://img.shields.io/badge/AI%20Studio-Demo-blue"></a>
<a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.13-aff.svg"></a>
<a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
<a href="https://pypi.org/project/rapid-layout/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapid-layout"></a>
<a href="https://pepy.tech/project/rapid-layout"><img src="https://static.pepy.tech/personalized-badge/rapid-layout?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
<a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</div>

### 简介
主要是做文档类图像的版面分析。具体来说，就是分析给定的文档类别图像（论文截图、研报等），定位其中类别和位置，如标题、段落、表格和图片等各个部分。

目前支持三种类别，两种场景的版面分析，具体参见下面表格：

|`model_type`| 版面类型 |        模型名称          |  支持类别|
| :------ | :----- | :------ | :----- |
|`pp_layout_table`|   表格   |   `layout_table.onnx`     |`["table"]` |
| `pp_layout_publaynet`|   英文   | `layout_publaynet.onnx`   |`["text", "title", "list", "table", "figure"]` |
| `pp_layout_cdla`|   中文   |   `layout_cdla.onnx`    | `['text', 'title', 'figure', 'figure_caption', 'table', 'table_caption', 'header', 'footer', 'reference', 'equation']` |
| `yolov8n_layout_paper`|   论文   |   `yolov8n_layout_paper.onnx`    | `['text', 'title', 'figure', 'figure_caption', 'table', 'table_caption', 'header', 'footer', 'reference', 'equation']` |
| `yolov8n_layout_report`|   研报   |   `yolov8n_layout_report.onnx`    | `['text', 'title', 'header', 'footer', 'figure', 'figure_caption', 'table', 'table_caption', 'toc']` |

PP模型来源：[PaddleOCR 版面分析](https://github.com/PaddlePaddle/PaddleOCR/blob/133d67f27dc8a241d6b2e30a9f047a0fb75bebbe/ppstructure/layout/README_ch.md)

yolov8n系列来源：[360LayoutAnalysis](https://github.com/360AILAB-NLP/360LayoutAnalysis)

模型下载地址为：[link](https://github.com/RapidAI/RapidLayout/releases/tag/v0.0.0)

### 安装
由于模型较小，预先将中文版面分析模型(`layout_cdla.onnx`)打包进了whl包内，如果做中文版面分析，可直接安装使用

```bash
$ pip install rapid-layout
```

### 使用方式
#### python脚本运行
```python
import cv2
from rapid_layout import RapidLayout, VisLayout

# model_type类型参见上表。指定不同model_type时，会自动下载相应模型到安装目录下的。
layout_engine = RapidLayout(conf_thres=0.5, model_type="pp_layout_cdla")

img = cv2.imread('test_images/layout.png')

boxes, scores, class_names, *elapse = layout_engine(img)
ploted_img = VisLayout.draw_detections(img, boxes, scores, class_names)
if ploted_img is not None:
    cv2.imwrite("layout_res.png", ploted_img)
```

#### 终端运行
- 用法:
    ```bash
    $ rapid_layout -h
    usage: rapid_layout [-h] -img IMG_PATH
                        [-m {pp_layout_cdla,pp_layout_publaynet,pp_layout_table,yolov8n_layout_paper,yolov8n_layout_report}]
                        [--conf_thres {pp_layout_cdla,pp_layout_publaynet,pp_layout_table,yolov8n_layout_paper,yolov8n_layout_report}]
                        [--iou_thres {pp_layout_cdla,pp_layout_publaynet,pp_layout_table,yolov8n_layout_paper,yolov8n_layout_report}]
                        [-v]

    options:
      -h, --help            show this help message and exit
      -img IMG_PATH, --img_path IMG_PATH
                            Path to image for layout.
      -m {pp_layout_cdla,pp_layout_publaynet,pp_layout_table,yolov8n_layout_paper,yolov8n_layout_report}, --model_type {pp_layout_cdla,pp_layout_publaynet,pp_layout_table,yolov8n_layout_paper,yolov8n_layout_report}
                            Support model type
      --conf_thres {pp_layout_cdla,pp_layout_publaynet,pp_layout_table,yolov8n_layout_paper,yolov8n_layout_report}
                            Box threshold, the range is [0, 1]
      --iou_thres {pp_layout_cdla,pp_layout_publaynet,pp_layout_table,yolov8n_layout_paper,yolov8n_layout_report}
                            IoU threshold, the range is [0, 1]
      -v, --vis             Wheter to visualize the layout results.
    ```
- 示例:
    ```bash
    $ rapid_layout -v -img test_images/layout.png
    ```

### 可视化结果

<div align="center">
    <img src="https://github.com/RapidAI/RapidLayout/releases/download/v0.0.0/layout_res.png" width="80%" height="80%">
</div>
