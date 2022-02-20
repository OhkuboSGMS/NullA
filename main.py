from loguru import logger

from logic.backend import Backend
from src.res import initialize_kv
from src.gui.App import MonitorApp


def main():
    try:
        initialize_kv(debug=True)
        backend = Backend(src="test.mp4")
        backend.start()
        app = MonitorApp(backend)
        app.run()
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    main()
