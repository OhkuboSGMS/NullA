import numpy as np
from kivy.core.image import Texture


def cv2_to_kivy(image: np.ndarray) -> Texture:
    texture = Texture.create(size=(image.shape[1], image.shape[0]), colorfmt='bgr',
                             bufferfmt='ubyte')  # BGRモードで用意,ubyteはデフォルト引数なので指定なくてもよい
    texture.blit_buffer(image.tostring(), colorfmt='bgr', bufferfmt='ubyte')  # ★ここもここもBGRで指定しないとRGBになって色の表示がおかしくなる
    texture.flip_vertical()  # 画像を上下反転する

    return texture
