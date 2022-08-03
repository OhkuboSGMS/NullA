from typing import Any

import cv2
import mediapipe as mp
import numpy as np

from nulla.ml.base import MLBase

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


class MPHandTracking(MLBase):
    def __init__(self, **kwargs):
        self.hand = mp_hands.Hands(model_complexity=0,
                                   min_detection_confidence=0.5,
                                   min_tracking_confidence=0.5)

    def __call__(self, frame, *args, **kwargs):
        frame.flags.writeable = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hand.process(frame)
        frame.flags.writeable = True
        return results

    def draw(self, image: np.ndarray, results: Any, *args, **kwargs):
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        return image

    def close(self):
        self.hand.close()

    @property
    def name(self) -> str:
        return 'MPHandTracking'

    @classmethod
    def help(self) -> str:
        return 'Estimate Hand KeyPoint From Single Image'
