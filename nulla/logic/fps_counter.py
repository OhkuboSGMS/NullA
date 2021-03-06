import time
from contextlib import contextmanager
import ctypes
import platform

import cv2
import numpy as np

winmm = ctypes.WinDLL('winmm')


def time_begin(period: int):
    if platform.system() == 'Windows':
        winmm.timeBeginPeriod(period)


def time_end(period: int):
    if platform.system() == 'Windows':
        winmm.timeEndPeriod(period)


def ns_to_sec(ns: int) -> float:
    return ns / 1000_000_000


def ns_to_ms(ns: int) -> float:
    return ns / 1000_000


font_face = cv2.FONT_HERSHEY_PLAIN


class FPSTimer:
    MIN_SLEEP_TIME = 0.001  # 1ms
    N_FPS_FRAME = 16  # FPSを計算する頻度
    # mod演算の高速化のため，割る数は2のべき乗にする
    assert bin(N_FPS_FRAME).count("1")

    def __init__(self, target_fps: float = 30.0, no_sleep: bool = False):
        self.max_sleep_time = 1 / target_fps  # 1second /fps
        self.no_sleep = no_sleep
        self.frame_count = 0
        self.over_sleep_time = 0
        self._fps = 0
        self.prev_fps_calc_time = time.perf_counter_ns()
        self.prev_start = 0
        self.last_sleep_time = 0

    @contextmanager
    def update(self):
        self.start()
        yield
        self.stop_and_wait()

    def start(self):
        self.prev_start = time.perf_counter_ns()
        self.frame_count += 1

    def stop_and_wait(self):
        end = time.perf_counter_ns()
        diff = ns_to_sec(end - self.prev_start)
        sleep_time = self.max_sleep_time - diff - self.over_sleep_time
        if not self.no_sleep:
            time_begin(1)
            if sleep_time <= 0:
                target_sleep_time = self.MIN_SLEEP_TIME
                # 最低でも1ms以上スリープする(保証はない)
            else:
                target_sleep_time = sleep_time
            self.last_sleep_time = target_sleep_time
            time.sleep(target_sleep_time)
            time_end(1)
        # 実際にどれだけsleepしたか(正確に指定した時間sleepするわけではない)
        after_sleep = ns_to_sec(time.perf_counter_ns() - end)
        self.over_sleep_time = after_sleep - sleep_time
        # print(f'Max Sleep:{self.max_sleep_time},diff:{diff},over_sleep:{self.over_sleep_time}')
        # print(f"Sleep Time:{sleep_time * 1000:.3f}ms "
        #       f"Target Sleep Time:{target_sleep_time * 1000:.3f}ms "
        #       f"actual sleep time:{after_sleep * 1000:.3f}ms "
        #       f"over sleep:{self.over_sleep_time * 1000:.3f}ms")
        self.calc_fps()

    @property
    def fps(self):
        return self._fps

    @property
    def last_sleep(self):
        return self.last_sleep_time

    def calc_fps(self):
        # ビット演算による剰余
        if self.frame_count & (self.N_FPS_FRAME - 1) == 0:
            elapsed = time.perf_counter_ns()
            diff = ns_to_sec(elapsed - self.prev_fps_calc_time)
            self._fps = self.N_FPS_FRAME / diff
            self.prev_fps_calc_time = elapsed

    def draw(self, image: np.ndarray):
        text = f'FPS:{self.fps:.1f}'
        size, baseline = cv2.getTextSize(text, font_face, 1, 2)
        cv2.putText(image, text, (0, size[1] + baseline), font_face, 1, (255, 255, 255), 2)
