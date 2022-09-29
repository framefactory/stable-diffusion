from copy import deepcopy
from .parameters import FormatParams, SequenceParams, ImageParams, ContentParams
from .interpolation import interpolate

class Job:
    type = "Job"

class ImageJob(Job):
    type = "ImageJob"

    def __init__(self, params: ImageParams):
        self.params = deepcopy(params)

class SequenceJob(Job):
    type = "SequenceJob"

    def __init__(self, params: SequenceParams):
        self.params = deepcopy(params)

    def get_interpolated_content(self, frame: int) -> ContentParams:
        keys = self.params.keys
        count = len(keys)
        left_key = keys[count - 1]
        right_key = None
        interpolation = "hold"

        for i in range(count):
            key = keys[i]
            if key.frame > frame:
                left_key = keys[i - 1] if i > 0 else None
                right_key = keys[i]
                break

        if left_key is None:
            return right_key.content #type:ignore
        elif right_key is None:
            return left_key.content
        else:
            factor = (frame - left_key.frame) / (right_key.frame - left_key.frame)
            return interpolate(left_key.content, right_key.content, factor, interpolation)
        