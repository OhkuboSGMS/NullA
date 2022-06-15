from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout


class EmptyMonitor(BoxLayout):
    __kv_loaded__: bool = False

    def __init__(self, **kwargs):
        if not EmptyMonitor.__kv_loaded__:
            Builder.load_file('nulla/res/empty_monitor.kv')
            EmptyMonitor.__kv_loaded__ = True
        super(EmptyMonitor, self).__init__(**kwargs)
