from pathlib import Path
from typing import Union, Optional

from kivy.lang import Builder
from loguru import logger


def _initialize_kv_(dir_path: Union[str, Path], debug: bool = False):
    for file in Path(dir_path).parent.glob("**/*.kv"):
        if debug:
            logger.debug(file)
        Builder.load_file(str(file))


def int_or_str(v: Optional[str]) -> Union[str, int]:
    if v is None:
        return ''
    return int(v) if str.isdigit(v) else v
