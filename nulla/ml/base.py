import abc
from abc import ABCMeta
from typing import Any

import numpy as np


class MLBase(metaclass=ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def draw(self, image: np.ndarray, results: Any, *args, **kwargs):
        return image

    @abc.abstractmethod
    def close(self):
        pass

    @classmethod
    @abc.abstractmethod
    def help(self) -> str:
        return 'This is Base Class'

    @property
    @abc.abstractmethod
    def name(self) -> str:
        return 'MLBase '
