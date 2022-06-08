import os

os.environ['KIVY_NO_ARGS'] = '1'
from argparse import ArgumentParser
from typing import Optional, Union

from loguru import logger

from nulla.gui.App import MonitorApp
from nulla.logic.backend import Backend
from nulla.res import initialize_kv
from nulla.util import int_or_str


def cli():
    parser = ArgumentParser('nulla')
    parser.add_argument('--source', default=None, type=int_or_str)
    parser.add_argument('--model', default=None, type=str)
    args = parser.parse_args()
    main(src=args.source, model=args.model)


def main(src: Union[int, str, None] = None, model: Optional[str] = None):
    try:
        initialize_kv(debug=True)
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
