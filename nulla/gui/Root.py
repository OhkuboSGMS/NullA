from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout


class Root(FloatLayout):
    __kv__loaded: bool = False

    def __init__(self, **kwargs):
        if not Root.__kv__loaded:
            Root.__kv__loaded = True
            Builder.load_file('nulla/res/root.kv')
        super(Root, self).__init__(**kwargs)
