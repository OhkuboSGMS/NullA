import threading
import time
from abc import ABCMeta
from threading import Thread
from typing import Union, Optional, Callable, NoReturn, List, Dict

import numpy as np
from loguru import logger
from rx.subject import Subject

from nulla import factory
from nulla.error import DetectorNotFoundError
from nulla.logic.fps_counter import FPSTimer
# from logic.cy_fps_counter import FPSTimer
from nulla.logic.player import Player
from nulla.ml.base import MLBase


class Backend:
    lock = threading.Lock()

    def __init__(self, on_update: Callable[[np.ndarray], NoReturn] = None, frozen: bool = False, data: Dict = {}):
        self.frozen = frozen
        self.data = data
        self.player: Optional[Player] = None
        self.models: List[MLBase] = []
        self.process_thread: Optional[Thread] = None

        self.end: bool = False
        self.on_initialize = Subject()
        self.on_update = Subject()
        self.on_load_model = Subject()

        if on_update:
            self.on_update.subscribe(on_update)
        self.fps_timer = FPSTimer(target_fps=30)

    def load_models(self):
        factory.load_model_async(lambda v: self.on_load_model.on_next(v), self.frozen)

    # Float Layout に対してのアクセスを持っておけばよい？
    def set_resource(self, src: Union[int, str, None] = None):
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

    def set_model(self, src: Union[str, ABCMeta, None]):
        if src is None:
            logger.warning('Not Set Model')
            return

        if type(src) == ABCMeta:
            with self.lock:
                for model in self.models:
                    model.close()
                self.models = [src(**self.data)]
            return
        try:
            with self.lock:
                new_model = [factory.get(src)(**self.data)]
                for model in self.models:
                    model.close()
                self.models = new_model
        except ModuleNotFoundError as e:
            logger.warning(e)
        except DetectorNotFoundError as e:
            logger.warning(DetectorNotFoundError)

    def start(self):
        self.process_thread = Thread(target=self.run, name='Backend', daemon=True)
        self.process_thread.start()

    def run(self):
        try:
            while not self.end and True:
                if self.player is None:
                    time.sleep(0.01)
                    continue
                self.fps_timer.start()
                # start fps timer
                frame = self.player.next()
                with self.lock:
                    result = None
                    for model in self.models:
                        result = model(frame)
                        frame = model.draw(frame, result)
                    # modelから GUIに表示してほしい情報を受け取る
                info = getattr(result, 'info', '')

                # stop and wait
                self.fps_timer.stop_and_wait()
                # TODO make class
                self.on_update.on_next(
                    (frame, self.fps_timer.fps, self.player.source, [m.name for m in self.models], info))
            for model in self.models:
                model.close()
        except Exception as e:
            logger.exception(e)
