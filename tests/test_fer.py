import tarfile
import tempfile
from pathlib import Path

import numpy as np
import onnxruntime as ort

from nulla.download import download_from_github
from nulla.ml.onnx import load_proto


def test_inference():
    with tempfile.TemporaryDirectory() as t:
        result, save_path = download_from_github(
            'https://github.com/onnx/models/blob/main/vision/body_analysis/emotion_ferplus/model/emotion-ferplus-8.tar.gz?raw=true',
            t)
        assert result
        assert save_path.exists()
        with tarfile.open(save_path, 'r') as tar:
            tar.extractall(t)

        result, model_save_path = download_from_github(
            'https://github.com/onnx/models/blob/main/vision/body_analysis/emotion_ferplus/model/emotion-ferplus-8.onnx?raw=true',
            t)
        assert result
        assert model_save_path.exists()

        input_pb = load_proto(Path(t).joinpath('model/test_data_set_0/input_0.pb'))
        output_pb = load_proto(Path(t).joinpath('model/test_data_set_0/output_0.pb'))

        assert input_pb.shape == (1, 1, 64, 64)
        assert output_pb.shape == (1, 8)
        session = ort.InferenceSession(str(model_save_path), providers=['CPUExecutionProvider'])
        pred = session.run([session.get_outputs()[0].name], {session.get_inputs()[0].name: input_pb})

        np.testing.assert_almost_equal(output_pb, pred[0])
