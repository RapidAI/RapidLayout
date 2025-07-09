# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import os
import traceback
from pathlib import Path

import numpy as np
from omegaconf import DictConfig
from openvino.runtime import Core

from ..utils.download_file import DownloadFile, DownloadFileInput
from ..utils.logger import Logger
from .base import InferSession


class OpenVINOInferSession(InferSession):
    def __init__(self, cfg: DictConfig):
        super().__init__(cfg)
        self.logger = Logger(logger_name=__name__).get_log()

        core = Core()

        model_path = cfg.get("model_dir_or_path", None)
        self.logger.info(f"Using {model_path}")
        model_path = Path(model_path)
        self._verify_model(model_path)

        engine_cfg = self.update_params(
            self.engine_cfg[cfg["engine_type"].value], cfg["engine_cfg"]
        )

        cpu_nums = os.cpu_count()
        infer_num_threads = engine_cfg.get("inference_num_threads", -1)
        if infer_num_threads != -1 and 1 <= infer_num_threads <= cpu_nums:
            core.set_property("CPU", {"INFERENCE_NUM_THREADS": str(infer_num_threads)})

        model_onnx = core.read_model(model_path)
        compile_model = core.compile_model(model=model_onnx, device_name="CPU")
        self.session = compile_model.create_infer_request()

    def __call__(self, input_content: np.ndarray) -> np.ndarray:
        try:
            self.session.infer(inputs=[input_content])
            return self.session.get_output_tensor().data
        except Exception as e:
            error_info = traceback.format_exc()
            raise OpenVIONError(error_info) from e

    def have_key(self, key: str = "character") -> bool:
        return False


class OpenVIONError(Exception):
    pass
