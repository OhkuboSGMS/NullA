import os
from typing import Optional

from nulla.error import DetectorNotFoundError
from nulla import ml
from nulla.ml.base import MLBase
from nulla.__factory_util__ import search_subclass, walk_package

namespace = ml.__package__ + '.'
root = os.path.dirname(__file__)


# def list_detector() -> Sequence[str]:
#     return tuple(CLASS_MAP.keys())


def get(name: Optional[str]) -> MLBase:
    """
    MLBaseを実装したnameのパスのクラスを取得する

    例: name = nulla.mlmeidpipes.facemesh.MPFaceMesh

    :param name:
    :raises DetectorNotFound
    :return:
    """
    walk_package()
    if name is None:
        raise DetectorNotFoundError(name)

    return search_subclass(name, MLBase)
