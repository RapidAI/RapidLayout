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
paddle2onnx  --model_dir=models/PP-DocLayoutV2  --model_filename inference.json --params_filename inference.pdiparams  --save_file=./models/PP-DocLayoutV2/inference_v2.onnx  --enable_onnx_checker=True
```

#### 比较结果

我在`/xxxx/miniforge3/envs/wjh_debug/lib/python3.10/site-packages/paddlex/inference/models/layout_analysis/predictor.py`中插入以下代码（在 **L103** 行左右），来保证输入相同，比较输出。

按照上面直接转换后，在相同输入下，ONNX模型和Paddle模型推理结果误差为 **14.8%** 。在我看来，这个误差其实挺大的。

但是从可视化示例图结果来看，两者并无明显区别。可能在某些图上会有较大区别。

```python linenums="1"

# 省略前面代码... ...

import onnxruntime
import numpy as np

model_path = "models/PP-DocLayoutV2/inference_v5_op15_pd_cpu_fixed.onnx"
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
