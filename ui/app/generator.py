from typing import Callable, Tuple

import torch
from PIL.Image import Image
from ldm.generate import Generate

from ui.data import ModelParams, DreamImage


StepCallback = Callable[[torch.Tensor, int], None]


class Generator:
    def __init__(self, params: ModelParams, callback: StepCallback):
        self._pipeline = Generate(**params.to_dict())
        self._callback = callback

    def load(self):
        self._pipeline.load_model()

    def generate(self, dream: DreamImage) -> Tuple[Image, Image]:
        output = dream.output
        generator = dream.generator

        with_variations = [
            (generator.seed_b, generator.seed_blend)
        ] if generator.seed_blend > 0.0 else None

        params = {
            "prompt": generator.prompt,
            "iterations": 1,
            "steps": generator.steps,
            "seed": generator.seed_a,
            "cfg_scale": generator.cfg_scale,
            "ddim_eta": generator.ddim_eta,
            "skip_normalize": False,
            "image_callback": None,
            "step_callback": self._callback,
            "width": output.width,
            "height": output.height,
            "sampler_name": generator.sampler,
            "seamless": output.seamless,
            "log_tokenization": False,
            "with_variations": with_variations,
            "variation_amount": 0.0,
            "init_img": generator.image_path or None,
            "init_mask": generator.mask_path or None,
            "fit": True,
            "strength": 1.0 - generator.image_strength,
            "save_original": False,
        }

        if params["sampler_name"] is not "ddim":
            params["ddim_eta"] = 0.0

        if params["strength"] >= 1.0:
            params["init_img"] = None
            params["strength"] = 0.99

        print("\nGenerator Parameters:")
        for key, value in params.items():
            print(f"  {key}: {value}")


        result = self._pipeline.prompt2image(**params)
        raw_image = result[0][0]

        upscale = (
            None if output.upscale_factor < 2
            else (output.upscale_factor, output.upscale_strength)
        )

        print("\nUpscale/face reconstruction parameters:")
        print(f"  upscale: {upscale}")
        print(f"  gfpgan_strength: {output.gfpgan_strength}")

        if upscale is not None or output.gfpgan_strength > 0:
            self._pipeline.upscale_and_reconstruct(result, upscale, output.gfpgan_strength)

        final_image = result[0][0]
        return (final_image, raw_image)