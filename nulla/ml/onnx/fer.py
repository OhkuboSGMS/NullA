from pathlib import Path
from typing import Any

import cv2
import numpy as np
import onnxruntime as ort
from mediapipe.python.solutions.drawing_utils import _normalized_to_pixel_coordinates

from nulla.download import cache_download_from_github
from nulla.ml.mediapipe.face_detection import MPFaceDetection

emotion_table = {0: 'neutral', 1: 'happiness', 2: 'surprise', 3: 'sadness',
                 4: 'anger', 5: 'disgust', 6: 'fear', 7: 'contempt'}
emotion_table_ja = {0: '通常', 1: '幸せ', 2: '驚き', 3: '悲しみ',
                    4: '怒り', 5: '嫌悪', 6: '恐怖', 7: '軽蔑'}


def softmax(x):
    y = np.exp(x - np.max(x))
    f_x = y / np.sum(np.exp(x))
    return f_x


class OnnxFER(MPFaceDetection):
    """
    onnx8以外はonnxruntimeで正しく動作しなかった
    動作環境:
    | name | value|
    | os   | Windows10|
    | python | 3.81.3 |
    | onnxruntime | 1.12.1|
    | onxx  | 1.12.0 |

    TODO 絵文字出だすと面白いかも
    TODO onnxruntime-gpuで動作確認
    
    https://github.com/onnx/models/tree/main/vision/body_analysis/emotion_ferplus
    """
    _url = 'https://github.com/onnx/models/blob/main/vision/body_analysis/emotion_ferplus/model/emotion-ferplus-8.onnx?raw=true'
    _model_cache_dir = Path(__file__).parent.joinpath('.emotion_ferplus')
    _provider = ['CPUExecutionProvider']

    def __init__(self, **kwargs):
        super(OnnxFER, self).__init__(**kwargs)
        result, save_path = cache_download_from_github(self._url, self._model_cache_dir)
        if not result:
            raise FileNotFoundError(self._url)

        self.model = ort.InferenceSession(str(save_path), providers=self._provider)
        self.input_name = self.model.get_inputs()[0].name
        self.output_name = self.model.get_outputs()[0].name

    def _crop_face(self, frame, detect_result):
        image_rows, image_cols, _ = frame.shape
        if detect_result.detections is None or len(detect_result.detections) == 0:
            return None, None
        detection = detect_result.detections[0]
        location = detection.location_data
        relative_bounding_box = location.relative_bounding_box
        lt = _normalized_to_pixel_coordinates(
            relative_bounding_box.xmin, relative_bounding_box.ymin, image_cols,
            image_rows)
        rb = _normalized_to_pixel_coordinates(
            relative_bounding_box.xmin + relative_bounding_box.width,
            relative_bounding_box.ymin + relative_bounding_box.height, image_cols,
            image_rows)
        if not lt or not rb:
            return None, None
        return lt, rb

    def __call__(self, frame):
        detect_result = super(OnnxFER, self).__call__(frame)
        detect_result.classes = None
        lt, rb = self._crop_face(frame, detect_result)
        if not lt or not rb:
            return detect_result
        crop_face = frame[lt[1]:rb[1], lt[0]:rb[0], :]

        input_shape = (1, 1, 64, 64)
        img = crop_face
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (64, 64), cv2.INTER_AREA)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        img_data = np.array(img, dtype=np.float32)
        img_data = np.resize(img_data, input_shape)

        scores = self.model.run([self.output_name], {self.input_name: img_data})
        prob = softmax(scores)
        prob = np.squeeze(prob)
        classes = np.argsort(prob)[::-1]
        detect_result.classes = classes
        detect_result.info = emotion_table[classes[0]]
        return detect_result

    def draw(self, image: np.ndarray, results: Any, *args, **kwargs):
        image = super(OnnxFER, self).draw(image, results, *args, **kwargs)
        # if results.classes is not None:
        #     classes = results.classes
        #     print(emotion_table[classes[0]])

        return image

    def close(self):
        super(OnnxFER, self).close()
        del self.model

    @classmethod
    def help(self) -> str:
        return 'Facial Expression Recognition with ONNX. detect with MediaPipe Face Detection'

    @property
    def name(self) -> str:
        return 'OnnxFER'

