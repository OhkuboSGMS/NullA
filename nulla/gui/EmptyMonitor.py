from typing import Callable

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput


class EmptyMonitor(BoxLayout):
    __kv_loaded__: bool = False

    def __init__(self, on_text_input: Callable[[str], None], **kwargs):
        self.on_text_input = on_text_input
        if not EmptyMonitor.__kv_loaded__:
            Builder.load_file('nulla/res/empty_monitor.kv')
            EmptyMonitor.__kv_loaded__ = True
        super(EmptyMonitor, self).__init__(**kwargs)

    def on_kv_post(self, base_widget):
        text_input: TextInput = self.ids.url_input
        text_input.bind(on_text_validate=lambda v: self.on_text_input(v.text))
