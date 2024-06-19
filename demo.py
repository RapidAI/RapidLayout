# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import cv2

from rapid_layout import RapidLayout, VisLayout

layout_engine = RapidLayout(box_threshold=0.5, model_type="pp_layout_cdla")

img_path = "tests/test_files/layout.png"
img = cv2.imread(img_path)

boxes, scores, class_names, *elapse = layout_engine(img)
ploted_img = VisLayout.draw_detections(img, boxes, scores, class_names)
if ploted_img is not None:
    cv2.imwrite("layout_res.png", ploted_img)
