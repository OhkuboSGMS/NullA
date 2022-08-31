from pathlib import Path

import cv2
import numpy as np
import onnxruntime as ort

from nulla.download import cache_download_from_github
from nulla.ml.mediapipe.face_detection import MPFaceDetection
from typer import Frame

genderList = ['Male', 'Female']


class OnnxGenderFace(MPFaceDetection):
    _url = 'https://github.com/onnx/models/blob/main/vision/body_analysis/age_gender/models/gender_googlenet.onnx?raw=true'
    _model_cache_dir = Path(__file__).parent.joinpath('.face_gender')
    _provider = ['CPUExecutionProvider']

    def __init__(self, **kwargs):
        super(OnnxGenderFace, self).__init__(**kwargs)
        result, save_path = cache_download_from_github(self._url, self._model_cache_dir)
        if not result:
            raise FileNotFoundError(self._url)
        self.model = ort.InferenceSession(str(save_path), providers=self._provider)
        self.input_name = self.model.get_inputs()[0].name
        self.output_name = self.model.get_outputs()[0].name

    def _preprocess(self, face: Frame):
        # https://github.com/onnx/models/blob/main/vision/body_analysis/age_gender/levi_googlenet.py#L65
        image = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (224, 224))
        image_mean = np.array([104, 117, 123])
        image = image - image_mean
        image = np.transpose(image, [2, 0, 1])
        image = np.expand_dims(image, axis=0)
        image = image.astype(np.float32)
        return image

    def __call__(self, frame: Frame):
        detect_result = super(OnnxGenderFace, self).__call__(frame)
        detect_result.classes = None
        lt, rb = self.crop_face(frame, detect_result)
        if not lt or not rb:
            return detect_result
        crop_face = frame[lt[1]:rb[1], lt[0]:rb[0], :]
        crop_face = self._preprocess(crop_face)
        scores = self.model.run([self.output_name], {self.input_name: crop_face})
        gender = genderList[scores[0].argmax()]

        detect_result.classes = detect_result.info = gender
        print(scores)
        return detect_result

    def draw(self, image: np.ndarray, results, *args, **kwargs):
        return super(OnnxGenderFace, self).draw(image, results, *args, *kwargs)

    def close(self):
        super(OnnxGenderFace, self).close()
        del self.model

    @classmethod
    def help(cls) -> str:
        return 'Facial Gender Recognition with ONNX. detect with MediaPipe Face Detection'

    @property
    def name(self) -> str:
        return 'OnnxGender'
