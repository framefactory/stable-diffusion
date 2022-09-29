from tkinter.tix import Form
from typing import List
from dataclasses import dataclass, field
from PIL.Image import Image

from .utils import DataClass


@dataclass
class ContentParams(DataClass):
    prompt: str = "An astronaut riding on a horse in the desert, trending on artstation"
    negative_prompt: str = ""
    image_path: str = ""
    mask_path: str = ""
    image_strength: float = 0.0
    feedback_strength: float = 0.0

    steps: int = 50
    seed: int = 59469391
    cfg_scale: float = 7.5
    sampler: str = "plms"
    ddim_eta: float = 0.0

    @staticmethod
    def from_dict(params: dict) -> "ContentParams":
        return ContentParams(**params)


@dataclass
class FormatParams(DataClass):
    width: int = 512
    height: int = 512
    seamless: bool = False
    upscale_factor: int = 1
    upscale_strength: float = 0.75
    gfpgan_strength: float = 0.0

    @staticmethod
    def from_dict(params: dict) -> "FormatParams":
        return FormatParams(**params)


@dataclass
class ContentKey:
    frame: int
    content: ContentParams

    def to_dict(self) -> dict:
        return {
            "frame": self.frame,
            "content": self.content.to_dict()
        }

    @staticmethod
    def from_dict(key: dict) -> "ContentKey":
        return ContentKey(
            frame = key["frame"],
            content = ContentParams.from_dict(key["content"])
        )


@dataclass
class SequenceParams:
    path: str
    length: int = 1
    seed_mode: str = "fixed"
    format: FormatParams = FormatParams()
    keys: List[ContentKey] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "length": self.length,
            "seed_mode": self.seed_mode,
            "format": self.format.to_dict(),
            "keys": [ key.to_dict() for key in self.keys ]
        }

    @staticmethod
    def from_dict(params: dict) -> "SequenceParams":
        return SequenceParams(
            path = params["path"],
            length = params["length"],
            seed_mode = params["seed_mode"],
            format = FormatParams.from_dict(params["format"]),
            keys = [ ContentKey.from_dict(key) for key in params["keys"] ]
        )


@dataclass
class ImageParams:
    path: str = ""
    format: FormatParams = FormatParams()
    content: ContentParams = ContentParams()

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "format": self.format.to_dict(),
            "content": self.content.to_dict()
        }

    @staticmethod
    def from_dict(params: dict) -> "ImageParams":
        return ImageParams(
            path = params["path"],
            format = FormatParams.from_dict(params["format"]),
            content = ContentParams.from_dict(params["content"])
        )
