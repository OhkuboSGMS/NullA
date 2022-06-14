import importlib
import inspect
import pkgutil
from abc import ABCMeta
from itertools import chain
from typing import Type, TypeVar, Set, Tuple

from nulla.error import DetectorNotInheritError
from nulla.ml.base import MLBase

T = TypeVar('T')


def search_subclass(path: str, base_class: Type[T]) -> T:
    """
    base_classを継承したpathのclassを取得
    取得したclassがbase_classを継承していない場合はDetectorNotInheritError発生
    :param path: Search Path
    :param base_class: Implemented Class
    :return: T
    :raises ModuleNotFoundError
    :raises DetectorNotInheritError
    """
    *namespace, class_name = path.split('.')
    _attr = getattr(importlib.import_module('.'.join(namespace)), class_name)
    if not issubclass(_attr, base_class):
        raise DetectorNotInheritError(_attr, base_class)
    return _attr


def walk_package(package_name: str = 'nulla', filter_sub_package: str = 'ml', fetch_class: Type = MLBase) \
        -> Set[Tuple[str, ABCMeta]]:
    """
    あるパッケージからfetch_classを継承したclassを抽出する

    参考:https://qiita.com/inon3135/items/54bf58c7c50c59e8ae3c
       :https://docs.python.org/3/library/importlib.html#importlib.import_module
    :param package_name:列挙したいパッケージ
    :param filter_sub_package: 抽出したいサブパッケージ
    :param fetch_class: 抽出したいベースクラス
    :return:
    """
    # package_name配下のすべてからモジュールを抽出
    namespaces = map(lambda x: '.'.join([package_name, x.name]),
                     filter(lambda x: not x.ispkg and filter_sub_package in x.name,
                            pkgutil.walk_packages([package_name])))
    # moduleをインポートして具体化する
    modules = map(lambda namespace: importlib.import_module(namespace), namespaces)
    # 各具象モジュールからclassだけを抽出する
    classes = chain.from_iterable(map(lambda module: inspect.getmembers(module, inspect.isclass), modules))
    # fetch_classのサブクラスのみを抽出
    same_base_classes = filter(lambda t: issubclass(t[1], fetch_class) and t[1] != fetch_class, classes)
    # TODO Packageごとに分類
    return set(same_base_classes)
