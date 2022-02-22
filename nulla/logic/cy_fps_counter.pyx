import time
import cython

cdef:
    double MIN_DIFF = 0.001
    double MIN_SLEEP_TIME = 0.001
    unsigned int N_FPS_FRAME = 16

cdef double ns_to_sec(long long  ns):
    return ns / 1000_000_000.0

cdef double ns_to_ms(long long  ns):
    return ns / 1000_000.0

cdef class FPSTimer:
    cdef:
        double max_sleep_time
        long frame_count
        double over_sleep_time
        double _fps
        double last_sleep_time
        long long prev_fps_calc_time
        long long prev_start
        bint no_sleep
    def __init__(self, double target_fps =30.0, bint no_sleep=False):
        self.max_sleep_time = 1.0 / target_fps  # 1second /fps
        self.no_sleep = no_sleep
        self.frame_count = 0
        self.over_sleep_time = 0.0
        self._fps = 0.0
        self.prev_fps_calc_time = time.perf_counter_ns()
        self.prev_start = 0
        self.last_sleep_time = 0.0

    cpdef update(self):
        self.start()
        self.stop_and_wait()
    cpdef start(self):
        """
        ContextManagerが使用できないためPython版とは若干使用感が違う.
        startを実行後.
        stop_and_waitで計測を終了．FPSをsleepで調整する.
        :return: 
        """
        self.prev_start = time.perf_counter_ns()
        self.frame_count += 1

    cpdef stop_and_wait(self):
        cdef:
            long long end
            double diff
            double sleep_time
            double after_sleep

        end = time.perf_counter_ns()
        diff = ns_to_sec(end - self.prev_start)
        sleep_time = self.max_sleep_time - diff - self.over_sleep_time
        if not self.no_sleep:
            if sleep_time <= 0:
                # 最低でも1ms以上スリープする
                time.sleep(MIN_SLEEP_TIME)
                self.last_sleep_time = MIN_SLEEP_TIME
            else:
                time.sleep(sleep_time)
                self.last_sleep_time = sleep_time
        # 実際にどれだけsleepしたか(正確に指定した時間sleepするわけではない)
        after_sleep = ns_to_sec(time.perf_counter_ns() - end)
        self.over_sleep_time = after_sleep - sleep_time
        self.calc_fps()

    @property
    def fps(self):
        return self._fps

    @property
    def last_sleep(self):
        return self.last_sleep_time
    cdef calc_fps(self):
        cdef:
            long long elapsed
            double diff

        # ビット演算による剰余
        if self.frame_count & (N_FPS_FRAME - 1) == 0:
            elapsed = time.perf_counter_ns()
            diff = ns_to_sec(elapsed - self.prev_fps_calc_time)
            if diff <= 0.0:
                self._fps = N_FPS_FRAME / MIN_DIFF
            else:
                self._fps = N_FPS_FRAME / diff
            self.prev_fps_calc_time = elapsed
