from abc import ABCMeta
from threading import Thread
from typing import Optional, Callable, Set, Tuple

from loguru import logger

from nulla.__factory_util__ import search_subclass, walk_package
from nulla.error import DetectorNotFoundError
from nulla.ml.base import MLBase


def load_model_async(callback: Callable[[Set[Tuple[str, ABCMeta]]], None], frozen: bool = False):
    """
    非同期でモデルを読み込み.
    :param callback: 読み込み完了後，実行
    :param frozen: アプリかpythonから実行か
    :return:
    """
    if frozen:
        from nulla.models import models
        data: Set[Tuple[str, ABCMeta]] = {(k, v) for k, v in models.items()}
        callback(data)
    else:
        def load():
            try:
                packages = walk_package()
                callback(packages)
            except Exception as e:
                logger.exception(e)

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
