# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import argparse
import time
from pathlib import Path
from typing import Optional, Tuple, Union

import cv2
import numpy as np

from .utils import (
    DownloadModel,
    LoadImage,
    OrtInferSession,
    PicoDetPostProcess,
    VisLayout,
    create_operators,
    get_logger,
    read_yaml,
    transform,
)

ROOT_DIR = Path(__file__).resolve().parent
logger = get_logger("rapid_layout")

ROOT_URL = "https://github.com/RapidAI/RapidStructure/releases/download/v0.0.0/"
KEY_TO_MODEL_URL = {
    "pp_layout_cdla": f"{ROOT_URL}/layout_cdla.onnx",
    "pp_layout_publaynet": f"{ROOT_URL}/layout_publaynet.onnx",
    "pp_layout_table": f"{ROOT_URL}/layout_table.onnx",
}
DEFAULT_MODEL_PATH = str(ROOT_DIR / "models" / "layout_cdla.onnx")


class RapidLayout:
    def __init__(
        self,
        model_type: str = "pp_layout_cdla",
        box_threshold: float = 0.5,
        use_cuda: bool = False,
    ):
        config_path = str(ROOT_DIR / "config.yaml")
        config = read_yaml(config_path)
        config["model_path"] = self.get_model_path(model_type)
        config["use_cuda"] = use_cuda

        self.session = OrtInferSession(config)
        labels = self.session.get_character_list()
        logger.info("%s contains %s", model_type, labels)

        self.preprocess_op = create_operators(config["pre_process"])

        config["post_process"]["score_threshold"] = box_threshold
        self.postprocess_op = PicoDetPostProcess(labels, **config["post_process"])
        self.load_img = LoadImage()

    def __call__(
        self, img_content: Union[str, np.ndarray, bytes, Path]
    ) -> Tuple[Optional[np.ndarray], Optional[np.ndarray], Optional[np.ndarray], float]:
        img = self.load_img(img_content)

        ori_im = img.copy()
        data = transform({"image": img}, self.preprocess_op)
        img = data[0]
        if img is None:
            return None, None, None, 0.0

        img = np.expand_dims(img, axis=0)
        img = img.copy()

        preds, elapse = 0, 1
        starttime = time.time()
        preds = self.session(img)

        score_list, boxes_list = [], []
        num_outs = int(len(preds) / 2)
        for out_idx in range(num_outs):
            score_list.append(preds[out_idx])
            boxes_list.append(preds[out_idx + num_outs])

        boxes, scores, class_names = self.postprocess_op(
            ori_im, img, {"boxes": score_list, "boxes_num": boxes_list}
        )
        elapse = time.time() - starttime
        return boxes, scores, class_names, elapse

    @staticmethod
    def get_model_path(model_type: str) -> str:
        model_url = KEY_TO_MODEL_URL.get(model_type, None)
        if model_url:
            model_path = DownloadModel.download(model_url)
            return model_path

        logger.info("model url is None, using the default model %s", DEFAULT_MODEL_PATH)
        return DEFAULT_MODEL_PATH


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-img", "--img_path", type=str, required=True, help="Path to image for layout."
    )
    parser.add_argument(
        "-m",
        "--model_type",
        type=str,
        default=DEFAULT_MODEL_PATH,
        choices=list(KEY_TO_MODEL_URL.keys()),
        help="Support model type",
    )
    parser.add_argument(
        "--box_threshold",
        type=float,
        default=0.5,
        choices=list(KEY_TO_MODEL_URL.keys()),
        help="Box threshold, the range is [0, 1]",
    )
    parser.add_argument(
        "-v",
        "--vis",
        action="store_true",
        help="Wheter to visualize the layout results.",
    )
    args = parser.parse_args()

    layout_engine = RapidLayout(
        model_type=args.model_type, box_threshold=args.box_threshold
    )

    img = cv2.imread(args.img_path)
    boxes, scores, class_names, *elapse = layout_engine(img)
    print(boxes)
    print(scores)
    print(class_names)

    if args.vis:
        img_path = Path(args.img_path)
        ploted_img = VisLayout.draw_detections(img, boxes, scores, class_names)
        if ploted_img is not None:
            save_path = img_path.resolve().parent / f"vis_{img_path.name}"
            cv2.imwrite(str(save_path), ploted_img)
            print(f"The visualized image has been saved in {save_path}")


if __name__ == "__main__":
    main()
