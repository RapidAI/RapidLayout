# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import sys
from pathlib import Path

import pytest

cur_dir = Path(__file__).resolve().parent
root_dir = cur_dir.parent

sys.path.insert(0, str(root_dir))

from rapid_layout import EngineType, ModelType, RapidLayout, RapidLayoutInput

test_dir = cur_dir / "test_files"

# 与 test_main.py 保持一致：(图片名, 模型类型, 期望检测框数量)
ENGINE_TEST_CASES = [
    ("layout.jpg", "pp_layout_cdla", 14),
    ("PMC3576793_00004.jpg", "yolov8n_layout_publaynet", 12),
    ("PMC3576793_00004.jpg", "yolov8n_layout_general6", 13),
    ("PMC3576793_00004.jpg", "doclayout_docstructbench", 14),
]


def get_engine(params: RapidLayoutInput):
    return RapidLayout(cfg=params)


@pytest.mark.parametrize("img_name, model_type, gt", ENGINE_TEST_CASES)
def test_engine_onnxruntime(img_name, model_type, gt):
    """使用 onnxruntime 引擎推理，结果与 test_main 预期一致。"""
    params = RapidLayoutInput(
        model_type=ModelType(model_type),
        engine_type=EngineType.ONNXRUNTIME,
    )
    engine = get_engine(params)
    img_path = test_dir / img_name
    results = engine(img_path)

    assert results.boxes is not None
    assert len(results.boxes) == gt


@pytest.mark.parametrize("img_name, model_type, gt", ENGINE_TEST_CASES)
def test_engine_openvino(img_name, model_type, gt):
    """使用 openvino 引擎推理，结果与 test_main 预期一致。"""
    pytest.importorskip(
        "openvino", reason="openvino not installed, skip openvino tests"
    )
    params = RapidLayoutInput(
        model_type=ModelType(model_type),
        engine_type=EngineType.OPENVINO,
    )
    engine = get_engine(params)
    img_path = test_dir / img_name
    results = engine(img_path)

    assert results.boxes is not None
    assert len(results.boxes) == gt
