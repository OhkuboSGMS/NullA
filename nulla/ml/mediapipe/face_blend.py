import cv2
import numpy as np
from cv2_resize import resize
from mediapipe.python.solutions.drawing_utils import _normalized_to_pixel_coordinates

from nulla.ml.mediapipe.face_detection import MPFaceDetection


class FaceBlend(MPFaceDetection):
    def __init__(self, src_face: str):
        super(FaceBlend, self).__init__()
        self.src_face = cv2.imread(src_face)
        # self.src_face = resize.resize_with_aspect(cv2.imread(src_face),width=300)
        self.src_det = self.face_det.process(self.src_face)
        self.src_mask = np.zeros(self.src_face.shape, self.src_face.dtype)
        img_h, img_w = self.src_face.shape[:2]
        bbox = self.src_det.detections[0].location_data.relative_bounding_box
        bbox = [_normalized_to_pixel_coordinates(bbox.xmin, bbox.ymin, img_w, img_h),
                _normalized_to_pixel_coordinates(bbox.width, bbox.height, img_w, img_h)]
        x, y, w, h = [bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1]]
        xy_bbox = np.array([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], np.int)
        # cv2.fillPoly(self.src_mask, [xy_bbox], colors.white)
        self.src_face = self.src_face[y:y + h, x:x + w, :]
        self.src_mask = 255 * np.ones(self.src_face.shape, self.src_face.dtype)
        # cv2.imshow('test src', self.src_face)
        # cv2.waitKey(-1)

    def __call__(self, image, *args, **kwargs):
        return super(FaceBlend, self).__call__(image)

    def draw(self, image: np.ndarray, result, *args, **kwargs):
        img_h, img_w = image.shape[:2]
        bbox = result.detections[0].location_data.relative_bounding_box
        bbox = [_normalized_to_pixel_coordinates(bbox.xmin, bbox.ymin, img_w, img_h),
                _normalized_to_pixel_coordinates(bbox.width, bbox.height, img_w, img_h)]
        x, y, w, h = [bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1]]
        src = resize.resize_with_aspect(self.src_face, width=w, height=h)
        mask = 255 * np.ones(src.shape, src.dtype)
        # draw_detection(image, result.detections[0])
        # cv2.imshow('', image)
        # cv2.waitKey(-1)
        kp_px = [_normalized_to_pixel_coordinates(keypoint.x, keypoint.y, img_w, img_h) for keypoint in
                 result.detections[0].location_data.relative_keypoints]
        nose = kp_px[2]
        center = nose[0], nose[1]
        output = cv2.seamlessClone(src, image, mask, center, cv2.NORMAL_CLONE)

        return output

    def close(self):
        super(FaceBlend, self).close()

    @classmethod
    def help(cls) -> str:
        return 'Blend 2 Face'

    @property
    def name(self) -> str:
        return 'MPFaceBlend'

