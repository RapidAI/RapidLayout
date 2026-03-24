---
comments: true
title: 模型列表
hide:
  - navigation
  - toc
---

!!! tip

    由于不同场景下的版面差异较大，现阶段不存在一个模型可以搞定所有场景。如果实际业务需要，以下模型效果不好的话，建议构建自己的训练集微调。

| `model_type` | 版面类型 | 支持类别 |
| :------ | :----- | :----- |
|`pp_doc_layoutv3 (rapid_layout>=1.2.0)`|文档|`['abstract', 'algorithm', 'aside_text', 'chart', 'content', 'display_formula', 'doc_title', 'figure_title', 'footer', 'footer_image', 'footnote', 'formula_number', 'header', 'header_image', 'image', 'inline_formula', 'number', 'paragraph_title', 'reference', 'reference_content', 'seal', 'table', 'text', 'vertical_text', 'vision_footnote']`|
|`pp_doc_layoutv2 (rapid_layout>=1.1.0)`|文档|`['abstract', 'algorithm', 'aside_text', 'chart', 'content', 'display_formula', 'doc_title', 'figure_title', 'footer', 'footer_image', 'footnote', 'formula_number', 'header', 'header_image', 'image', 'inline_formula', 'number', 'paragraph_title', 'reference', 'reference_content', 'seal', 'table', 'text', 'vertical_text', 'vision_footnote']`|
||||
| `pp_layout_table` | 表格 | `["table"]` |
| `pp_layout_publaynet` | 英文 | `["text", "title", "list", "table", "figure"]` |
| `pp_layout_cdla` | 中文 | `['text', 'title', 'figure', 'figure_caption', 'table', 'table_caption', 'header', 'footer', 'reference', 'equation']` |
||||
| `yolov8n_layout_paper` | 论文 | `['Text', 'Title', 'Header', 'Footer', 'Figure', 'Table', 'Toc', 'Figure caption', 'Table caption']` |
| `yolov8n_layout_report` | 研报 | `['Text', 'Title', 'Header', 'Footer', 'Figure', 'Table', 'Toc', 'Figure caption', 'Table caption']` |
| `yolov8n_layout_publaynet` | 英文 | `["Text", "Title", "List", "Table", "Figure"]` |
| `yolov8n_layout_general6` | 通用 | `["Text", "Title", "Figure", "Table", "Caption", "Equation"]` |
||||
| `doclayout_docstructbench` | 通用 | `['title', 'plain text', 'abandon', 'figure', 'figure_caption', 'table', 'table_caption', 'table_footnote', 'isolate_formula', 'formula_caption']` |
| `doclayout_d4la` | 通用 | `['DocTitle', 'ParaTitle', 'ParaText', 'ListText', 'RegionTitle', 'Date', 'LetterHead', 'LetterDear', 'LetterSign', 'Question', 'OtherText', 'RegionKV', 'RegionList', 'Abstract', 'Author', 'TableName', 'Table', 'Figure', 'FigureName', 'Equation', 'Reference', 'Footer', 'PageHeader', 'PageFooter', 'Number', 'Catalog', 'PageNumber']` |
| `doclayout_docsynth` | 通用 | `['Caption', 'Footnote', 'Formula', 'List-item', 'Page-footer', 'Page-header', 'Picture', 'Section-header', 'Table', 'Text', 'Title']` |

## 模型来源

**🔥 PP-DocLayoutV3**: [PP-DocLayoutV2](https://huggingface.co/PaddlePaddle/PP-DocLayoutV3)

**🔥 PP-DocLayoutV2**: [PP-DocLayoutV2](https://huggingface.co/PaddlePaddle/PP-DocLayoutV2)

**PP 模型**：[PaddleOCR 版面分析](https://github.com/PaddlePaddle/PaddleOCR/blob/133d67f27dc8a241d6b2e30a9f047a0fb75bebbe/ppstructure/layout/README_ch.md)

**yolov8n 系列**：[360LayoutAnalysis](https://github.com/360AILAB-NLP/360LayoutAnalysis)

**doclayout_yolo（推荐）**：[DocLayout-YOLO](https://github.com/opendatalab/DocLayout-YOLO)，目前较为优秀的开源版面分析模型，提供基于不同训练集的三个模型：

- `doclayout_docstructbench`：[Hugging Face](https://huggingface.co/juliozhao/DocLayout-YOLO-DocStructBench/tree/main)
- `doclayout_d4la`：[Hugging Face](https://huggingface.co/juliozhao/DocLayout-YOLO-D4LA-Docsynth300K_pretrained/blob/main/doclayout_yolo_d4la_imgsz1600_docsynth_pretrain.pt)
- `doclayout_docsynth`：[Hugging Face](https://huggingface.co/juliozhao/DocLayout-YOLO-DocLayNet-Docsynth300K_pretrained/tree/main)

## 模型下载

模型均已经托管在 [魔搭平台](https://www.modelscope.cn/models/RapidAI/RapidLayout/files)。
