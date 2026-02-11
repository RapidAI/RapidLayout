---
title: 支持PP-DocLayoutV2/V3系列模型
date:
  created: 2026-02-10
authors: [SWHL]
slug: support-PP-DocLayoutv2-v3
categories:
  - General
comments: true
---

本篇文章主要记录如何集成PP-DocLayoutV2/V3模型的

<!-- more -->

### 引言

PP-DocLayout系列模型在版面分析方面效果很好，目前已经作为PaddleOCR-VL系列模型的前置，起着至关重要的作用。

文档智能的关键地方就在于此。因此，想着将该模型纳入RapidLayout系列模型中，方便小伙伴们快速使用。

### 运行环境

- 操作系统： Ubuntu
- Python： 3.10.14
- 其他依赖环境：

    ```text linenums="1"
    paddle2onnx==2.1.0
    paddlepaddle==3.3.0
    onnx==1.17.0
    onnxruntime==1.23.2
    ```

### 转换命令

```bash
paddle2onnx  --model_dir=models/PP-DocLayoutV2  --model_filename inference.json --params_filename inference.pdiparams  --save_file=./models/PP-DocLayoutV2/inference.onnx  --enable_onnx_checker=True
```

### 比较结果

我在`/xxxx/miniforge3/envs/wjh_debug/lib/python3.10/site-packages/paddlex/inference/models/layout_analysis/predictor.py`中插入以下代码（在 **L103** 行左右），来保证输入相同，比较输出。

#### PP-DocLayoutV2

按照上面直接转换后，在相同输入下，ONNX模型和Paddle模型推理结果误差为 **14.8%** 。在我看来，这个误差其实挺大的。

但是从可视化示例图结果来看，两者并无明显区别。可能在某些图上会有较大区别。

```python linenums="1" title="比较两种格式模型推理结果"

# 省略前面代码... ...

import onnxruntime
import numpy as np

model_path = "models/PP-DocLayoutV2/inference.onnx"
ort_session = onnxruntime.InferenceSession(model_path)
ort_inputs = {
    "im_shape": batch_inputs[0],
    "image": batch_inputs[1],
    "scale_factor": batch_inputs[2],
}
ort_outputs = ort_session.run(None, ort_inputs)

# do infer
batch_preds = self.infer(batch_inputs)

# 千分位是否相同
np.testing.assert_allclose(batch_preds[0], ort_outputs[0], atol=1e-3, rtol=0)
```

输出结果如下：

```bash linenums="1" hl_lines="21-23"
Traceback (most recent call last):
  File "/xxxx/paddleocr/test_pp_doc_layoutv2.py", line 4, in <module>
    output = model.predict(
  File "/xxxx/lib/python3.10/site-packages/paddleocr/_models/base.py", line 57, in predict
    result = list(self.predict_iter(*args, **kwargs))
  File "/xxxx/lib/python3.10/site-packages/paddlex/inference/models/base/predictor/base_predictor.py", line 281, in __call__
    yield from self.apply(input, **kwargs)
  File "/xxxx/lib/python3.10/site-packages/paddlex/inference/models/base/predictor/base_predictor.py", line 338, in apply
    prediction = self.process(batch_data, **kwargs)
  File "/xxxx/lib/python3.10/site-packages/paddlex/inference/models/layout_analysis/predictor.py", line 119, in process
    np.testing.assert_allclose(batch_preds[0], ort_outputs[0], atol=1e-3, rtol=0)
  File "/xxxx/lib/python3.10/site-packages/numpy/testing/_private/utils.py", line 1504, in assert_allclose
    assert_array_compare(compare, actual, desired, err_msg=str(err_msg),
  File "/xxxx/lib/python3.10/contextlib.py", line 79, in inner
    return func(*args, **kwds)
  File "/xxxx/lib/python3.10/site-packages/numpy/testing/_private/utils.py", line 797, in assert_array_compare
    raise AssertionError(msg)
AssertionError:
Not equal to tolerance rtol=0, atol=0.001

Mismatched elements: 354 / 2400 (14.8%)
Max absolute difference: 196.
Max relative difference: 194.
 x: array([[2.200000e+01, 9.889924e-01, 3.354079e+01, ..., 6.150450e+02,
        2.900000e+02, 2.900000e+02],
       [2.200000e+01, 9.888635e-01, 3.372379e+01, ..., 8.526023e+02,...
 y: array([[2.200000e+01, 9.889925e-01, 3.354081e+01, ..., 6.150450e+02,
        2.900000e+02, 2.900000e+02],
       [2.200000e+01, 9.888635e-01, 3.372382e+01, ..., 8.526024e+02,...
```

