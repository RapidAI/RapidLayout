# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from typing import List, Tuple

import numpy as np


class PPPostProcess:
    def __init__(self, labels, conf_thres=0.4, iou_thres=0.5):
        self.labels = labels
        self.strides = [8, 16, 32, 64]
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.nms_top_k = 1000
        self.keep_top_k = 100

    def __call__(
        self, ori_shape, img: np.ndarray, preds: List[np.ndarray]
    ) -> Tuple[List[List[float]], List[float], List[str]]:
        scores, raw_boxes = [], []
        num_outs = int(len(preds) / 2)
        for out_idx in range(num_outs):
            scores.append(preds[out_idx])
            raw_boxes.append(preds[out_idx + num_outs])

        batch_size = raw_boxes[0].shape[0]
        reg_max = int(raw_boxes[0].shape[-1] / 4 - 1)

        out_boxes_num, out_boxes_list = [], []
        ori_shape, input_shape, scale_factor = self.img_info(ori_shape, img)

        for batch_id in range(batch_size):
            # generate centers
            decode_boxes, select_scores = [], []
            for stride, box_distribute, score in zip(self.strides, raw_boxes, scores):
                box_distribute = box_distribute[batch_id]
                score = score[batch_id]
                # centers
                fm_h = input_shape[0] / stride
                fm_w = input_shape[1] / stride
                h_range = np.arange(fm_h)
                w_range = np.arange(fm_w)
                ww, hh = np.meshgrid(w_range, h_range)
                ct_row = (hh.flatten() + 0.5) * stride
                ct_col = (ww.flatten() + 0.5) * stride
                center = np.stack((ct_col, ct_row, ct_col, ct_row), axis=1)

                # box distribution to distance
                reg_range = np.arange(reg_max + 1)
                box_distance = box_distribute.reshape((-1, reg_max + 1))
                box_distance = self.softmax(box_distance, axis=1)
                box_distance = box_distance * np.expand_dims(reg_range, axis=0)
                box_distance = np.sum(box_distance, axis=1).reshape((-1, 4))
                box_distance = box_distance * stride

                # top K candidate
                topk_idx = np.argsort(score.max(axis=1))[::-1]
                topk_idx = topk_idx[: self.nms_top_k]
                center = center[topk_idx]
                score = score[topk_idx]
                box_distance = box_distance[topk_idx]

                # decode box
                decode_box = center + [-1, -1, 1, 1] * box_distance

                select_scores.append(score)
                decode_boxes.append(decode_box)

            # nms
            bboxes = np.concatenate(decode_boxes, axis=0)
            confidences = np.concatenate(select_scores, axis=0)
            picked_box_probs, picked_labels = [], []
            for class_index in range(0, confidences.shape[1]):
                probs = confidences[:, class_index]
                mask = probs > self.conf_thres
                probs = probs[mask]
                if probs.shape[0] == 0:
                    continue

                subset_boxes = bboxes[mask, :]
                box_probs = np.concatenate([subset_boxes, probs.reshape(-1, 1)], axis=1)
                box_probs = self.hard_nms(
                    box_probs,
                    iou_thres=self.iou_thres,
                    top_k=self.keep_top_k,
                )
                picked_box_probs.append(box_probs)
                picked_labels.extend([class_index] * box_probs.shape[0])

            if len(picked_box_probs) == 0:
                out_boxes_list.append(np.empty((0, 4)))
                out_boxes_num.append(0)
            else:
                picked_box_probs = np.concatenate(picked_box_probs)

                # resize output boxes
                picked_box_probs[:, :4] = self.warp_boxes(
                    picked_box_probs[:, :4], ori_shape[batch_id]
                )
                im_scale = np.concatenate(
                    [scale_factor[batch_id][::-1], scale_factor[batch_id][::-1]]
                )
                picked_box_probs[:, :4] /= im_scale
                # clas score box
                out_boxes_list.append(
                    np.concatenate(
                        [
                            np.expand_dims(np.array(picked_labels), axis=-1),
                            np.expand_dims(picked_box_probs[:, 4], axis=-1),
                            picked_box_probs[:, :4],
                        ],
                        axis=1,
                    )
                )
                out_boxes_num.append(len(picked_labels))

        out_boxes_list = np.concatenate(out_boxes_list, axis=0)
        out_boxes_num = np.asarray(out_boxes_num).astype(np.int32)

        boxes, scores, class_names = [], [], []
        for dt in out_boxes_list:
            clsid, bbox, score = int(dt[0]), dt[2:], dt[1]
            label = self.labels[clsid]
            boxes.append(bbox.tolist())
            scores.append(float(score))
            class_names.append(label)
        return boxes, scores, class_names

    def warp_boxes(self, boxes, ori_shape):
        """Apply transform to boxes"""
        width, height = ori_shape[1], ori_shape[0]
        n = len(boxes)
        if n:
            # warp points
            xy = np.ones((n * 4, 3))
            xy[:, :2] = boxes[:, [0, 1, 2, 3, 0, 3, 2, 1]].reshape(
                n * 4, 2
            )  # x1y1, x2y2, x1y2, x2y1
            # xy = xy @ M.T  # transform
            xy = (xy[:, :2] / xy[:, 2:3]).reshape(n, 8)  # rescale
            # create new boxes
            x = xy[:, [0, 2, 4, 6]]
            y = xy[:, [1, 3, 5, 7]]
            xy = (
                np.concatenate((x.min(1), y.min(1), x.max(1), y.max(1))).reshape(4, n).T
            )
            # clip boxes
            xy[:, [0, 2]] = xy[:, [0, 2]].clip(0, width)
            xy[:, [1, 3]] = xy[:, [1, 3]].clip(0, height)
            return xy.astype(np.float32)
        return boxes

    def img_info(self, origin_shape, img):
        resize_shape = img.shape
        im_scale_y = resize_shape[2] / float(origin_shape[0])
        im_scale_x = resize_shape[3] / float(origin_shape[1])
        scale_factor = np.array([im_scale_y, im_scale_x], dtype=np.float32)
        img_shape = np.array(img.shape[2:], dtype=np.float32)

        input_shape = np.array(img).astype("float32").shape[2:]
        ori_shape = np.array((img_shape,)).astype("float32")
        scale_factor = np.array((scale_factor,)).astype("float32")
        return ori_shape, input_shape, scale_factor

    @staticmethod
    def softmax(x, axis=None):
        def logsumexp(a, axis=None, b=None, keepdims=False):
            a_max = np.amax(a, axis=axis, keepdims=True)

            if a_max.ndim > 0:
                a_max[~np.isfinite(a_max)] = 0
            elif not np.isfinite(a_max):
                a_max = 0

            tmp = np.exp(a - a_max)

            # suppress warnings about log of zero
            with np.errstate(divide="ignore"):
                s = np.sum(tmp, axis=axis, keepdims=keepdims)
                out = np.log(s)

            if not keepdims:
                a_max = np.squeeze(a_max, axis=axis)
            out += a_max
            return out

        return np.exp(x - logsumexp(x, axis=axis, keepdims=True))

    def hard_nms(self, box_scores, iou_thres, top_k=-1, candidate_size=200):
        """
        Args:
            box_scores (N, 5): boxes in corner-form and probabilities.
            iou_thres: intersection over union threshold.
            top_k: keep top_k results. If k <= 0, keep all the results.
            candidate_size: only consider the candidates with the highest scores.
        Returns:
            picked: a list of indexes of the kept boxes
        """
        scores = box_scores[:, -1]
        boxes = box_scores[:, :-1]
        picked = []
        indexes = np.argsort(scores)
        indexes = indexes[-candidate_size:]
        while len(indexes) > 0:
            current = indexes[-1]
            picked.append(current)
            if 0 < top_k == len(picked) or len(indexes) == 1:
                break
            current_box = boxes[current, :]
            indexes = indexes[:-1]
            rest_boxes = boxes[indexes, :]
            iou = self.iou_of(
                rest_boxes,
                np.expand_dims(current_box, axis=0),
            )
            indexes = indexes[iou <= iou_thres]

        return box_scores[picked, :]

    def iou_of(self, boxes0, boxes1, eps=1e-5):
        """Return intersection-over-union (Jaccard index) of boxes.
        Args:
            boxes0 (N, 4): ground truth boxes.
            boxes1 (N or 1, 4): predicted boxes.
            eps: a small number to avoid 0 as denominator.
        Returns:
            iou (N): IoU values.
        """
        overlap_left_top = np.maximum(boxes0[..., :2], boxes1[..., :2])
        overlap_right_bottom = np.minimum(boxes0[..., 2:], boxes1[..., 2:])

        overlap_area = self.area_of(overlap_left_top, overlap_right_bottom)
        area0 = self.area_of(boxes0[..., :2], boxes0[..., 2:])
        area1 = self.area_of(boxes1[..., :2], boxes1[..., 2:])
        return overlap_area / (area0 + area1 - overlap_area + eps)

    @staticmethod
    def area_of(left_top, right_bottom):
        """Compute the areas of rectangles given two corners.
        Args:
            left_top (N, 2): left top corner.
            right_bottom (N, 2): right bottom corner.
        Returns:
            area (N): return the area.
        """
        hw = np.clip(right_bottom - left_top, 0.0, None)
        return hw[..., 0] * hw[..., 1]
