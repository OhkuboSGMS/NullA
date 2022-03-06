from pathlib import Path
from typing import Union

import mediapipe as mp
import numpy as np
from kivy.app import App
from kivy.clock import Clock
from kivy.core.image import Image
from kivy.graphics import Rectangle
from kivy.properties import ListProperty
from kivy.uix.widget import Widget
from mediapipe.python.solutions.drawing_utils import _normalized_to_pixel_coordinates

from ml.mediapipe.face_detection import MPFaceDetection
from nulla.gui import add_widget

mp_drawing = mp.solutions.drawing_utils

__all__ = ['MPFaceCover']


class FaceImage(Widget):
    # TODO 複数人
    tex_coords = ListProperty([-1, 0, 1, 0, 1, 1, 0, 1])

    def __init__(self, texture: str, **kwargs):
        super(FaceImage, self).__init__(**kwargs)
        self.texture = Image(texture).texture
        self.size_hint = (None, None)
        self.bind(pos=self.draw)
        self.bind(size=self.draw)

    def draw(self, *args):
        self.canvas.clear()
        with self.canvas:
            Rectangle(pos=self.pos, size=self.size, texture=self.texture)
            # Rectangle(pos=self.pos, size=self.size, )


class MPFaceCover(MPFaceDetection):
    def __init__(self, face_image: Union[str, Path], scale: float = 1.8):
        super(MPFaceCover, self).__init__()
        self.face = str(face_image)
        self.scale = scale
        self.widget = None
        Clock.schedule_once(self.initialize_widget)

    def initialize_widget(self, ins):
        self.widget = FaceImage(self.face)
        self.widget.size_hint = (None, None)
        add_widget(self.widget)

    def draw(self, image: np.ndarray, results, *args, **kwargs):
        h, w, _ = image.shape
        r_w, r_h = 1, 1
        if self.widget:
            app_w, app_h = App.get_running_app().root.size
            r_w, r_h = app_w / w, app_h / h

        if results.detections:
            for detection in results.detections:
                location = detection.location_data
                if location.relative_keypoints:
                    # 0:左目,1:右目,2:鼻頭,3:口,4:左耳,5:右耳
                    kp_px = [_normalized_to_pixel_coordinates(keypoint.x, keypoint.y, w, h) for keypoint in
                             location.relative_keypoints]
                    kp_px = list(filter(lambda p: p, kp_px))
                    bbox = location.relative_bounding_box
                    bbox = [_normalized_to_pixel_coordinates(bbox.xmin, bbox.ymin, w, h),
                            _normalized_to_pixel_coordinates(bbox.width, bbox.height, w, h)]
                    if len(kp_px) != 6:
                        if self.widget:
                            self.widget.size = (0, 0)
                        continue
                    if len(list(filter(lambda b: b, bbox))) != 2:
                        if self.widget:
                            self.widget.size = (0, 0)
                        continue
                    # 口から鼻の長さ
                    size = bbox[1][0] * self.scale, bbox[1][1] * self.scale
                    inc = bbox[1][0] * (self.scale - 1) / 2, bbox[1][1] * (self.scale - 1) / 2
                    pos = bbox[0][0] - inc[0], h - (bbox[0][1] + size[1] - inc[1])
                    if self.widget:
                        self.widget.size = size[0] * r_w, size[1] * r_h
                        self.widget.pos = pos[0] * r_w, pos[1] * r_h

                    # mp_drawing.draw_detection(image, detection)

        return image
