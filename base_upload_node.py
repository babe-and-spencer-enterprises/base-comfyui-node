import requests
from PIL import Image
from io import BytesIO
import base64
import numpy as np
import torch

class UploadToBaseNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {"default": ""}),
                "prompt": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "run"
    CATEGORY = "BASE"

    def run(self, image, api_key, prompt):
        print("BASE node: running")
        print("API key:", api_key)
        print("Prompt:", prompt)

        image_data = image[0]
        img_array = (image_data.cpu().numpy().transpose(1, 2, 0) * 255).clip(0, 255).astype("uint8")
        print("Image shape:", img_array.shape)

        if img_array.shape[2] == 1:
            img_array = np.repeat(img_array, 3, axis=2)
        img = Image.fromarray(img_array)
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        b64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

        response = requests.post("https://us-central1-base-14bf3.cloudfunctions.net/uploadImageToBase", json={
            "imageBase64": b64_image,
            "prompt": prompt,
            "apiKey": api_key,
        }, timeout=30)

        print("Upload response code:", response.status_code)

        return (image[0],)
