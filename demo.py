# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import cv2

from rapid_layout import RapidLayout, VisLayout

layout_engine = RapidLayout(model_type="doclayout_yolo", conf_thres=0.1)

img_path = "tests/test_files/PMC3576793_00004.jpg"
img = cv2.imread(img_path)

boxes, scores, class_names, elapse = layout_engine(img)
ploted_img = VisLayout.draw_detections(img, boxes, scores, class_names)
if ploted_img is not None:
    cv2.imwrite("layout_res.png", ploted_img)
