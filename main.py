from typing import Union, Optional

from loguru import logger

from nulla.logic.backend import Backend
from nulla.res import initialize_kv
from nulla.gui.App import MonitorApp
from argparse import ArgumentParser


def cli():
    parser = ArgumentParser('nulla')
    parser.add_argument('--source', default=0, type=Union[str, int])
    parser.add_argument('--model', default=None, type=Optional[str])

    args = parser.parse_args()
    main(src=args.source, model=args.model)


def main(src=0, model=None):
    try:
        initialize_kv(debug=True)
        backend = Backend(src=src)
        backend.start()
        app = MonitorApp(backend)
        app.run()
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    main()
