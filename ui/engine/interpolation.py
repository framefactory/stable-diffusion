
from ui.engine.parameters import ContentParams
from .parameters import ContentParams

def lerp(a:float, b:float, factor:float):
    return a + (b - a) * factor

def interpolate(a: ContentParams, b: ContentParams, factor: float, interpolation: str) -> ContentParams:
    if interpolation == "hold":
        return a

    return ContentParams(
        prompt=a.prompt,
        negative_prompt=a.negative_prompt,
        image_path=a.image_path,
        mask_path=a.mask_path,
        image_strength=lerp(a.image_strength, b.image_strength, factor),
        feedback_strength=lerp(a.feedback_strength, b.feedback_strength, factor),
        steps=int(lerp(float(a.steps), float(b.steps), factor)),
        seed=a.seed,
        cfg_scale= lerp(a.cfg_scale, b.cfg_scale, factor),
        sampler=a.sampler,
        ddim_eta=lerp(a.ddim_eta, b.ddim_eta, factor)
    )