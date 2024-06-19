## Rapid Layout
<p align="left">
    <a href=""><img src="https://img.shields.io/badge/Python->=3.6,<3.12-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/OS-Linux%2C%20Win%2C%20Mac-pink.svg"></a>
    <a href="https://pypi.org/project/rapid-layout/"><img alt="PyPI" src="https://img.shields.io/pypi/v/rapid-layout"></a>
    <a href="https://pepy.tech/project/rapid-layout"><img src="https://static.pepy.tech/personalized-badge/rapid-layout?period=total&units=abbreviation&left_color=grey&right_color=blue&left_text=Downloads"></a>
</p>

#### 简介和说明
- 该部分主要是做文档类图像的版面分析。模型来源：[PaddleOCR 版面分析](https://github.com/PaddlePaddle/PaddleOCR/blob/133d67f27dc8a241d6b2e30a9f047a0fb75bebbe/ppstructure/layout/README_ch.md)
- 具体来说，就是分析给定的文档类别图像（论文截图等），定位其中类别和位置，如标题、段落、表格和图片等各个部分。
- 目前支持三种类别的版面分析模型：中文、英文和表格版面分析模型，具体可参见下面表格：

    |`model_type`| 版面类型 |        模型名称          |  支持类别|
    | :------ | :----- | :------ | :----- |
    |`pp_layout_table`|   表格   |   `layout_table.onnx`     |`table` |
    | `pp_layout_publaynet`|   英文   | `layout_publaynet.onnx`   |`text title list table figure` |
    | `pp_layout_table`|   中文   |   `layout_cdla.onnx`    | `text title figure  figure_caption table table_caption` <br> `header footer reference equation` |

- 模型下载地址为：[百度网盘](https://pan.baidu.com/s/1PI9fksW6F6kQfJhwUkewWg?pwd=p29g) | [Google Drive](https://drive.google.com/drive/folders/1DAPWSN2zGQ-ED_Pz7RaJGTjfkN2-Mvsf?usp=sharing)

#### 安装
由于模型较小，预先将中文版面分析模型(`layout_cdla.onnx`)打包进了whl包内，如果做中文版面分析，可直接安装使用

```bash
$ pip install rapid-layout
```

#### 使用方式
1. python脚本运行
    ```python
    import cv2
    from rapid_layout import RapidLayout，vis_layout

    # model_type类型参见上表。指定不同model_type时，会自动下载相应模型到安装目录下的。
    layout_engine = RapidLayout(box_threshold=0.5, model_type="pp_layout_cdla")

    img = cv2.imread('test_images/layout.png')

    layout_res, elapse = layout_engine(img)

    ploted_img = vis_layout(img, layout_res)
    cv2.imwrite("layout_res.png", ploted_img)
    print(layout_res)
    ```

2. 终端运行
   - 用法:
        ```bash
        $ rapid_layout -h
        usage: rapid_layout [-h] -img IMG_PATH [-m {pp_layout_cdla,pp_layout_publaynet,pp_layout_table}]
                            [--box_threshold {pp_layout_cdla,pp_layout_publaynet,pp_layout_table}] [-v]

        options:
        -h, --help            show this help message and exit
        -img IMG_PATH, --img_path IMG_PATH
                                Path to image for layout.
        -m {pp_layout_cdla,pp_layout_publaynet,pp_layout_table}, --model_type {pp_layout_cdla,pp_layout_publaynet,pp_layout_table}
                                Support model type
        --box_threshold {pp_layout_cdla,pp_layout_publaynet,pp_layout_table}
                                Box threshold, the range is [0, 1]
        -v, --vis             Wheter to visualize the layout results.
        ```
   - 示例:
     ```bash
     $ rapid_layout -v -img test_images/layout.png
     ```

3. 结果
    - 返回结果
        ```python
        # bbox: [左上角x0,左上角y0, 右下角x1, 右下角y1]
        # label: 类别
        [
            {'bbox': array([321.4160495, 91.53214898, 562.06141263, 199.85522603]), 'label': 'text'},
            {'bbox': array([58.67292211, 107.29000663, 300.25448676, 199.68142]), 'label': 'table_caption'}
        ]
        ```
   - 可视化结果
    <div align="center">
        <img src="https://github.com/RapidAI/RapidStructure/releases/download/v0.0.0/layout_result.jpg" width="80%" height="80%">
    </div>
