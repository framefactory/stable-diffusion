from typing import List
from dataclasses import dataclass

from ui.app.utils import DataClass


def lerp(a:float, b:float, factor:float):
    return a + (b - a) * factor


@dataclass
class DreamVariables(DataClass):
    prompt: str = "An astronaut riding on a horse in the desert, trending on artstation"
    negative_prompt: str = ""
    image_strength: float = 0.0
    feedback_strength: float = 0.0

    seed_a: int = 5946931
    seed_b: int = 7192209
    seed_blend: float = 0.0
    steps: int = 50
    cfg_scale: float = 7.5
    sampler: str = "plms"
    ddim_eta: float = 0.0

    @staticmethod
    def from_dict(params: dict) -> "DreamVariables":
        return DreamVariables(**params)

    @staticmethod
    def interpolate(a: 'DreamVariables', b: 'DreamVariables', factor: float, interpolation: str) -> 'DreamVariables':
        if interpolation == "hold":
            return a

        return DreamVariables(
            prompt = a.prompt,
            negative_prompt = a.negative_prompt,
            image_strength = lerp(a.image_strength, b.image_strength, factor),
            feedback_strength = lerp(a.feedback_strength, b.feedback_strength, factor),

            seed_a = a.seed_a,
            seed_b = a.seed_b,
            seed_blend = lerp(a.seed_blend, b.seed_blend, factor),
            steps = int(lerp(float(a.steps), float(b.steps), factor)),
            cfg_scale = lerp(a.cfg_scale, b.cfg_scale, factor),
            sampler = a.sampler,
            ddim_eta=lerp(a.ddim_eta, b.ddim_eta, factor)
        )

@dataclass
class DreamConstants(DataClass):
    seed_a_random: bool = True
    seed_b_random: bool = False
    image_path: str = ""
    mask_path: str = ""

    width: int = 512
    height: int = 512
    seamless: bool = False
    upscale_factor: int = 1
    upscale_strength: float = 0.75
    gfpgan_strength: float = 0.0

    @staticmethod
    def from_dict(params: dict) -> "DreamConstants":
        return DreamConstants(**params)


@dataclass
class DreamFrame:
    path: str
    constants: DreamConstants
    variables: DreamVariables

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "constants": self.constants.to_dict(),
            "variables": self.variables.to_dict()
        }

    @staticmethod
    def from_dict(params: dict) -> "DreamFrame":
        return DreamFrame(
            path = params["path"],
            constants = DreamConstants.from_dict(params["constants"]),
            variables = DreamVariables.from_dict(params["variables"])
        )

@dataclass
class VariableKey:
    frame: int
    variables: DreamVariables

    def to_dict(self) -> dict:
        return {
            "frame": self.frame,
            "variables": self.variables.to_dict()
        }

    @staticmethod
    def from_dict(key: dict) -> "VariableKey":
        return VariableKey(
            frame = key["frame"],
            variables = DreamVariables.from_dict(key["variables"])
        )


class Dream:
    def __init__(self, path: str = "", length: int = 1, constants = DreamConstants(),
        keys: List[VariableKey] = []):

        self.path = path
        self.length = length
        self.constants = constants
        self.keys = keys

    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "length": self.length,
            "constants": self.constants.to_dict(),
            "keys": [ key.to_dict() for key in self.keys ]
        }

    @staticmethod
    def from_dict(params: dict) -> "Dream":
        return Dream(
            path = params["path"],
            length = params["length"],
            constants = DreamConstants.from_dict(params["constants"]),
            keys = [ VariableKey.from_dict(key) for key in params["keys"] ]
        )

    def interpolate(self, frame: int) -> DreamVariables:
        keys = self.keys
        count = len(keys)
        left_key = keys[count - 1]
        right_key = None
        interpolation = "linear"

        for i in range(count):
            key = keys[i]
            if key.frame > frame:
                left_key = keys[i - 1] if i > 0 else None
                right_key = keys[i]
                break

        if left_key is None:
            return right_key.variables #type:ignore
        elif right_key is None:
            return left_key.variables
        else:
            factor = (frame - left_key.frame) / (right_key.frame - left_key.frame)
            return DreamVariables.interpolate(left_key.variables, right_key.variables, factor, interpolation)
        