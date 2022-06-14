import numpy as np
import cv2
from nulla.ml.base import MLBase


class BarcodeDetector(MLBase):

    def __init__(self):
        self.detector = cv2.barcode_BarcodeDetector()

    def __call__(self, image, *args, **kwargs):
        ok, decoded_info, decoded_type, corners = self.detector.detectAndDecode(image)
        # print(ok, decoded_info, decoded_type, corners)
        return {'is_detect': ok, 'info': decoded_info, 'type': decoded_type, 'point': corners}

    def draw(self, image: np.ndarray, result, *args, **kwargs):
        corners = result['point']
        # imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        # contours, h = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # print(contours)
        # if contours:
        #     cv2.drawContours(image,contours,-1,(255,255,0),3)
        #     return image
        if corners is None:
            return image
        print(corners)
        corners = np.array(corners,dtype=np.int)
        cv2.drawContours(image, np.array(corners), -1, (255, 0, 0))
        # for point in corners:
        #     print(corners)
        #     cv2.drawContours(image, contours, -1, (255, 255, 255))
        # for point in corners:
        return image

    def close(self):
        pass
