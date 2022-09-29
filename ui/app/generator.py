from typing import Callable, Tuple
from dataclasses import dataclass

import torch
from PIL.Image import Image
from ldm.generate import Generate
from ui.app.dream_params import DreamFrame

from ui.data import ModelParams


StepCallback = Callable[[torch.Tensor, int], None]


class Generator:
    def __init__(self, params: ModelParams, callback: StepCallback):
        self._pipeline = Generate(**params.to_dict())
        self._callback = callback

    def load(self):
        self._pipeline.load_model()

    def generate(self, params: DreamFrame) -> Tuple[Image, Image]:
        constants = params.constants
        variables = params.variables

        with_variations = [
            (variables.seed_b, variables.seed_blend)
        ] if variables.seed_blend > 0.0 else None

        generator_params = {
            "prompt": variables.prompt,
            "iterations": 1,
            "steps": variables.steps,
            "seed": variables.seed_a,
            "cfg_scale": variables.cfg_scale,
            "ddim_eta": variables.ddim_eta,
            "skip_normalize": False,
            "image_callback": None,
            "step_callback": self._callback,
            "width": constants.width,
            "height": constants.height,
            "sampler_name": variables.sampler,
            "seamless": constants.seamless,
            "log_tokenization": False,
            "with_variations": with_variations,
            "variation_amount": 0.0,
            "init_img": constants.image_path or None,
            "init_mask": constants.mask_path or None,
            "fit": True,
            "strength": 1.0 - variables.image_strength,
            "save_original": False,
        }

        if generator_params["strength"] >= 1.0:
            generator_params["init_img"] = None
            generator_params["strength"] = 0.99

        print("\nGenerator Parameters:")
        for key, value in generator_params.items():
            print(f"  {key}: {value}")


        result = self._pipeline.prompt2image(**generator_params)
        raw_image = result[0][0]

        upscale = (
            None if constants.upscale_factor < 2
            else (constants.upscale_factor, constants.upscale_strength)
        )

        print("\nUpscale/face reconstruction parameters:")
        print(f"  upscale: {upscale}")
        print(f"  gfpgan_strength: {constants.gfpgan_strength}")

        if upscale is not None or constants.gfpgan_strength > 0:
            self._pipeline.upscale_and_reconstruct(result, upscale, constants.gfpgan_strength)

        final_image = result[0][0]
        return (final_image, raw_image)