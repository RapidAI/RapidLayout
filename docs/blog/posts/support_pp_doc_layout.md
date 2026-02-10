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

    ```text

    ```

### 转换命令

```bash
paddle2onnx  --model_dir=models/PP-DocLayoutV2  --model_filename inference.json --params_filename inference.pdiparams  --save_file=./models/PP-DocLayoutV2/inference_v2.onnx  --enable_onnx_checker=True
```

#### 比较结果

按照上面直接转换后，在相同输入下，ONNX模型和Paddle模型推理误差较大。

```bash
>> np.testing.assert_allclose(batch_preds[0], ort_outputs[0], atol=1e-3, rtol=0)
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "/xxx/miniforge3/envs/wjh_debug/lib/python3.10/site-packages/numpy/testing/_private/utils.py", line 1504, in assert_allclose
    assert_array_compare(compare, actual, desired, err_msg=str(err_msg),
  File "/xxx/miniforge3/envs/wjh_debug/lib/python3.10/contextlib.py", line 79, in inner
    return func(*args, **kwds)
  File "/xxx/miniforge3/envs/wjh_debug/lib/python3.10/site-packages/numpy/testing/_private/utils.py", line 797, in assert_array_compare
    raise AssertionError(msg)
AssertionError:
Not equal to tolerance rtol=0, atol=0.001

Mismatched elements: 1321 / 2400 (55%)
Max absolute difference: 819.32886
Max relative difference: 294.
 x: array([[2.200000e+01, 9.889959e-01, 3.354025e+01, ..., 6.150441e+02,
        2.900000e+02, 2.900000e+02],
       [2.200000e+01, 9.888721e-01, 3.372420e+01, ..., 8.526017e+02,...
 y: array([[2.200000e+01, 9.889925e-01, 3.354081e+01, ..., 6.150450e+02,
        2.900000e+02, 2.900000e+02],
       [2.200000e+01, 9.888635e-01, 3.372382e+01, ..., 8.526024e+02,...
```
