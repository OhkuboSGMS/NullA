from typing import Optional

import cv2
import numpy as np


class Player:

    def __init__(self, src: str, flip: int = 1):
        """
        :param src: 動画URL
        :param flip: >0 左右　=0上下 <0 上下左右
        """
        self.source = src
        self.flip = flip
        self.capture = cv2.VideoCapture(src)

    def next(self) -> Optional[np.ndarray]:
        ret, frame = self.capture.read()
        if ret:
            if self.flip:
                frame = cv2.flip(frame, self.flip)
            return frame
        else:
            return None

    def close(self):
        if self.capture and self.capture.isOpened():
            self.capture.release()
