import time
from pathlib import Path
from threading import Thread
from typing import Union, Optional, Callable, NoReturn

import numpy as np

from logic.player import Player


class Backend:
    def __init__(self, src: Optional[str] = None, on_update: Callable[[np.ndarray], NoReturn] = None):
        self.player = None
        self.on_update = on_update
        self.set_resource(src)

    def set_resource(self, src: Optional[Union[str, Path]]):
        if src is None:
            return
        self.player = Player(src)

    def start(self):
        Thread(target=self.run, name='Backend', daemon=True).start()

    def run(self):
        while True:
            if self.player is None:
                time.sleep(0.01)
                continue

            frame = self.player.next()
            if frame is None:
                time.sleep(0.01)
                continue
            if self.on_update is not None:
                self.on_update(frame)
            #TODO FPS調整方法
            #TODO 動画のFPSより調整を行う
            time.sleep(0.05)
