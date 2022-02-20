from kivy.clock import mainthread
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

from logic.cv2_to_kivy import cv2_to_kivy


class Monitor(BoxLayout):
    def on_kv_post(self, base_widget):
        self.image: Image = self.ids.preview

    @mainthread
    def update(self, img):
        self.image.texture = cv2_to_kivy(img)
