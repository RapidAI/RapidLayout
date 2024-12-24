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

    def __call__(self, ori_shape, img, preds):
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
            boxes.append(bbox)
            scores.append(score)
            class_names.append(label)
        return np.array(boxes), np.array(scores), np.array(class_names)

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


class YOLOv8PostProcess:
    def __init__(self, labels: List[str], conf_thres=0.7, iou_thres=0.5):
        self.labels = labels
        self.conf_threshold = conf_thres
        self.iou_threshold = iou_thres
        self.input_width, self.input_height = None, None
        self.img_width, self.img_height = None, None

    def __call__(
        self, output, ori_img_shape: Tuple[int, int], img_shape: Tuple[int, int]
    ):
        self.img_height, self.img_width = ori_img_shape
        self.input_height, self.input_width = img_shape

        predictions = np.squeeze(output[0]).T

        # Filter out object confidence scores below threshold
        scores = np.max(predictions[:, 4:], axis=1)
        predictions = predictions[scores > self.conf_threshold, :]
        scores = scores[scores > self.conf_threshold]

        if len(scores) == 0:
            return [], [], []

        # Get the class with the highest confidence
        class_ids = np.argmax(predictions[:, 4:], axis=1)

        # Get bounding boxes for each object
        boxes = self.extract_boxes(predictions)

        # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
        # indices = nms(boxes, scores, self.iou_threshold)
        indices = multiclass_nms(boxes, scores, class_ids, self.iou_threshold)

        labels = [self.labels[i] for i in class_ids[indices]]
        return boxes[indices], scores[indices], labels

    def extract_boxes(self, predictions):
        # Extract boxes from predictions
        boxes = predictions[:, :4]

        # Scale boxes to original image dimensions
        boxes = rescale_boxes(
            boxes, self.input_width, self.input_height, self.img_width, self.img_height
        )

        # Convert boxes to xyxy format
        boxes = xywh2xyxy(boxes)

        return boxes


class DocLayoutPostProcess:
    def __init__(self, labels: List[str], conf_thres=0.2, iou_thres=0.5):
        self.labels = labels
        self.conf_threshold = conf_thres
        self.iou_threshold = iou_thres
        self.input_width, self.input_height = None, None
        self.img_width, self.img_height = None, None

    def __call__(
        self,
        preds,
        ori_img_shape: Tuple[int, int],
        img_shape: Tuple[int, int] = (1024, 1024),
    ):
        preds = preds[0]
        mask = preds[..., 4] > self.conf_threshold
        preds = [p[mask[idx]] for idx, p in enumerate(preds)][0]
        preds[:, :4] = scale_boxes(list(img_shape), preds[:, :4], list(ori_img_shape))

        boxes = preds[:, :4]
        confidences = preds[:, 4]
        class_ids = preds[:, 5].astype(int)
        labels = [self.labels[i] for i in class_ids]
        return boxes, confidences, labels


def rescale_boxes(boxes, input_width, input_height, img_width, img_height):
    # Rescale boxes to original image dimensions
    input_shape = np.array([input_width, input_height, input_width, input_height])
    boxes = np.divide(boxes, input_shape, dtype=np.float32)
    boxes *= np.array([img_width, img_height, img_width, img_height])
    return boxes


