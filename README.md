# ComfyUI Upload to BASE Node

A custom [ComfyUI](https://github.com/comfyanonymous/ComfyUI) node that lets you upload generated images directly to your [BASE](https://getbase.app) account — no manual downloads or re-uploads needed.

---

## 🚀 Features

- Upload any image from a ComfyUI workflow to your BASE account
- Attach prompt metadata with the image
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

1. Log in at [getbase.app](https://getbase.app)
2. Go to **Settings → Integrations**
3. Click **Generate API Key**
4. Copy and paste this key into the `api_key` input of the node in ComfyUI

This key securely links your uploads to your BASE account.

---

## 🛠️ Node Inputs

| Input     | Description                                            |
|-----------|--------------------------------------------------------|
| `image`   | An image tensor (connect from a generation node)       |
| `prompt`  | (Optional) Prompt text used for generation             |
| `api_key` | Your personal BASE API key (see above)                 |

---

## 📦 Output

Returns a confirmation message from the BASE API — typically the uploaded image URL or an `Upload successful` message.

---

## 💡 Example Workflow

Include this node at the end of your generation pipeline to send the final image to BASE. You can optionally attach a prompt or label.

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
