from dataclasses import dataclass
from .utils import DataClass


@dataclass
class ModelParams(DataClass):
    """
    Model parameters
    """
    config: str = "configs/stable-diffusion/v1-inference.yaml"
    weights: str = "models/ldm/stable-diffusion-v1/model.ckpt"
    precision: str = "autocast"
    full_precision: bool = True
    device_type: str = "cuda"

    @staticmethod
    def from_dict(params: dict) -> "ModelParams":
        return ModelParams(**params)


@dataclass
class Preferences:
    library_path: str = "library"
    model_params: ModelParams = ModelParams()

    def to_dict(self) -> dict:
        return {
            "library_path": self.library_path,
            "model_params": self.model_params.to_dict()
        }

    @staticmethod
    def from_dict(prefs: dict):
        return Preferences(
            library_path = prefs["library_path"],
            model_params = ModelParams.from_dict(prefs["model_params"])
        )