def scale_boxes(
    img1_shape, boxes, img0_shape, ratio_pad=None, padding=True, xywh=False
):
    """
    Rescales bounding boxes (in the format of xyxy by default) from the shape of the image they were originally
    specified in (img1_shape) to the shape of a different image (img0_shape).

    Args:
        img1_shape (tuple): The shape of the image that the bounding boxes are for, in the format of (height, width).
        boxes (torch.Tensor): the bounding boxes of the objects in the image, in the format of (x1, y1, x2, y2)
        img0_shape (tuple): the shape of the target image, in the format of (height, width).
        ratio_pad (tuple): a tuple of (ratio, pad) for scaling the boxes. If not provided, the ratio and pad will be
            calculated based on the size difference between the two images.
        padding (bool): If True, assuming the boxes is based on image augmented by yolo style. If False then do regular
            rescaling.
        xywh (bool): The box format is xywh or not, default=False.

    Returns:
        boxes (torch.Tensor): The scaled bounding boxes, in the format of (x1, y1, x2, y2)
    """
    if ratio_pad is None:  # calculate from img0_shape
        gain = min(
            img1_shape[0] / img0_shape[0], img1_shape[1] / img0_shape[1]
        )  # gain  = old / new
        pad = (
            round((img1_shape[1] - img0_shape[1] * gain) / 2 - 0.1),
            round((img1_shape[0] - img0_shape[0] * gain) / 2 - 0.1),
        )  # wh padding
    else:
        gain = ratio_pad[0][0]
        pad = ratio_pad[1]

    if padding:
        boxes[..., 0] -= pad[0]  # x padding
        boxes[..., 1] -= pad[1]  # y padding
        if not xywh:
            boxes[..., 2] -= pad[0]  # x padding
            boxes[..., 3] -= pad[1]  # y padding
    boxes[..., :4] /= gain
    return clip_boxes(boxes, img0_shape)


def clip_boxes(boxes, shape):
    boxes[..., [0, 2]] = boxes[..., [0, 2]].clip(0, shape[1])  # x1, x2
    boxes[..., [1, 3]] = boxes[..., [1, 3]].clip(0, shape[0])  # y1, y2
    return boxes


def nms(boxes, scores, iou_threshold):
    # Sort by score
    sorted_indices = np.argsort(scores)[::-1]

    keep_boxes = []
    while sorted_indices.size > 0:
        # Pick the last box
        box_id = sorted_indices[0]
        keep_boxes.append(box_id)

        # Compute IoU of the picked box with the rest
        ious = compute_iou(boxes[box_id, :], boxes[sorted_indices[1:], :])

        # Remove boxes with IoU over the threshold
        keep_indices = np.where(ious < iou_threshold)[0]

        # print(keep_indices.shape, sorted_indices.shape)
        sorted_indices = sorted_indices[keep_indices + 1]

    return keep_boxes


def multiclass_nms(boxes, scores, class_ids, iou_threshold):
    unique_class_ids = np.unique(class_ids)

    keep_boxes = []
    for class_id in unique_class_ids:
        class_indices = np.where(class_ids == class_id)[0]
        class_boxes = boxes[class_indices, :]
        class_scores = scores[class_indices]

        class_keep_boxes = nms(class_boxes, class_scores, iou_threshold)
        keep_boxes.extend(class_indices[class_keep_boxes])

    return keep_boxes


def compute_iou(box, boxes):
    # Compute xmin, ymin, xmax, ymax for both boxes
    xmin = np.maximum(box[0], boxes[:, 0])
    ymin = np.maximum(box[1], boxes[:, 1])
    xmax = np.minimum(box[2], boxes[:, 2])
    ymax = np.minimum(box[3], boxes[:, 3])

    # Compute intersection area
    intersection_area = np.maximum(0, xmax - xmin) * np.maximum(0, ymax - ymin)

    # Compute union area
    box_area = (box[2] - box[0]) * (box[3] - box[1])
    boxes_area = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
    union_area = box_area + boxes_area - intersection_area

    # Compute IoU
    iou = intersection_area / union_area

    return iou


def xywh2xyxy(x):
    # Convert bounding box (x, y, w, h) to bounding box (x1, y1, x2, y2)
    y = np.copy(x)
    y[..., 0] = x[..., 0] - x[..., 2] / 2
    y[..., 1] = x[..., 1] - x[..., 3] / 2
    y[..., 2] = x[..., 0] + x[..., 2] / 2
    y[..., 3] = x[..., 1] + x[..., 3] / 2
    return y
