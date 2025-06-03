# ComfyUI Upload to BASE Node

A custom [ComfyUI](https://github.com/comfyanonymous/ComfyUI) node that lets you upload generated media directly to your [BASE](https://getbase.app) account — no manual downloads or re-uploads needed.

---

## 🚀 Features

- Upload static images, animated WebP sequences, or MP4 videos from a ComfyUI workflow to your BASE account
- Supports animated WebP generation from image sequences
- Supports direct upload of browser-compatible MP4 video files
- Optionally specify a folder ID to organize uploads
- Secure uploads via personal API key
- Streamlines creative workflow between ComfyUI and BASE

---

## 🧩 Installation

1. Clone this repo into your ComfyUI `custom_nodes/` directory:
   ```bash
   cd ComfyUI/custom_nodes/
   git clone https://github.com/babe-and-spencer-enterprises/base-comfyui-node.git
   ```

2. Restart ComfyUI.

3. The node will appear under the **BASE** category in the node menu as `Upload to BASE`.

---

## 🔐 Generate Your API Key

1. Log in at [go.getbase.app](https://go.getbase.app)
2. Go to **Settings → Integrations**
3. Click **Generate API Key**
4. Copy and paste this key into the `api_key` input of the node in ComfyUI

This key securely links your uploads to your BASE account.

---

## 🛠️ Node Inputs

| Input       | Description                                                                                                              |
|-------------|--------------------------------------------------------------------------------------------------------------------------|
| `image`     | The generated image to upload (connect from a `VAEDecode` node). Supports single image or list of images for animation.  |
| `video`     | (Optional) A video file to upload as browser-compatible MP4. Takes precedence over `image` if provided.                  |
| `fps`       | (Optional) Frame rate for animated WebP output (applies when uploading multiple images as animation).                    |
| `lossless`  | (Optional) Whether to save the animated WebP in lossless mode.                                                           |
| `quality`   | (Optional) Quality setting for animated WebP (0–100).                                                                    |
| `method`    | (Optional) Encoding method for animated WebP (`default`, `fastest`, or `slowest`).                                       |
| `api_key`   | Your personal BASE API key (see above).                                                                                  |
| `folder_id` | (Optional) The ID of a folder in your BASE account to store the image/video under. Right-click a folder in BASE to copy its ID. |

---

## 📦 Node Behavior

This is an output node in ComfyUI. It performs an upload as a side effect and does not return any value to the graph.

- If `video` is provided, the node uploads a browser-compatible MP4 video to your BASE account.
- If `image` is a list of multiple frames, the node generates and uploads an animated WebP file.
- Otherwise, a static PNG image is uploaded.

---

## 💡 Example Workflow

Place this node at the end of your workflow as an output node. Example use cases:

- **Static image upload:** Connect a single image (e.g., from `VAEDecode`) to `image` input to upload a PNG.
- **Animated image sequence:** Connect a list of images (frames) to `image` input and set `fps`/`quality`/`lossless`/`method` as desired to upload an animated WebP.
- **Video upload:** Connect a video file to the `video` input to upload it as an MP4.

Provide your BASE API key and (optionally) a folder ID. The node will upload the file to your BASE account as a side effect; it does not return any value to the graph.

---

## 📁 Repository Structure

```
base-comfyui-node/
├── base_upload_node.py   # The custom node logic
├── __init__.py           # Node registration
├── README.md             # This file
├── LICENSE               # MIT License
├── .gitignore            # Python-specific ignores
```

---

## 🤝 License

This project is licensed under the [MIT License](LICENSE). Use freely with attribution.