暂时先用这个ONNX模型，该问题已经反馈到了Paddle2ONNX issue [#1608](https://github.com/PaddlePaddle/Paddle2ONNX/issues/1608#issuecomment-3875561303)

#### PP-DocLayoutV3

和 PP-DocLayoutV2 相同环境，相同转换代码，这个模型误差就小很多了，仅有 **1.57%**了。

```bash
AssertionError:
Not equal to tolerance rtol=0, atol=0.001

Mismatched elements: 33 / 2100 (1.57%)
Max absolute difference among violations: 1.
Max relative difference among violations: 0.01754386
 ACTUAL: array([[2.200000e+01, 9.658169e-01, 3.387792e+01, ..., 3.626684e+02,
        8.528884e+02, 1.540000e+02],
       [2.200000e+01, 9.657925e-01, 3.363610e+01, ..., 3.633332e+02,...
 DESIRED: array([[2.200000e+01, 9.658167e-01, 3.387791e+01, ..., 3.626685e+02,
        8.528885e+02, 1.530000e+02],
       [2.200000e+01, 9.657924e-01, 3.363615e+01, ..., 3.633333e+02,...
```

### 剥离推理代码

因为PaddleOCR库中需要兼容的推理代码较多，大而全。这也导致了有些臃肿。这是难以避免的。但是如果只看PP-DocLayout推理代码的话，很多问题就很简单了。

完整的推理代码，我放到了Gist上 → [link](https://gist.github.com/SWHL/c9455e8947f4abdfbbd8439c0bb83410)

### 字典写入 ONNX

```python linenums="1" title="write_dict.py"
from pathlib import Path
from typing import List, Union

import onnx
import onnxruntime as ort
from onnx import ModelProto


class ONNXMetaOp:
    @classmethod
    def add_meta(
        cls,
        model_path: Union[str, Path],
        key: str,
        value: List[str],
        delimiter: str = "\n",
    ) -> ModelProto:
        model = onnx.load_model(model_path)
        meta = model.metadata_props.add()
        meta.key = key
        meta.value = delimiter.join(value)
        return model

    @classmethod
    def get_meta(
        cls, model_path: Union[str, Path], key: str, split_sym: str = "\n"
    ) -> List[str]:
        sess = ort.InferenceSession(model_path)
        meta_map = sess.get_modelmeta().custom_metadata_map
        key_content = meta_map.get(key)
        key_list = key_content.split(split_sym)
        return key_list

    @classmethod
    def del_meta(cls, model_path: Union[str, Path]) -> ModelProto:
        model = onnx.load_model(model_path)
        del model.metadata_props[:]
        return model

    @classmethod
    def save_model(cls, save_path: Union[str, Path], model: ModelProto):
        onnx.save_model(model, save_path)


paper_label = [
    "abstract",
    "algorithm",
    "aside_text",
    "chart",
    "content",
    "display_formula",
    "doc_title",
    "figure_title",
    "footer",
    "footer_image",
    "footnote",
    "formula_number",
    "header",
    "header_image",
    "image",
    "inline_formula",
    "number",
    "paragraph_title",
    "reference",
    "reference_content",
    "seal",
    "table",
    "text",
    "vertical_text",
    "vision_footnote",
]
model_path = "models/inference.onnx"
model = ONNXMetaOp.add_meta(model_path, key="character", value=paper_label)

new_model_path = "models/pp_doc_layoutv2.onnx"
ONNXMetaOp.save_model(new_model_path, model)

t = ONNXMetaOp.get_meta(new_model_path, key="character")
print(t)
```

输出以下`label`，则认为成功：

```bash linenums="1"
$ python write_dict.py
['abstract', 'algorithm', 'aside_text', 'chart', 'content', 'display_formula', 'doc_title', 'figure_title', 'footer', 'footer_image', 'footnote', 'formula_number', 'header', 'header_image', 'image', 'inline_formula', 'number', 'paragraph_title', 'reference', 'reference_content', 'seal', 'table', 'text', 'vertical_text', 'vision_footnote']
```

PP-DocLayoutV2 和 PP-DocLayoutV3 字典是一样的。

### 使用

目前 PP-DocLayoutV2 在`rapid_layout>=1.1.0`已经支持。PP-DocLayoutV3 在`rapid_layout>=1.2.0`中支持。使用示例：

```python linenums="1"
from rapid_layout import EngineType, ModelType, RapidLayout

layout_engine = RapidLayout(
    engine_type=EngineType.ONNXRUNTIME,
    model_type=ModelType.PP_DOC_LAYOUTV2,
)

img_url = "https://www.modelscope.cn/models/RapidAI/RapidLayout/resolve/master/resources/test_files/pp_doc_layoutv2_layout.jpg"
results = layout_engine(img_url)
print(results)

results.vis("layout_res.png")
```
