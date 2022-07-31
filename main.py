import os

os.environ['KIVY_NO_ARGS'] = '1'
os.environ["KIVY_NO_CONSOLELOG"] = "1"

from argparse import ArgumentParser
from typing import Optional, Union

from loguru import logger

from nulla.gui.App import MonitorApp
from nulla.logic.backend import Backend
from nulla.util import int_or_str


def _help_available_model():
    from nulla.__factory_util__ import walk_package
    packages = walk_package()
    print(f'Show Available Model: {len(packages)} Models')
    n_max_name = max(map(lambda x: len(x[0]), list(packages)))
    for name, abc in packages:
        print(f'{name:<{n_max_name}}:{abc}.{abc.help()}:')


def cli():
    parser = ArgumentParser('nulla')
    parser.add_argument('--source', default=None, type=int_or_str)
    parser.add_argument('--model', default=None, type=str)
    parser.add_argument('--spec_model', action='store_true', help='show available models')
    args = parser.parse_args()

    if args.spec_model:
        _help_available_model()
        return
    main(src=args.source, model=args.model)


def main(src: Union[int, str, None] = None, model: Optional[str] = None):
    try:
        backend = Backend()
        backend.start()
        app = MonitorApp(backend)
        backend.set_resource(src)
        backend.set_model(model)
        app.run()
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    cli()
