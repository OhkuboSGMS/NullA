import cv2
import mediapipe as mp
import numpy as np

from ml.base import MLBase

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils


class MPFaceDetection(MLBase):

    def __init__(self):
        super(MPFaceDetection, self).__init__()
        self.face_det = mp_face_detection.FaceDetection()

    def __call__(self, frame):
        frame.flags.writeable = False
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_det.process(image)
        # Draw the face detection annotations on the image.
        image.flags.writeable = True
        return results

    @classmethod
    def draw(cls, image: np.ndarray, results, *args, **kwargs):
        if results.detections:
            for detection in results.detections:
                mp_drawing.draw_detection(image, detection)
        return image
