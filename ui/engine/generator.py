from dataclasses import dataclass
from typing import Callable

import torch
from PIL.Image import Image
from ldm.generate import Generate

from .parameters import ImageParams
from .preferences import ModelParams

StepCallback = Callable[[torch.Tensor, int], None]


class Generator():
    def __init__(self, params: ModelParams):
        self._pipeline = Generate(**params.to_dict())

    def load(self):
        self._pipeline.load_model()

    def generate(self, params: ImageParams, step_callback: StepCallback) -> Image:
        format = params.format
        content = params.content

        upscale = (
            None if format.upscale_factor < 2
            else (format.upscale_factor, format.upscale_strength)
        )

        param_dict = {
            "prompt": content.prompt,
            "iterations": 1,
            "steps": content.steps,
            "seed": content.seed,
            "cfg_scale": content.cfg_scale,
            "ddim_eta": content.ddim_eta,
            "skip_normalize": False,
            "image_callback": None,
            "step_callback": step_callback,
            "width": format.width,
            "height": format.height,
            "sampler_name": content.sampler,
            "seamless": format.seamless,
            "log_tokenization": False,
            "with_variations": None,
            "variation_amount": 0.0,
            "init_img": content.image_path or None,
            "init_mask": content.mask_path or None,
            "fit": True,
            "strength": 1.0 - content.image_strength,
            "gfpgan_strength": format.gfpgan_strength,
            "save_original": False,
            "upscale": upscale
        }

        if param_dict["strength"] >= 1.0:
            param_dict["init_img"] = None
            param_dict["strength"] = 0.99

        print("\nGenerator Parameters:")
        for key, value in param_dict.items():
            print(f"  {key}: {value}")

        result = self._pipeline.prompt2image(**param_dict)
        image = result[0][0]
        return image