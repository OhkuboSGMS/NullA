import os
from typing import Sequence, Optional

from __factory_util__ import search_subclass
from ml.base import MLBase
from nulla import ml

namespace = ml.__package__ + '.'
root = os.path.dirname(__file__)

CLASS_MAP = search_subclass(os.path.dirname(ml.__file__), MLBase, 'nulla.', root)


class DetectorNotFound(Exception):
    pass


def list_detector() -> Sequence[str]:
    return tuple(CLASS_MAP.keys())


def get(name: str) -> MLBase:
    if name not in CLASS_MAP:
        raise DetectorNotFound(name, list_detector())

    return CLASS_MAP[name]
