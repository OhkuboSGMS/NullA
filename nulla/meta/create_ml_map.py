import os

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

import sys
from loguru import logger
from nulla.__factory_util__ import walk_package


def generate(py_path: str = os.path.join('nulla', 'models.py')):
    sys.path.append('nulla')
    """
    PyInstaller用に静的なモデル配置を作成
    :param py_path: 
    :return: 
    """
    logger.debug(f'Create Model Map to {py_path}')
    with open(py_path, 'w', encoding='UTF-8') as fp:
        classes = walk_package()
        models = []
        for name, clazz in classes:
            models.append(name)
            fp.write(f'from {clazz.__module__} import {name}' + '\n')

        fp.write('\n')
        fp.write('models = {\n')
        for name in models:
            fp.write(f'\t\'{name}\': {name},\n')
        fp.write('}\n')
    exit()


if __name__ == '__main__':
    generate()
