import cv2
import mediapipe as mp
import numpy as np

from nulla.ml.base import MLBase

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

__all__ = ['MPPose']


# BG_COLOR = (192, 192, 192)  # gray
#
#         if not results.pose_landmarks:
#             continue
#         print(
#             f'Nose coordinates: ('
#             f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * image_width}, '
#             f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_height})'
#         )
#
#         annotated_image = image.copy()
#         # Draw segmentation on the image.
#         # To improve segmentation around boundaries, consider applying a joint
#         # bilateral filter to "results.segmentation_mask" with "image".
#         condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
#         bg_image = np.zeros(image.shape, dtype=np.uint8)
#         bg_image[:] = BG_COLOR
#         annotated_image = np.where(condition, annotated_image, bg_image)
#         # Draw pose landmarks on the image.
#         mp_drawing.draw_landmarks(
#             annotated_image,
#             results.pose_landmarks,
#             mp_pose.POSE_CONNECTIONS,
#             landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
#         cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)
#         # Plot pose world landmarks.
#         mp_drawing.plot_landmarks(
#             results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)


class MPPose(MLBase):
    def __init__(self):
        super(MPPose, self).__init__()
        self.pose = mp_pose.Pose(min_detection_confidence=0.5,
                                 min_tracking_confidence=0.5,
                                 static_image_mode=False,
                                 model_complexity=0)

    def __call__(self, frame):
        frame.flags.writeable = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame)
        frame.flags.writeable = True
        return results

    def draw(self, image: np.ndarray, results, *args, **kwargs):
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        return image

    def close(self):
        self.pose.close()

    @classmethod
    def help(self) -> str:
        return 'Estimate Human Pose From Single Image'

    @property
    def name(self) -> str:
        return 'MPPose'
