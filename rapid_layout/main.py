# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse
import time
from pathlib import Path
from typing import Optional, Tuple, Union

import cv2
import numpy as np

from .utils import (
    DocLayoutPostProcess,
    DocLayoutPreProcess,
    DownloadModel,
    LoadImage,
    OrtInferSession,
    PPPostProcess,
    PPPreProcess,
    VisLayout,
    YOLOv8PostProcess,
    YOLOv8PreProcess,
    get_logger,
)

ROOT_DIR = Path(__file__).resolve().parent
logger = get_logger("rapid_layout")

ROOT_URL = "https://github.com/RapidAI/RapidLayout/releases/download/v0.0.0/"
KEY_TO_MODEL_URL = {
    "pp_layout_cdla": f"{ROOT_URL}/layout_cdla.onnx",
    "pp_layout_publaynet": f"{ROOT_URL}/layout_publaynet.onnx",
    "pp_layout_table": f"{ROOT_URL}/layout_table.onnx",
    "yolov8n_layout_paper": f"{ROOT_URL}/yolov8n_layout_paper.onnx",
    "yolov8n_layout_report": f"{ROOT_URL}/yolov8n_layout_report.onnx",
    "yolov8n_layout_publaynet": f"{ROOT_URL}/yolov8n_layout_publaynet.onnx",
    "yolov8n_layout_general6": f"{ROOT_URL}/yolov8n_layout_general6.onnx",
    "doclayout_docstructbench": f"{ROOT_URL}/doclayout_yolo_docstructbench_imgsz1024.onnx",
    "doclayout_d4la": f"{ROOT_URL}/doclayout_yolo_d4la_imgsz1600_docsynth_pretrain.onnx",
    "doclayout_docsynth": f"{ROOT_URL}/doclayout_yolo_doclaynet_imgsz1120_docsynth_pretrain.onnx",
}
DEFAULT_MODEL_PATH = str(ROOT_DIR / "models" / "layout_cdla.onnx")


class RapidLayout:
    def __init__(
        self,
        model_type: str = "pp_layout_cdla",
        model_path: Union[str, Path, None] = None,
        conf_thres: float = 0.5,
        iou_thres: float = 0.5,
        use_cuda: bool = False,
        use_dml: bool = False,
    ):
        if not self.check_of(conf_thres):
            raise ValueError(f"conf_thres {conf_thres} is outside of range [0, 1]")

        if not self.check_of(iou_thres):
            raise ValueError(f"iou_thres {conf_thres} is outside of range [0, 1]")

        self.model_type = model_type
        config = {
            "model_path": self.get_model_path(model_type, model_path),
            "use_cuda": use_cuda,
            "use_dml": use_dml,
        }
        self.session = OrtInferSession(config)
        labels = self.session.get_character_list()
        logger.info("%s contains %s", model_type, labels)

        # pp
        self.pp_preprocess = PPPreProcess(img_size=(800, 608))
        self.pp_postprocess = PPPostProcess(labels, conf_thres, iou_thres)

        # yolov8
        self.yolov8_input_shape = (640, 640)
        self.yolov8_preprocess = YOLOv8PreProcess(img_size=self.yolov8_input_shape)
        self.yolov8_postprocess = YOLOv8PostProcess(labels, conf_thres, iou_thres)

        # doclayout
        self.doclayout_input_shape = (1024, 1024)
        self.doclayout_preprocess = DocLayoutPreProcess(
            img_size=self.doclayout_input_shape
        )
        self.doclayout_postprocess = DocLayoutPostProcess(labels, conf_thres, iou_thres)

        self.load_img = LoadImage()

        self.pp_layout_type = [k for k in KEY_TO_MODEL_URL if k.startswith("pp")]
        self.yolov8_layout_type = [
            k for k in KEY_TO_MODEL_URL if k.startswith("yolov8n")
        ]
        self.doclayout_type = [k for k in KEY_TO_MODEL_URL if k.startswith("doclayout")]

    def __call__(
        self, img_content: Union[str, np.ndarray, bytes, Path]
    ) -> Tuple[Optional[np.ndarray], Optional[np.ndarray], Optional[np.ndarray], float]:
        img = self.load_img(img_content)
        ori_img_shape = img.shape[:2]

        if self.model_type in self.pp_layout_type:
            return self.pp_layout(img, ori_img_shape)

        if self.model_type in self.yolov8_layout_type:
            return self.yolov8_layout(img, ori_img_shape)

        if self.model_type in self.doclayout_type:
            return self.doclayout_layout(img, ori_img_shape)

        raise ValueError(f"{self.model_type} is not supported.")

    def pp_layout(self, img: np.ndarray, ori_img_shape: Tuple[int, int]):
        s_time = time.time()

        img = self.pp_preprocess(img)
        preds = self.session(img)
        boxes, scores, class_names = self.pp_postprocess(ori_img_shape, img, preds)

        elapse = time.time() - s_time
        return boxes, scores, class_names, elapse

    def yolov8_layout(self, img: np.ndarray, ori_img_shape: Tuple[int, int]):
        s_time = time.time()

        input_tensor = self.yolov8_preprocess(img)
        outputs = self.session(input_tensor)
        boxes, scores, class_names = self.yolov8_postprocess(
            outputs, ori_img_shape, self.yolov8_input_shape
        )
        elapse = time.time() - s_time
        return boxes, scores, class_names, elapse

    def doclayout_layout(self, img: np.ndarray, ori_img_shape: Tuple[int, int]):
        s_time = time.time()

        input_tensor = self.doclayout_preprocess(img)
        outputs = self.session(input_tensor)
        boxes, scores, class_names = self.doclayout_postprocess(
            outputs, ori_img_shape, self.doclayout_input_shape
        )
        elapse = time.time() - s_time
        return boxes, scores, class_names, elapse

    @staticmethod
    def get_model_path(model_type: str, model_path: Union[str, Path, None]) -> str:
        if model_path is not None:
            return model_path

        model_url = KEY_TO_MODEL_URL.get(model_type, None)
        if model_url:
            model_path = DownloadModel.download(model_url)
            return model_path

        logger.info("model url is None, using the default model %s", DEFAULT_MODEL_PATH)
        return DEFAULT_MODEL_PATH

    @staticmethod
    def check_of(thres: float) -> bool:
        if 0 <= thres <= 1.0:
            return True
        return False


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
        "--conf_thres",
        type=float,
        default=0.5,
        choices=list(KEY_TO_MODEL_URL.keys()),
        help="Box threshold, the range is [0, 1]",
    )
    parser.add_argument(
        "--iou_thres",
        type=float,
        default=0.5,
        choices=list(KEY_TO_MODEL_URL.keys()),
        help="IoU threshold, the range is [0, 1]",
    )
    parser.add_argument("--use_cuda", action="store_true", help="Whether to use cuda.")
    parser.add_argument(
        "--use_dml",
        action="store_true",
        help="Whether to use DirectML, which only works in Windows10+.",
    )
    parser.add_argument(
        "-v",
        "--vis",
        action="store_true",
        help="Wheter to visualize the layout results.",
    )
    args = parser.parse_args()

    layout_engine = RapidLayout(
        model_type=args.model_type, conf_thres=args.conf_thres, iou_thres=args.iou_thres
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
