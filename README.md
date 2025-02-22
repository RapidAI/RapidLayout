<div align="center">
  <div align="center">
    <h1><b>📖 Rapid Layout</b></h1>
  </div>

<a href="https://huggingface.co/spaces/SWHL/RapidLayout" target="_blank"><img src="https://img.shields.io/badge/%F0%9F%A4%97-Hugging Face Demo-blue"></a>
<a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.13-aff.svg"></a>
<a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
<a href="https://pypi.org/project/rapid-layout/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapid-layout"></a>
<a href="https://pepy.tech/project/rapid-layout"><img src="https://static.pepy.tech/personalized-badge/rapid-layout?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
<a href="https://semver.org/"><img alt="SemVer2.0" src="https://img.shields.io/badge/SemVer-2.0-brightgreen"></a>
<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</div>

### 简介

该项目主要是汇集全网开源的版面分析的项目，具体来说，就是分析给定的文档类别图像（论文截图、研报等），定位其中类别和位置，如标题、段落、表格和图片等各个部分。

⚠️注意：需要说明的是，由于不同场景下的版面差异较大，现阶段不存在一个模型可以搞定所有场景。如果实际业务需要，以下模型效果不好的话，建议构建自己的训练集微调。

目前支持已经支持的版面分析模型如下：

|`model_type`| 版面类型 |  支持类别|
| :------ | :----- | :----- |
|`pp_layout_table`|   表格   |`["table"]` |
| `pp_layout_publaynet`|   英文   |`["text", "title", "list", "table", "figure"]` |
| `pp_layout_cdla`|   中文    | `['text', 'title', 'figure', 'figure_caption', 'table', 'table_caption', 'header', 'footer', 'reference', 'equation']` |
| `yolov8n_layout_paper`|   论文    | `['Text', 'Title', 'Header', 'Footer', 'Figure', 'Table', 'Toc', 'Figure caption', 'Table caption']` |
| `yolov8n_layout_report`|   研报    | `['Text', 'Title', 'Header', 'Footer', 'Figure', 'Table', 'Toc', 'Figure caption', 'Table caption']` |
| `yolov8n_layout_publaynet`|   英文     | `["Text", "Title", "List", "Table", "Figure"]` |
| `yolov8n_layout_general6`|   通用      | `["Text", "Title", "Figure", "Table", "Caption", "Equation"]` |
| 🔥`doclayout_docstructbench`|   通用   | `['title', 'plain text', 'abandon', 'figure', 'figure_caption', 'table', 'table_caption', 'table_footnote', 'isolate_formula', 'formula_caption']` |
| 🔥`doclayout_d4la`|   通用       | `['DocTitle', 'ParaTitle', 'ParaText', 'ListText', 'RegionTitle', 'Date', 'LetterHead', 'LetterDear', 'LetterSign', 'Question', 'OtherText', 'RegionKV', 'RegionList', 'Abstract', 'Author', 'TableName', 'Table', 'Figure', 'FigureName', 'Equation', 'Reference', 'Footer', 'PageHeader', 'PageFooter', 'Number', 'Catalog', 'PageNumber']` |
| 🔥`doclayout_docsynth`|   通用    | `['Caption', 'Footnote', 'Formula', 'List-item', 'Page-footer', 'Page-header', 'Picture', 'Section-header', 'Table', 'Text', 'Title']` |

