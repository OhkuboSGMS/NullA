import cv2
import mediapipe as mp
import numpy as np

from nulla.ml.base import MLBase

mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation

BG_COLOR = (192, 192, 192)  # gray

__all__ = ["MPSelfieSegmentation"]


class MPSelfieSegmentation(MLBase):
    def __init__(self, **kwargs):
        super(MPSelfieSegmentation, self).__init__()
        self.model = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

    def __call__(self, frame):
        frame.flags.writeable = False
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.model.process(image)
        image.flags.writeable = True
        return results

    def draw(self, image: np.ndarray, results, *args, **kwargs):
        condition = np.stack(
            (results.segmentation_mask,) * 3, axis=-1) > 0.1
        # bg_image = cv2.GaussianBlur(image, (55, 55), 0)
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = BG_COLOR
        output_image = np.where(condition, image, bg_image)
        return output_image

    def close(self):
        self.model.close()
