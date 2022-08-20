from pathlib import Path

from nulla.download import download_from_github
import tempfile


def test_download_github():
    url = 'https://github.com/onnx/models/blob/main/vision/body_analysis/emotion_ferplus/model/emotion-ferplus-8.onnx?raw=true'
    with tempfile.TemporaryDirectory() as _dir:
        result, url = download_from_github(url, _dir)
        assert result
        assert url.exists()
