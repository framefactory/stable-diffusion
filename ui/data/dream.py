from typing import List, Dict, Any
from dataclasses import dataclass, field, asdict
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
    seed_b: int = 7192209
    seed_blend: float = 0.0
    seed_randomize: bool = True
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
        seed_b = a.seed_b,
        seed_blend = lerp(a.seed_blend, b.seed_blend, factor),
        seed_randomize = a.seed_randomize,
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
class DreamImage:
    path: str = ""
    generator: GeneratorSettings = GeneratorSettings()
    output: OutputSettings = OutputSettings()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> 'DreamImage':
        return from_dict(DreamImage, data)


@dataclass
class GeneratorKey:
    frame: int
    interpolation: str = "linear"
    settings: GeneratorSettings = GeneratorSettings()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> 'GeneratorKey':
        return from_dict(GeneratorKey, data)


@dataclass
class DreamSequence:
    path: str = ""
    length: int = 1
    keys: List[GeneratorKey] = field(default_factory=list)
    output: OutputSettings = OutputSettings()

    def interpolate(self, frame: int) -> GeneratorSettings:
        keys = self.keys
        count = len(keys)
        left_key = keys[count - 1]
        right_key = None

        for i in range(count):
            key = keys[i]
            if key.frame > frame:
                left_key = keys[i - 1] if i > 0 else None
                right_key = keys[i]
                break

        if left_key is None:
            return right_key.settings #type:ignore
        elif right_key is None:
            return left_key.settings
        else:
            factor = (frame - left_key.frame) / (right_key.frame - left_key.frame)
            return interpolate_settings(left_key.settings, right_key.settings,
                factor, left_key.interpolation)
        
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> 'DreamSequence':
        return from_dict(DreamSequence, data)
 