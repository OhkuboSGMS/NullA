from typing import Optional

import cv2
import numpy as np


class Player:

    def __init__(self, src: str):
        self.capture = cv2.VideoCapture(src)

    def next(self) -> Optional[np.ndarray]:
        ret, frame = self.capture.read()
        if ret:
            return frame
        else:
            return None
