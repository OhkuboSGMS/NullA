from pathlib import Path
from typing import Union

import cv2
import numpy as np
from mediapipe.python.solutions.drawing_utils import _normalized_to_pixel_coordinates

from ml.mediapipe.face_detection import MPFaceDetection

__all__ = ['MPFaceCover']


class MPFaceCover(MPFaceDetection):
    def __init__(self, face_image: Union[str, Path]):
        super(MPFaceCover, self).__init__()
        self.face = cv2.imread(str(face_image))

    @classmethod
    def draw(cls, image: np.ndarray, results, *args, **kwargs):
        h, w, _ = image.shape

        if results.detections:
            for detection in results.detections:
                location = detection.location_data
                if location.relative_keypoints:
                    keypoint = location.relative_keypoints[2]
                    keypoint_px = _normalized_to_pixel_coordinates(keypoint.x, keypoint.y, w, h)
                    # TODO kivyでImageを重ねたい!
                    # https://github.com/mvasilkov/kb/blob/master/7_KivyBird/kivybird.kv
                    cv2.circle(image, keypoint_px, 150, (255, 255, 255), -1)

        return image
