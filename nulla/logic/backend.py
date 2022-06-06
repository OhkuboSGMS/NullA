import threading
import time
from pathlib import Path
from threading import Thread
from typing import Union, Optional, Callable, NoReturn

import numpy as np
from rx.subject import Subject

from nulla import factory
from nulla.logic.fps_counter import FPSTimer
# from logic.cy_fps_counter import FPSTimer
from nulla.logic.player import Player


class Backend:
    lock = threading.Lock()

    def __init__(self, on_update: Callable[[np.ndarray], NoReturn] = None):
        self.player: Optional[Player] = None
        self.process_thread: Optional[Thread] = None
        self.end: bool = False
        self.on_initialize = Subject()
        self.on_update = Subject()
        if on_update:
            self.on_update.subscribe(on_update)
        self.fps_timer = FPSTimer(target_fps=30)
        # self.models = [MPFaceMesh()]
        # self.models = [MPSelfieSegmentation(), MPFaceCover('assets/nc73730.png')]
        # self.models = [BarcodeDetector()]
        self.models = [factory.get('MPFaceMesh')()]
        # self.models = [MPSelfieSegmentation(),FaceBlend('assets/ueda.webp')]

    # Float Layout に対してのアクセスを持っておけばよい？
    def set_resource(self, src: Optional[Union[int, str]] = None):
        if src is None:
            self.on_initialize.on_next(None)
            return
        with self.lock:
            self.end = True
            self.process_thread.join()

            if self.player:
                self.player.close()
            self.player = Player(src)
            self.on_initialize.on_next(src)
            self.end = False
            self.start()

    def start(self):
        self.process_thread = Thread(target=self.run, name='Backend', daemon=True)
        self.process_thread.start()

    def run(self):
        while not self.end and True:
            if self.player is None:
                time.sleep(0.01)
                continue
            # with self.fps_timer.update():
            self.fps_timer.start()
            # start fps timer
            frame = self.player.next()
            for model in self.models:
                result = model(frame)
                frame = model.draw(frame, result)
            # self.fps_timer.draw(frame)
            # stop and wait
            self.fps_timer.stop_and_wait()
            self.on_update.on_next((frame, self.fps_timer.fps, self.player.source, 'FaceMesh'))
            # print(f"FPS:{self.fps_timer.fps:.2f} last sleep time:{self.fps_timer.last_sleep}")
