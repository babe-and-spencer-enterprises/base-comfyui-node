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
                "fps": ("FLOAT", {"default": 10.0, "min": 0.01, "max": 1000.0, "step": 0.01}),
                "lossless": ("BOOLEAN", {"default": False}),
                "quality": ("INT", {"default": 80, "min": 0, "max": 100}),
                "method": (["default", "fastest", "slowest"], {"default": "default"}),
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

    def run(self, image, api_key, folder_id, fps, lossless, quality, method, prompt=None, extra_pnginfo=None):
        # Convert batched tensor to list if needed
        if torch.is_tensor(image) and image.ndim == 4:
            image = list(image)
        import json
        from PIL import Image, PngImagePlugin
        from io import BytesIO
        import tempfile

        def tensor_to_pil(img_tensor):
            img_array = (img_tensor.cpu().numpy() * 255).clip(0, 255).astype("uint8")

            # If it's a batch of images, select the first one (or raise if unexpected)
            if img_array.ndim == 4:
                if img_array.shape[3] in {1, 3}:
                    img_array = img_array[0]  # Take first image in batch
                else:
                    raise ValueError(f"Unexpected channel dimension in batch: {img_array.shape}")

            if img_array.ndim == 3:
                if img_array.shape[0] in {1, 3}:
                    img_array = np.transpose(img_array, (1, 2, 0))  # (C, H, W) → (H, W, C)
                elif img_array.shape[2] not in {1, 3}:
                    raise ValueError(f"Unexpected channel dimension: {img_array.shape}")
            elif img_array.ndim == 2:
                img_array = np.expand_dims(img_array, axis=-1)
                img_array = np.repeat(img_array, 3, axis=2)
            else:
                raise ValueError(f"Unsupported image shape: {img_array.shape}")

            if img_array.shape[2] == 1:
                img_array = np.repeat(img_array, 3, axis=2)

            return Image.fromarray(img_array)

        is_animated = isinstance(image, list) and len(image) > 1

        if is_animated:
            # Animated WebP logic
            pil_images = [tensor_to_pil(t) for t in image]
            buffer = BytesIO()
            pil_images[0].save(
                buffer,
                format="WEBP",
                save_all=True,
                append_images=pil_images[1:],
                duration=int(1000 / fps),
                loop=0,
                lossless=lossless,
                quality=quality,
                method={"default": 4, "fastest": 0, "slowest": 6}.get(method, 4),
            )
            mime_type = "image/webp"
            filename = "uploaded_to_base.webp"
        else:
            # Static PNG logic
            img_tensor = image[0] if isinstance(image, list) else image
            img = tensor_to_pil(img_tensor)

            pnginfo = PngImagePlugin.PngInfo()
            if prompt is not None:
                pnginfo.add_text("prompt", json.dumps(prompt))
            if extra_pnginfo is not None:
                for k, v in extra_pnginfo.items():
                    pnginfo.add_text(k, json.dumps(v))

            buffer = BytesIO()
            img.save(buffer, format="PNG", pnginfo=pnginfo)
            mime_type = "image/png"
            filename = "uploaded_to_base.png"

        # Save locally for debug
        verify_path = os.path.join(tempfile.gettempdir(), filename)
        with open(verify_path, "wb") as f:
            f.write(buffer.getvalue())

        b64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

        response = requests.post(
            "https://us-central1-base-14bf3.cloudfunctions.net/uploadToBase", json={
                "imageBase64": b64_image,
                "parent": folder_id or None,
                "apiKey": api_key,
                "mimeType": mime_type,
                "filename": filename,
            }, timeout=30)

        if response.status_code != 200:
            raise RuntimeError(f"Upload failed with status {response.status_code}: {response.text}")

        output_dir = folder_paths.get_output_directory()
        full_path = os.path.join(output_dir, filename)
        with open(full_path, "wb") as f:
            f.write(buffer.getvalue())

        results = [{
            "filename": filename,
            "subfolder": "",
            "type": self.type,
        }]

        animated = is_animated
        return {"ui": {"images": results, "animated": (animated,)}}
