import os
from typing import Sequence, Optional

from nulla import ml
from nulla.__factory_util__ import search_subclass
from nulla.ml.base import MLBase

namespace = ml.__package__ + '.'
root = os.path.dirname(__file__)

# TODO 外部注入も可能にする
CLASS_MAP = search_subclass(os.path.dirname(ml.__file__), MLBase, 'nulla.', root)


class DetectorNotFound(Exception):
    pass


def list_detector() -> Sequence[str]:
    return tuple(CLASS_MAP.keys())


def get(name: Optional[str]) -> MLBase:
    if name is None or name not in CLASS_MAP:
        raise DetectorNotFound(name, list_detector())

    return CLASS_MAP[name]
