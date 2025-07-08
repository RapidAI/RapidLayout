# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from dataclasses import dataclass

import numpy as np


@dataclass
class RapidLayoutOutput:
    boxes: np.ndarray
