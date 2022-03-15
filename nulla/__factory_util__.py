import importlib
import inspect
import os
from pathlib import Path
from typing import Type


def iterate_py(path: str):
    """
    Pythonのスクリプトを列挙. __init__は除外
    :param path:
    :return:
    """
    for dir_path, dir_names, file_names in os.walk(path):
        for f in file_names:
            if Path(f).stem == '__init__':
                continue
            if Path(f).suffix == '.py':
                yield os.path.join(dir_path, f)


def search_subclass(path: str, base_class: Type, namespace: str, root_path: str):
    """
    base_classを継承するSubClassを検索.クラスマップを生成
    :param path:
    :param base_class:
    :param namespace:
    :param root_path:
    :return:
    """
    class_map = {}
    for i in iterate_py(path):
        module_path = os.path.splitext(os.path.relpath(i, root_path))[0]
        module_path = namespace + module_path.replace('\\', '.')
        module = importlib.import_module(module_path)
        for clazz_name, clazz in inspect.getmembers(module, inspect.isclass):
            if issubclass(type(clazz), type(base_class)):
                if clazz_name not in class_map:
                    class_map[clazz_name] = clazz
    class_map.pop(base_class.__name__)
    return class_map
