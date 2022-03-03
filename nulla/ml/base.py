import abc
from abc import ABCMeta
import numpy as np


class MLBase(metaclass=ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def draw(cls, image: np.ndarray, *args, **kwargs):
        return image