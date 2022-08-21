from pathlib import Path
from typing import Union

import onnx
from onnx import numpy_helper
import numpy as np


def load_proto(file: Union[str, Path]) -> np.ndarray:
    """
    .pbファイルをnumpyデータとして読み込み
    :param file:
    :return:
    """
    tensor = onnx.TensorProto()
    with open(file, 'rb') as f:
        tensor.ParseFromString(f.read())
    return numpy_helper.to_array(tensor)
