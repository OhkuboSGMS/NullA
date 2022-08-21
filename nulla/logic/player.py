from typing import Optional

import cv2
import numpy as np

NOT_FLIP = 3


class Player:

    def __init__(self, src: str, flip: int = NOT_FLIP):
        """
        :param src: 動画URL
        :param flip: >0 左右　=0上下 <0 上下左右
        """
        self.source = src
        self.flip = flip
        self.capture = cv2.VideoCapture(self.source)

    def next(self) -> Optional[np.ndarray]:
        ret, frame = self.capture.read()
        if ret:
            if self.flip != NOT_FLIP:
                frame = cv2.flip(frame, self.flip)
            return frame
        else:
            self.capture = cv2.VideoCapture(self.source)
            ret, frame = self.capture.read()
            if not ret:
                raise Exception(self.source)
            return frame

    def close(self):
        if self.capture and self.capture.isOpened():
            self.capture.release()
