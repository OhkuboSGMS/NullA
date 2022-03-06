from threading import Lock
from typing import Optional, List

from kivy.clock import mainthread
from kivy.uix.widget import Widget
from loguru import logger


class KivyWidgetAPI:

    def __init__(self, root_widget: Widget):
        self.root_widget = root_widget

    @property
    def root(self) -> Widget:
        return self.root_widget


instance: Optional[KivyWidgetAPI] = None

__widget_queue: List[Widget] = []


def add_widget(widget: Widget):
    global instance
    if not instance:
        __widget_queue.append(widget)
        logger.debug("add instance to queue")
    else:
        instance.root.add_widget(widget)
        logger.debug("add instance to widget")


def set_instance(widget: Widget):
    global instance
    instance = KivyWidgetAPI(widget)
    logger.debug('set instance')
    for widget in __widget_queue:
        instance.root.add_widget(widget)
    logger.debug(list(instance.root.children))
