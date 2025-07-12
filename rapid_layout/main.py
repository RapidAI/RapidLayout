# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse
from pathlib import Path
from typing import List, Optional, Union

import numpy as np

from .inference_engine.base import get_engine
from .model_handler import ModelHandler, ModelProcessor
from .utils.load_image import LoadImage
from .utils.typings import ModelType, RapidLayoutInput, RapidLayoutOutput
from .utils.utils import is_url


class RapidLayout:
    def __init__(self, cfg: Optional[RapidLayoutInput] = None):
        if cfg is None:
            cfg = RapidLayoutInput()

        if not cfg.model_dir_or_path:
            cfg.model_dir_or_path = ModelProcessor.get_model_path(cfg.model_type)

        self.session = get_engine(cfg.engine_type)(cfg)
        self.model_handler = ModelHandler(cfg, self.session)

        self.load_img = LoadImage()

    def __call__(
        self, img_content: Union[str, np.ndarray, bytes, Path]
    ) -> RapidLayoutOutput:
        img = self.load_img(img_content)
        result = self.model_handler(img)
        return result


def parse_args(arg_list: Optional[List[str]] = None):
    parser = argparse.ArgumentParser()
    parser.add_argument("img_path", type=str, help="Path to image for layout.")
    parser.add_argument(
        "-m",
        "--model_type",
        type=str,
        default=ModelType.PP_LAYOUT_CDLA.value,
        choices=[v.value for v in ModelType],
        help="Support model type",
    )
    parser.add_argument(
        "--conf_thresh",
        type=float,
        default=0.5,
        help="Box threshold, the range is [0, 1]",
    )
    parser.add_argument(
        "--iou_thresh",
        type=float,
        default=0.5,
        help="IoU threshold, the range is [0, 1]",
    )
    parser.add_argument(
        "-v",
        "--vis",
        action="store_true",
        help="Wheter to visualize the layout results.",
    )
    args = parser.parse_args(arg_list)
    return args


def main(arg_list: Optional[List[str]] = None):
    args = parse_args(arg_list)

    input_args = RapidLayoutInput(
        model_type=ModelType(args.model_type),
        iou_thresh=args.iou_thresh,
        conf_thresh=args.conf_thresh,
    )
    layout_engine = RapidLayout(input_args)

    results = layout_engine(args.img_path)
    print(results)

    if args.vis:
        save_path = "layout_vis.jpg"
        if not is_url(args.img_path):
            save_path = args.img_path.resolve().parent / "layout_vis.jpg"
        results.vis(save_path)


if __name__ == "__main__":
    main()
