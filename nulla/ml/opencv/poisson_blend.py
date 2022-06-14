import cv2
import numpy as np

from nulla.ml.base import MLBase
from cv2_resize import resize

class PoissonBlend(MLBase):
    def __init__(self, src):
        self.type = cv2.NORMAL_CLONE
        self.obj = resize.resize_with_aspect(cv2.imread(src),width=120)

    def __call__(self, image, *args, **kwargs):
        pass

    def draw(self, image: np.ndarray, *args, **kwargs):
        mask = 255 * np.ones(self.obj.shape, self.obj.dtype)
        center = image.shape[1] // 2, image.shape[0] // 2
        return cv2.seamlessClone(self.obj, image, mask, center, self.type)

    def close(self):
        pass
