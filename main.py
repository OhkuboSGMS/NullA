from loguru import logger

from nulla.logic.backend import Backend
from nulla.res import initialize_kv
from nulla.gui.App import MonitorApp


def main():
    try:
        initialize_kv(debug=True)
        backend = Backend(src=0)
        backend.start()
        app = MonitorApp(backend)
        app.run()
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    main()
