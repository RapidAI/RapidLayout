import traceback
from pathlib import Path
from typing import Any, Dict, List

import numpy as np

try:
    import openvino as ov
except ImportError:
    raise ImportError(
        "openvino is not installed. Please install it with: pip install openvino"
    )

from omegaconf import DictConfig

from ...model_handler.utils import ModelProcessor
from ...utils.logger import Logger
from ...utils.typings import RapidLayoutInput
from ..base import InferSession


class OpenVINOInferSession(InferSession):
    def __init__(self, cfg: RapidLayoutInput):
        self.logger = Logger(logger_name=__name__).get_log()

        if cfg.model_dir_or_path is None:
            model_path = ModelProcessor.get_model_path(cfg.model_type)
        else:
            model_path = Path(cfg.model_dir_or_path)

        self._verify_model(model_path)
        self.logger.info(f"Using {model_path}")

        engine_cfg = self.update_params(
            self.engine_cfg[cfg.engine_type.value], cfg.engine_cfg
        )
        core = ov.Core()

        self.model = core.read_model(model=str(model_path))
        self.input_tensor = self.model.inputs[0]
        self.output_tensors = self.model.outputs

        device = engine_cfg.get('device', 'CPU')
        ov_config = self._init_config(engine_cfg)
        self.compiled_model = core.compile_model(
            self.model,
            device,
            ov_config,
        )
        self.infer_request = self.compiled_model.create_infer_request()

    def _init_config(self, cfg: DictConfig) -> Dict[str, str]:
        config = {}
        engine_cfg = cfg.get("engine_cfg", {})

        def _set(k, v, *, cast=str):
            if v is not None and v != -1:
                config[k] = cast(v)

        _set("INFERENCE_NUM_THREADS",
             engine_cfg.get("inference_num_threads", -1),
             cast=lambda x: str(min(x, os.cpu_count())) if x > 0 else None)

        _set("PERFORMANCE_HINT",
             engine_cfg.get("performance_hint"))
        _set("PERFORMANCE_HINT_NUM_REQUESTS",
             engine_cfg.get("performance_num_requests"))
        _set("ENABLE_CPU_PINNING",
             engine_cfg.get("enable_cpu_pinning"))
        _set("NUM_STREAMS",
             engine_cfg.get("num_streams"))
        _set("ENABLE_HYPER_THREADING",
             engine_cfg.get("enable_hyper_threading"))
        _set("SCHEDULING_CORE_TYPE",
             engine_cfg.get("scheduling_core_type"))

        if config:
            self.logger.info("OpenVINO runtime config: %s", config)
        return config

    def __call__(self, input_content: np.ndarray) -> Any:
        try:
            input_tensor_name = self.input_tensor.get_any_name()
            self.infer_request.set_tensor(input_tensor_name, ov.Tensor(input_content))
            self.infer_request.infer()

            outputs = []
            for output_tensor in self.output_tensors:
                output_tensor_name = output_tensor.get_any_name()
                output = self.infer_request.get_tensor(output_tensor_name).data
                outputs.append(output)

            return outputs

        except Exception as e:
            error_info = traceback.format_exc()
            raise OpenVINOError(error_info) from e

    def get_input_names(self) -> List[str]:
        return [tensor.get_any_name() for tensor in self.model.inputs]

    def get_output_names(self) -> List[str]:
        return [tensor.get_any_name() for tensor in self.model.outputs]

    @property
    def characters(self):
        return self.get_character_list()

    def get_character_list(self, key: str = "character") -> List[str]:
        val = self.model.get_rt_info()["framework"][key]
        return val.value.splitlines()

    def have_key(self, key: str = "character") -> bool:
        try:
            rt_info = self.model.get_rt_info()
            return key in rt_info
        except:
            return False


class OpenVINOError(Exception):
    pass
