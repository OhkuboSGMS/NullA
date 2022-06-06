from typing import Tuple, Optional

from kivy.clock import mainthread
from kivy.core.text import Label
from kivy.uix.boxlayout import BoxLayout


class MonitorInfo(BoxLayout):

    def __init__(self, *args, **kwargs):
        self.text: Optional[Label] = None
        super(MonitorInfo, self).__init__(*args, **kwargs)

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.text = self.ids.text

    @mainthread
    def update(self, data: Tuple):
        if self.text is not None:
            _, fps, source, model = data
            self.text.text = f'Source : {source}\n' \
                             f'FPS : {fps:.2f}\n' \
                             f'Model : {model}'
