from typing import Tuple, Optional

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.python.solutions.drawing_utils import _normalized_to_pixel_coordinates

from nulla.ml.base import MLBase
from nulla.typer import Frame, Point

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils


class MPFaceDetection(MLBase):

    def __init__(self, **kwargs):
        super(MPFaceDetection, self).__init__()
        self.face_det = mp_face_detection.FaceDetection()

    def __call__(self, frame: Frame):
        frame.flags.writeable = False
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_det.process(image)
        # Draw the face detection annotations on the image.
        image.flags.writeable = True
        return results

    def draw(self, image: np.ndarray, results, *args, **kwargs):
        if results.detections:
            for detection in results.detections:
                mp_drawing.draw_detection(image, detection)
        return image

    def close(self):
        self.face_det.close()

    @classmethod
    def help(cls) -> str:
        return 'Detect Face From Single Image. Mediapipe'

    @property
    def name(self) -> str:
        return 'MPFaceDetection'

    @classmethod
    def crop_face(cls, image: Frame, detect_result) -> Tuple[Optional[Point], Optional[Point]]:
        h, w, _ = image.shape
        if detect_result.detections is None or len(detect_result.detections) == 0:
            return None, None
        detection = detect_result.detections[0]
        location = detection.location_data
        relative_bounding_box = location.relative_bounding_box
        lt = _normalized_to_pixel_coordinates(
            relative_bounding_box.xmin, relative_bounding_box.ymin, w,
            h)
        rb = _normalized_to_pixel_coordinates(
            relative_bounding_box.xmin + relative_bounding_box.width,
            relative_bounding_box.ymin + relative_bounding_box.height, w,
            h)
        if not lt or not rb:
            return None, None
        return lt, rb
