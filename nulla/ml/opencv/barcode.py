from typing import Dict

import numpy as np
import cv2
from nulla.ml.base import MLBase

"""
https://docs.opencv.org/4.x/dc/df7/classcv_1_1barcode_1_1BarcodeDetector.html
"""
class Cv2BarcodeDetector(MLBase):

    def __init__(self, **kwargs):
        self.detector = cv2.barcode_BarcodeDetector()

    def __call__(self, image, *args, **kwargs):
        ok, decoded_info, decoded_type, corners = self.detector.detectAndDecode(image)
        return {'is_detect': ok, 'info': decoded_info, 'type': decoded_type, 'point': corners}

    def draw(self, image: np.ndarray, result: Dict, *args, **kwargs):
        corners = result['point']
        imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        contours, h = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if corners is None:
            return image
        corners = np.array(corners, dtype=np.int)
        cv2.drawContours(image, np.array(corners), -1, (255, 0, 0))

        if result['info']:
            for idx, corner in enumerate(corners):
                px, py = int(corner[2][0]), int(corner[2][1])
                cv2.putText(image, result['info'][idx], (px, py), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255),
                            thickness=2)
        return image

    def close(self):
        pass

    @classmethod
    def help(cls) -> str:
        return 'Detect Barcode Code with Opencv Barcode Detector '

    @property
    def name(self) -> str:
        return 'Cv2BarcodeCodeDetector'
