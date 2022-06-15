from kivy.uix.floatlayout import FloatLayout

from nulla.gui.LazyWidget import LazyWidget


class Root(LazyWidget, FloatLayout):

    def __init__(self, **kwargs):
        super(Root, self).__init__(kv_file='nulla/res/root.kv', **kwargs)
