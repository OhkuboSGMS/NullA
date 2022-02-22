from kivy.app import App

from gui.Monitor import Monitor
from logic.backend import Backend


class MonitorApp(App):
    def __init__(self, backend: Backend):
        super(MonitorApp, self).__init__()
        self.backend = backend
        self.monitor = Monitor()
        # TODO Interface
        self.backend.on_update.subscribe(self.monitor.update)

    def build(self):
        return self.monitor
