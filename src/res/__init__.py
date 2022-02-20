from pathlib import Path

from kivy.lang import Builder
from loguru import logger


def initialize_kv(debug: bool = False):
    for file in Path(__file__).parent.glob("**/*.kv"):
        if debug:
            logger.debug(file)
        Builder.load_file(str(file))
