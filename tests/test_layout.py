# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import sys
from pathlib import Path

import cv2
import pytest

cur_dir = Path(__file__).resolve().parent
root_dir = cur_dir.parent

sys.path.append(str(root_dir))

from rapid_layout import RapidLayout
from rapid_layout.utils import LoadImageError

test_file_dir = cur_dir / "test_files"
img_path = test_file_dir / "layout.png"

img = cv2.imread(str(img_path))


@pytest.mark.parametrize(
    "model_type,gt",
    [
        ("yolov8n_layout_publaynet", 12),
        ("yolov8n_layout_general6", 13),
        (
            "doclayout_docstructbench",
            14,
        ),
        ("doclayout_d4la", 11),
        ("doclayout_docsynth", 14),
    ],
)
def test_layout(model_type, gt):
    img_path = test_file_dir / "PMC3576793_00004.jpg"
    engine = RapidLayout(model_type=model_type)
    boxes, scores, class_names, *elapse = engine(img_path)
    assert len(boxes) == gt


@pytest.mark.parametrize(
    "img_content", [img_path, str(img_path), open(img_path, "rb").read(), img]
)
def test_pp_layout(img_content):
    engine = RapidLayout()
    boxes, scores, class_names, *elapse = engine(img_content)
    assert len(boxes) == 15


@pytest.mark.parametrize(
    "img_content", [img_path, str(img_path), open(img_path, "rb").read(), img]
)
def test_yolov8_layout(img_content):
    engine = RapidLayout(model_type="yolov8n_layout_paper")
    boxes, scores, class_names, *elapse = engine(img_content)
    assert len(boxes) == 11


def test_iou_outside_thres():
    with pytest.raises(ValueError) as exc:
        engine = RapidLayout(iou_thres=1.2)
    assert exc.type is ValueError


def test_conf_outside_thres():
    with pytest.raises(ValueError) as exc:
        engine = RapidLayout(conf_thres=1.2)
    assert exc.type is ValueError


def test_empty():
    with pytest.raises(LoadImageError) as exc:
        engine = RapidLayout()
        engine(None)
    assert exc.type is LoadImageError
