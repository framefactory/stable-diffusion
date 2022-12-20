from typing import List, Dict, Any
from dataclasses import dataclass, field, asdict
from copy import copy
from sortedcontainers import SortedDict
from dacite.core import from_dict


@dataclass
class GeneratorSettings:
    prompt: str = "An astronaut riding on a horse in the desert, trending on artstation"
    negative_prompt: str = ""

    image_path: str = ""
    mask_path: str = ""
    image_strength: float = 0.0
    feedback_strength: float = 0.0

    seed_a: int = 5946931
    seed_a_randomize: bool = True
    seed_b: int = 7192209
    seed_b_randomize: bool = True
    seed_blend: float = 0.0
    steps: int = 50
    cfg_scale: float = 7.5
    sampler: str = "plms"
    ddim_eta: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> 'GeneratorSettings':
        return from_dict(GeneratorSettings, data)


def lerp(a:float, b:float, factor:float):
    return a + (b - a) * factor


def interpolate_settings(a: GeneratorSettings, b: GeneratorSettings, factor: float, mode: str):
    if mode == "hold":
        return a

    return GeneratorSettings(
        prompt = a.prompt,
        negative_prompt = a.negative_prompt,

        image_path = a.image_path,
        mask_path = a.mask_path,
        image_strength = lerp(a.image_strength, b.image_strength, factor),
        feedback_strength = lerp(a.feedback_strength, b.feedback_strength, factor),

        seed_a = a.seed_a,
        seed_a_randomize = a.seed_a_randomize,
        seed_b = a.seed_b,
        seed_b_randomize = a.seed_b_randomize,
        seed_blend = lerp(a.seed_blend, b.seed_blend, factor),
        steps = int(lerp(float(a.steps), float(b.steps), factor)),
        cfg_scale = lerp(a.cfg_scale, b.cfg_scale, factor),
        sampler = a.sampler,
        ddim_eta=lerp(a.ddim_eta, b.ddim_eta, factor)
    )

@dataclass
class OutputSettings:
    format: str = "png"
    width: int = 512
    height: int = 512
    seamless: bool = False
    upscale_factor: int = 1
    upscale_strength: float = 0.75
    gfpgan_strength: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> 'OutputSettings':
        return from_dict(OutputSettings, data)


@dataclass
class DreamStill:
    path: str = ""
    generator: GeneratorSettings = GeneratorSettings()
    output: OutputSettings = OutputSettings()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> 'DreamStill':
        return from_dict(DreamStill, data)


@dataclass
class GeneratorKey:
    frame: int
    generator: GeneratorSettings = GeneratorSettings()
    interpolation: str = "linear"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> 'GeneratorKey':
        return from_dict(GeneratorKey, data)


@dataclass
class DreamSequence:
    path: str = ""
    length: int = 1
    keys: List[GeneratorKey] = field(default_factory=lambda: [ GeneratorKey(0) ])
    output: OutputSettings = OutputSettings()

    @property
    def count(self) -> int:
        return len(self.keys)

    def get_or_interpolate_still(self, frame: int = 0) -> DreamStill:
        generator = self.get_or_interpolate_generator(frame)
        return DreamStill(self.path, generator, copy(self.output))

    def get_or_interpolate_generator(self, frame: int) -> GeneratorSettings:
        keys = self.keys
        count = len(keys)

        if count < 1:
            return GeneratorSettings()

        left_key = keys[count - 1]
        right_key = None

        for i in range(count):
            key = keys[i]
            if frame == key.frame:
                return key.generator

            if frame < key.frame:
                left_key = keys[i - 1] if i > 0 else None
                right_key = keys[i]
                break

        if left_key is None:
            return right_key.generator #type:ignore
        elif right_key is None:
            return left_key.generator
        else:
            factor = (frame - left_key.frame) / (right_key.frame - left_key.frame)
            return interpolate_settings(left_key.generator, right_key.generator,
                factor, left_key.interpolation)
        
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> 'DreamSequence':
        return from_dict(DreamSequence, data)
 