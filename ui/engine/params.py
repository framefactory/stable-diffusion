from typing import Optional, Tuple, List
from dataclasses import dataclass, field
from inspect import getmembers, isroutine
from enum import Enum
from copy import copy, deepcopy

from PIL.Image import Image


class Sampler(Enum):
    PLMS = "plms"
    DDIM = "ddim"
    K_DPM2 = "k_dpm_2"
    K_DPM2_A = "k_dpm_2_a"
    K_EULER = "k_euler"
    K_EULER_A = "k_euler_a"
    K_HEUN = "k_heun"
    K_LMS = "k_lms"

class DataClass:
    def to_dict(self) -> dict:
        attribs = getmembers(self, lambda a: not isroutine(a))
        attribs = [ a for a in attribs if not a[0].startswith("__") ]
        return deepcopy(dict(attribs))

@dataclass
class ModelParams(DataClass):
    """
    Model parameters
    """
    config: str = "configs/stable-diffusion/v1-inference.yaml"
    weights: str = "models/ldm/stable-diffusion-v1/model.ckpt"
    full_precision: bool = True

@dataclass
class ImageParams(DataClass):
    """
    Image generation parameters
    """
    prompt: str = "An astronaut riding on a horse in the desert, trending on artstation"
    steps: int = 50
    seed: Optional[int] = 0
    cfg_scale: float = 7.5
    ddim_eta: float = 0.0
    width: int = 512
    height: int = 512
    sampler_name: str = Sampler.PLMS.value
    seamless: bool = False
    log_tokenization: bool = False
    init_img: Optional[Image] = None
    strength: float = 0.0
    gfpgan_strength: float = 0.0
    upscale: Optional[Tuple[int, float]] = None # (2, 0.75)

@dataclass
class ImageItem:
    image: Image
    path: str
    params: ImageParams
    rating: int = 0
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "params": self.params.to_dict(),
            "rating": self.rating,
            "tags": copy(self.tags)
        }

@dataclass
class ImageResult:
    """
    Result from image generation
    """
    params: ImageParams
    image: Image