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

test_file_dir = cur_dir / "test_files"
layout_engine = RapidLayout()

img_path = test_file_dir / "layout.png"

img = cv2.imread(str(img_path))


@pytest.mark.parametrize(
    "img_content", [img_path, str(img_path), open(img_path, "rb").read(), img]
)
def test_multi_input(img_content):
    boxes, scores, class_names, *elapse = layout_engine(img_content)
    assert len(boxes) == 15
