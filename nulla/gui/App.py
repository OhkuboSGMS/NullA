from kivy.app import App
from kivy.clock import Clock

from gui.Root import Root
from nulla.gui.Monitor import Monitor
from nulla.logic.backend import Backend
from nulla.gui.KivyWidgetAPI import set_instance, KivyWidgetAPI


class MonitorApp(App):
    def __init__(self, backend: Backend):
        super(MonitorApp, self).__init__()
        self.backend = backend
        self.root = Root()
        set_instance(self.root)
        self.monitor = self.root.ids.monitor
        # TODO Interface
        self.backend.on_update.subscribe(self.monitor.update)

    def build(self):
        return self.root
