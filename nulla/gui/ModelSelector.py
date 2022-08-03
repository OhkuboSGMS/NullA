from abc import ABCMeta
from typing import Tuple, Set, Callable, Any

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.input.motionevent import MotionEvent
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.app import App

Builder.load_file('nulla/res/model_selector.kv')


class MLItem(RecycleDataViewBehavior, BoxLayout):
    text = StringProperty()
    index = 0
    callback: Callable[[Any], None] = None
    data = ObjectProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.data = data
        if 'callback' in data:
            self.callback = data['callback']
        super(MLItem, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch: MotionEvent):
        if self.collide_point(*touch.pos) and touch.button == 'left':
            if self.callback:
                self.callback(self.data)


class ModelList(RecycleView):

    def __init__(self, **kwargs):
        super(ModelList, self).__init__(**kwargs)

    def update(self, data: Set[Tuple[str, ABCMeta]]):
        """
        ModelItemを更新
        :param data:
        :return:
        """

        def _update():
            self.data = [{
                'text': x[0],
                'data': x,
                'callback': lambda x: App.get_running_app().select_model(x[1])
            } for x in sorted(list(data), key=lambda x: x[0])]

        Clock.schedule_once(lambda ins: _update())
