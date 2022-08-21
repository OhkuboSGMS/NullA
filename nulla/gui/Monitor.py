from kivy.clock import mainthread
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

from nulla.logic.cv2_to_kivy import cv2_to_kivy


class Monitor(BoxLayout):
    __kv__loaded__: bool = False

    def __init__(self, **kwargs):
        if not Monitor.__kv__loaded__:
            Monitor.__kv__loaded__ = True
            Builder.load_file('nulla/res/monitor.kv')

        super(Monitor, self).__init__(**kwargs)

    def on_kv_post(self, base_widget):
        self.image: Image = self.ids.preview

    @mainthread
    def update(self, data):
        img, _, _, _, _ = data
        self.image.texture = cv2_to_kivy(img)
