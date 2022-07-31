import os

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
os.environ['KIVY_NO_ARGS'] = '1'
os.environ["KIVY_NO_CONSOLELOG"] = "0"

import sys
from argparse import ArgumentParser
from typing import Optional, Union

from loguru import logger

from nulla.gui.App import MonitorApp
from nulla.logic.backend import Backend
from nulla.util import add_file_logger, is_frozen
from nulla.util import int_or_str


def _help_available_model():
    try:
        from nulla.__factory_util__ import walk_package
        packages = walk_package()
        print(f'Show Available Model: {len(packages)} Models')
        n_max_name = max(map(lambda x: len(x[0]), list(packages)), default=0)
        for name, abc in packages:
            print(f'{name:<{n_max_name}}:{abc}.{abc.help()}:')
    except Exception as e:
        logger.exception(e)


def cli(frozen: bool):
    parser = ArgumentParser('nulla')
    parser.add_argument('--source', default=None, type=int_or_str)
    parser.add_argument('--model', default=None, type=str)
    parser.add_argument('--spec_model', action='store_true', help='show available models')
    args = parser.parse_args()

    if args.spec_model:
        _help_available_model()
        return
    main(src=args.source, model=args.model, frozen=frozen)


def main(src: Union[int, str, None] = None, model: Optional[str] = None, frozen: bool = False):
    add_file_logger()
    backend = Backend(frozen=frozen)
    backend.start()
    app = MonitorApp(backend)
    backend.load_models()
    backend.set_resource(src)
    backend.set_model(model)
    app.run()


if __name__ == '__main__':
    try:
        _frozen = is_frozen()
        if not _frozen:
            # nulla配下を検索可能に設定.
            sys.path.append('nulla')
        cli(_frozen)
    except Exception as e:
        logger.exception(e)