PP模型来源：[PaddleOCR 版面分析](https://github.com/PaddlePaddle/PaddleOCR/blob/133d67f27dc8a241d6b2e30a9f047a0fb75bebbe/ppstructure/layout/README_ch.md)

yolov8n系列来源：[360LayoutAnalysis](https://github.com/360AILAB-NLP/360LayoutAnalysis)

（推荐使用）🔥doclayout_yolo模型来源：[DocLayout-YOLO](https://github.com/opendatalab/DocLayout-YOLO)，该模型是目前最为优秀的开源模型，挑选了3个基于不同训练集训练得到的模型。其中`doclayout_docstructbench`来自[link](https://huggingface.co/juliozhao/DocLayout-YOLO-DocStructBench/tree/main)，`doclayout_d4la`来自[link](https://huggingface.co/juliozhao/DocLayout-YOLO-D4LA-Docsynth300K_pretrained/blob/main/doclayout_yolo_d4la_imgsz1600_docsynth_pretrain.pt)，`doclayout_docsynth`来自[link](https://huggingface.co/juliozhao/DocLayout-YOLO-DocLayNet-Docsynth300K_pretrained/tree/main)。

上述模型下载地址为：[link](https://github.com/RapidAI/RapidLayout/releases/tag/v0.0.0)

### TODO

- [ ] [ PP-DocLayout](https://github.com/PaddlePaddle/PaddleX/blob/release/3.0-rc/docs/module_usage/tutorials/ocr_modules/layout_detection.md)整理

### 安装

由于模型较小，预先将中文版面分析模型(`layout_cdla.onnx`)打包进了whl包内，如果做中文版面分析，可直接安装使用

```bash
pip install rapid-layout
```

### 使用方式

#### python脚本运行

```python
import cv2
from imread_from_url import imread_from_url  # pip install imread_from_url

from rapid_layout import RapidLayout, VisLayout

# model_type类型参见上表。指定不同model_type时，会自动下载相应模型到安装目录下的。
layout_engine = RapidLayout(model_type="doclayout_docstructbench", conf_thres=0.2)

img_url = "https://raw.githubusercontent.com/opendatalab/DocLayout-YOLO/refs/heads/main/assets/example/financial.jpg"
img = imread_from_url(img_url)

boxes, scores, class_names, elapse = layout_engine(img)
ploted_img = VisLayout.draw_detections(img, boxes, scores, class_names)
if ploted_img is not None:
    cv2.imwrite("layout_res.png", ploted_img)
```

### 可视化结果

<div align="center">
    <img src="https://github.com/RapidAI/RapidLayout/releases/download/v0.0.0/layout_res.png" width="80%" height="80%">
</div>

#### 终端运行

```bash
$ rapid_layout -h
usage: rapid_layout [-h] -img IMG_PATH
                    [-m {pp_layout_cdla,pp_layout_publaynet,pp_layout_table,yolov8n_layout_paper,yolov8n_layout_report,yolov8n_layout_publaynet,yolov8n_layout_general6,doclayout_docstructbench,doclayout_d4la,doclayout_docsynth}]
                    [--conf_thres {pp_layout_cdla,pp_layout_publaynet,pp_layout_table,yolov8n_layout_paper,yolov8n_layout_report,yolov8n_layout_publaynet,yolov8n_layout_general6,doclayout_docstructbench,doclayout_d4la,doclayout_docsynth}]
                    [--iou_thres {pp_layout_cdla,pp_layout_publaynet,pp_layout_table,yolov8n_layout_paper,yolov8n_layout_report,yolov8n_layout_publaynet,yolov8n_layout_general6,doclayout_docstructbench,doclayout_d4la,doclayout_docsynth}]
                    [--use_cuda] [--use_dml] [-v]

options:
  -h, --help            show this help message and exit
  -img IMG_PATH, --img_path IMG_PATH
                        Path to image for layout.
  -m {pp_layout_cdla,pp_layout_publaynet,pp_layout_table,yolov8n_layout_paper,yolov8n_layout_report,yolov8n_layout_publaynet,yolov8n_layout_general6,doclayout_docstructbench,doclayout_d4la,doclayout_docsynth}, --model_type {pp_layout_cdla,pp_layout_publaynet,pp_layout_table,yolov8n_layout_paper,yolov8n_layout_report,yolov8n_layout_publaynet,yolov8n_layout_general6,doclayout_docstructbench,doclayout_d4la,doclayout_docsynth}
                        Support model type
  --conf_thres {pp_layout_cdla,pp_layout_publaynet,pp_layout_table,yolov8n_layout_paper,yolov8n_layout_report,yolov8n_layout_publaynet,yolov8n_layout_general6,doclayout_docstructbench,doclayout_d4la,doclayout_docsynth}
                        Box threshold, the range is [0, 1]
  --iou_thres {pp_layout_cdla,pp_layout_publaynet,pp_layout_table,yolov8n_layout_paper,yolov8n_layout_report,yolov8n_layout_publaynet,yolov8n_layout_general6,doclayout_docstructbench,doclayout_d4la,doclayout_docsynth}
                        IoU threshold, the range is [0, 1]
  --use_cuda            Whether to use cuda.
  --use_dml             Whether to use DirectML, which only works in Windows10+.
  -v, --vis             Wheter to visualize the layout results.
```

- 示例:

    ```bash
    rapid_layout -v -img test_images/layout.png
    ```

### GPU推理

- 因为版面分析模型输入图像尺寸固定，故可使用`onnxruntime-gpu`来提速。
- 因为`rapid_layout`库默认依赖是CPU版`onnxruntime`，如果想要使用GPU推理，需要手动安装`onnxruntime-gpu`。
- 详细使用和评测可参见[AI Studio](https://aistudio.baidu.com/projectdetail/8094594)

#### 安装

```bash
pip install rapid_layout
pip uninstall onnxruntime

# 这里一定要确定onnxruntime-gpu与GPU对应
# 可参见https://onnxruntime.ai/docs/execution-providers/CUDA-ExecutionProvider.html#requirements
pip install onnxruntime-gpu
```

#### 使用

```python
import cv2
from rapid_layout import RapidLayout
from pathlib import Path

# 注意：这里需要使用use_cuda指定参数
layout_engine = RapidLayout(model_type="doclayout_yolo", conf_thres=0.2, use_cuda=True)

# warm up
layout_engine("images/12027_5.png")

elapses = []
img_list = list(Path('images').iterdir())
for img_path in img_list:
    boxes, scores, class_names, elapse = layout_engine(img_path)
    print(f"{img_path}: {elapse}s")
    elapses.append(elapse)

avg_elapse = sum(elapses) / len(elapses)
print(f'avg elapse: {avg_elapse:.4f}')
```

### 参考项目

- [DocLayout-YOLO](https://github.com/opendatalab/DocLayout-YOLO)
- [PP-Structure](https://github.com/PaddlePaddle/PaddleOCR/blob/133d67f27dc8a241d6b2e30a9f047a0fb75bebbe/ppstructure/layout/README_ch.md)
- [360LayoutAnalysis](https://github.com/360AILAB-NLP/360LayoutAnalysis)
- [ONNX-YOLOv8-Object-Detection](https://github.com/ibaiGorordo/ONNX-YOLOv8-Object-Detection)
- [ChineseDocumentPDF](https://github.com/SWHL/ChineseDocumentPDF)
