from typing import Tuple, Optional

from kivy.clock import mainthread
from kivy.core.text import Label
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout


class MonitorInfo(BoxLayout):
    __kv__loaded__: bool = False

    def __init__(self, **kwargs):
        if not MonitorInfo.__kv__loaded__:
            Builder.load_file('nulla/res/monitor_info.kv')
            MonitorInfo.__kv__loaded__ = True

        self.text: Optional[Label] = None
        super(MonitorInfo, self).__init__(**kwargs)

    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.text = self.ids.text

    @mainthread
    def update(self, data: Tuple):
        if self.text is not None:
            _, fps, source, models = data
            self.text.text = f'Source : {source}\n' \
                             f'FPS : {fps:.2f}\n'
            self.text.text += '\n'.join([f'Model[{i:02d}] : {model}' for i, model in enumerate(models)])
