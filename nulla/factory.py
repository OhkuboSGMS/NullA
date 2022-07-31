import os
from abc import ABCMeta
from threading import Thread
from typing import Optional, Callable, Set, Tuple

from nulla import ml
from nulla.__factory_util__ import search_subclass, walk_package
from nulla.error import DetectorNotFoundError
from nulla.ml.base import MLBase

namespace = ml.__package__ + '.'
root = os.path.dirname(__file__)


def load_model_async(callback: Callable[[Set[Tuple[str, ABCMeta]]], None]):
    """
    非同期でモデルを読み込み.
    :param callback: 読み込み完了後，実行
    :return:
    """
    def load():
        packages = walk_package()
        callback(packages)

    Thread(name='Package Load Thread', target=load).start()


def get(name: Optional[str]) -> MLBase:
    """
    MLBaseを実装したnameのパスのクラスを取得する

    例: name = nulla.mlmeidpipes.facemesh.MPFaceMesh

    :param name:
    :raises DetectorNotFound
    :return:
    """
    if name is None:
        raise DetectorNotFoundError(name)

    return search_subclass(name, MLBase)
