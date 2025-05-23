import base64
import folder_paths
import numpy as np
import os
import requests
import torch
from PIL import Image
from io import BytesIO


class UploadToBaseNode:
    def __init__(self):
        self.type = "output"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {"default": ""}),
                "folder_id": ("STRING", {"default": ""}),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO"
            },
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "run"
    CATEGORY = "BASE"

    def run(self, image, api_key, folder_id, prompt=None, extra_pnginfo=None):
        import json
        from PIL.PngImagePlugin import PngInfo
        pnginfo = PngInfo()
        if prompt is not None:
            pnginfo.add_text("prompt", json.dumps(prompt))
        if extra_pnginfo is not None:
            for k, v in extra_pnginfo.items():
                pnginfo.add_text(k, json.dumps(v))

        image_data = image[0]
        img_array = (image_data.cpu().numpy() * 255).clip(0, 255).astype("uint8")

        # Ensure shape is (H, W, C)
        if img_array.ndim == 3 and img_array.shape[2] in {1, 3}:
            pass  # already (H, W, C)
        elif img_array.ndim == 3 and img_array.shape[0] in {1, 3}:
            img_array = np.transpose(img_array, (1, 2, 0))  # (C, H, W) -> (H, W, C)
        elif img_array.ndim == 2:
            img_array = np.expand_dims(img_array, axis=-1)
            img_array = np.repeat(img_array, 3, axis=2)
        else:
            raise ValueError(f"Unsupported image shape: {img_array.shape}")

        # If still grayscale, convert to RGB
        if img_array.shape[2] == 1:
            img_array = np.repeat(img_array, 3, axis=2)

        img = Image.fromarray(img_array)

        buffer = BytesIO()
        img.save(buffer, format="PNG", pnginfo=pnginfo)

        # Debug: write buffer to temp file to verify metadata
        import tempfile
        verify_path = os.path.join(tempfile.gettempdir(), "verify_base_upload.png")
        with open(verify_path, "wb") as f:
            f.write(buffer.getvalue())

        b64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

        response = requests.post(
            "https://us-central1-base-14bf3.cloudfunctions.net/uploadImageToBase", json={
                "imageBase64": b64_image,
                "parent": folder_id or None,
                "apiKey": api_key,
            }, timeout=30)

        if response.status_code != 200:
            raise RuntimeError(f"Upload failed with status {response.status_code}: {response.text}")

        output_dir = folder_paths.get_output_directory()
        filename = "uploaded_to_base.png"
        full_path = os.path.join(output_dir, filename)
        img.save(full_path, format="PNG", pnginfo=pnginfo)

        results = [{
            "filename": filename,
            "subfolder": "",
            "type": self.type,
        }]

        return {"ui": {"images": results}}
