from .PIP_longsize import PIP_longsize, PIP_ProportionalCrop

NODE_CLASS_MAPPINGS = {
    "PIP_longsize": PIP_longsize,
    "PIP_ProportionalCrop": PIP_ProportionalCrop
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PIP_longsize": "PIP 长边调整",
    "PIP_ProportionalCrop": "PIP 等比例裁切"
}
