# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import shlex
import sys
from pathlib import Path
from typing import Optional

import pytest

cur_dir = Path(__file__).resolve().parent
root_dir = cur_dir.parent

sys.path.append(str(root_dir))

from rapid_layout import ModelType, RapidLayout, RapidLayoutInput
from rapid_layout.main import main

test_dir = cur_dir / "test_files"


def get_engine(params: Optional[RapidLayoutInput] = None):
    if params:
        engine = RapidLayout(cfg=params)
        return engine

    engine = RapidLayout()
    return engine


@pytest.mark.parametrize(
    "img_name,model_type,gt",
    [
        ("layout.jpg", "pp_layout_cdla", 14),
        ("PMC3576793_00004.jpg", "yolov8n_layout_publaynet", 12),
        ("PMC3576793_00004.jpg", "yolov8n_layout_general6", 13),
        ("PMC3576793_00004.jpg", "doclayout_docstructbench", 14),
    ],
)
def test_normal(img_name, model_type, gt):
    img_path = test_dir / img_name
    engine = get_engine(params=RapidLayoutInput(model_type=ModelType(model_type)))
    results = engine(img_path)

    assert results.boxes is not None
    assert len(results.boxes) == gt


@pytest.mark.parametrize(
    "command, expected_output",
    [
        (f"{test_dir / 'layout.jpg'} --model_type pp_layout_cdla", 0),
    ],
)
def test_main_cli(capsys, command, expected_output):
    main(shlex.split(command))
    output = capsys.readouterr().out.rstrip()
    assert len(output) > expected_output
