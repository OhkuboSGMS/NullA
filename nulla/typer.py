from typing import Tuple, Union

from nptyping import NDArray, UInt8, Shape

Frame = NDArray[Shape["*,*,3"], UInt8]
Number = Union[int, float]
Point = Tuple[Number, Number]
