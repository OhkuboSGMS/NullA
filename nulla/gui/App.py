from typing import Optional

from kivy.app import App
from kivy.clock import mainthread
from loguru import logger

from nulla.gui.EmptyMonitor import EmptyMonitor
from nulla.gui.KivyWidgetAPI import set_instance
from nulla.gui.Root import Root
from nulla.logic.backend import Backend
from nulla.util import int_or_str


class MonitorApp(App):
    _empty_monitor: EmptyMonitor = None

    def __init__(self, backend: Backend):
        super(MonitorApp, self).__init__()
        self.backend = backend
        self.root = Root()
        set_instance(self.root)
        self.monitor = self.root.ids.monitor
        self.info = self.root.ids.info
        self.model_list = self.root.ids.model_list
        # TODO Interface
        self.backend.on_initialize.subscribe(self.initialize)
        self.backend.on_update.subscribe(self.monitor.update)
        self.backend.on_update.subscribe(self.info.update)
        self.backend.on_load_model.subscribe(self.model_list.update)

    @mainthread
    def initialize(self, source: Optional):
        """
        動画ソースが変更されたタイミングで実行.
        ソースの有無に応じて画面を切り替え
        :param source:
        :return:
        """
        logger.debug(f'monitor initialized : {source}')
        if source is not None:
            if self._empty_monitor in self.root.children:
                self.root.remove_widget(self._empty_monitor)
        else:
            self.root.add_widget(self._empty_monitor)

    def select_model(self, model: str) -> None:
        """
        モデルを選択. Call from MLItem
        :param model:
        :return:
        """
        self.backend.set_model(model)

    # TODO Kivy2.1.0現在 APIと引数が異なっている
    def _on_drop_file(self, window, filename: bytes, x: int, y: int, *args):
        # filenameはutf-8
        if filename:
            self.backend.set_resource(str(filename, encoding="utf-8"))

    def _on_url_input(self, url: str) -> None:
        """
        入力欄から動画リソースを入力.
        Backendに設定
        :param url:
        :return:
        """
        if url:
            self.backend.set_resource(int_or_str(url))

    def build(self):
        self.icon = 'assets/icon.ico'
        self._empty_monitor = EmptyMonitor(self._on_url_input)
        from kivy.core.window import Window
        # inspector.create_inspector(Window, self.root)
        Window.bind(on_drop_file=self._on_drop_file)
        Window.size = (1024, 600)
        return self.root
