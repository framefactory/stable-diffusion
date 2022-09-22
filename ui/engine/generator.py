from ldm.generate import Generate

from .params import ModelParams, ImageParams


class Generator():
    def __init__(self, params = ModelParams()):
        print(params.to_dict())
        self.pipeline = Generate(**params.to_dict())

    def load(self):
        self.pipeline.load_model()

    def generate(self, params = ImageParams()):
        result = self.pipeline.prompt2image(**params.to_dict())
        image = result[0][0]
        return image