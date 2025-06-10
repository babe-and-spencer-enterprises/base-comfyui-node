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
                "api_key": ("STRING", {"default": None}),
            },
            "optional": {
                "image": ("IMAGE", {"default": None}),
                "video": ("VIDEO", {"default": None}),
                "folder_id": ("STRING", {"default": None}),
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

    def run(self, image=None, video=None, api_key=None, folder_id=None, prompt=None, extra_pnginfo=None):
        import json
        from PIL import Image, PngImagePlugin
        from io import BytesIO
        import tempfile

        if image is None and video is None:
            raise ValueError("Either 'image' or 'video' must be provided.")

        if video is not None:
            mime_type = "video/mp4"
            filename = "uploaded_to_base.mp4"
            is_animated = False
            buffer = BytesIO()
            import av
            container = av.open(buffer, mode='w', format='mp4')
            stream = container.add_stream("libx264", rate=video.get_components().frame_rate)
            stream.width = video.get_dimensions()[0]
            stream.height = video.get_dimensions()[1]
            stream.pix_fmt = "yuv420p"
            for frame in video.get_components().images:
                frame = av.VideoFrame.from_ndarray(
                    torch.clamp(frame[..., :3] * 255, 0, 255).to(torch.uint8).cpu().numpy(),
                    format="rgb24")
                for packet in stream.encode(frame):
                    container.mux(packet)
            container.mux(stream.encode())
            container.close()
        else:
            # Convert batched tensor to list if needed
            if torch.is_tensor(image) and image.ndim == 4:
                image = list(image)

            def tensor_to_pil(img_tensor):
                img_array = (img_tensor.cpu().numpy() * 255).clip(0, 255).astype("uint8")

                # If it's a batch of images, select the first one (or raise if unexpected)
                if img_array.ndim == 4:
                    if img_array.shape[3] in {1, 3}:
                        img_array = img_array[0]  # Take first image in batch
                    else:
                        raise ValueError(
                            f"Unexpected channel dimension in batch: {img_array.shape}")

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

            # Removed is_animated check and related logic; animated images not supported
            if isinstance(image, list) and len(image) > 1:
                raise ValueError("Animated image export is not supported.")

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
        import tempfile
        verify_path = os.path.join(tempfile.gettempdir(), filename)
        with open(verify_path, "wb") as f:
            f.write(buffer.getvalue())

        b64_bytes = base64.b64encode(buffer.getvalue()).decode("utf-8")

        response = requests.post(
            "https://us-central1-base-14bf3.cloudfunctions.net/uploadToBase", json={
                "bytes": b64_bytes,
                "parent": folder_id,
                "apiKey": api_key,
                "mimeType": mime_type,
                "filename": filename,
            }, timeout=60)

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

        return {"ui": {"images": results}}
