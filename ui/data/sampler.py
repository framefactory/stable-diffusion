from typing import Dict
from enum import Enum


sampler_labels: Dict[str, str] = {
    "plms": "PLMS",
    "ddim": "DDIM",
    "k_dpm_2": "K DPM2",
    "k_dpm_2_a": "K DPM2 Ancestral",
    "k_euler": "K Euler",
    "k_euler_a": "K Euler Ancestral",
    "k_heun": "K Heun",
    "k_lms": "K LMS"
}

class Sampler(Enum):
    PLMS = "plms"
    DDIM = "ddim"
    K_DPM2 = "k_dpm_2"
    K_DPM2_A = "k_dpm_2_a"
    K_EULER = "k_euler"
    K_EULER_A = "k_euler_a"
    K_HEUN = "k_heun"
    K_LMS = "k_lms"

    @property
    def label(self):
        return sampler_labels[self.value]
