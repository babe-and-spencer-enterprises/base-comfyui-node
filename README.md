# ComfyUI Upload to BASE Node

A custom [ComfyUI](https://github.com/comfyanonymous/ComfyUI) node that lets you upload generated images directly to your [BASE](https://getbase.app) account — no manual downloads or re-uploads needed.

---

## 🚀 Features

- Upload any image from a ComfyUI workflow to your BASE account
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

1. Log in at [getbase.app](https://getbase.app)
2. Go to **Settings → Integrations**
3. Click **Generate API Key**
4. Copy and paste this key into the `api_key` input of the node in ComfyUI

This key securely links your uploads to your BASE account.

---

## 🛠️ Node Inputs

| Input       | Description                                                                                                      |
|-------------|------------------------------------------------------------------------------------------------------------------|
| `image`     | The generated image to upload (connect from a `VAEDecode` node)                                                 |
| `api_key`   | Your personal BASE API key (see below)                                                                          |
| `folder_id` | (Optional) The ID of a folder in your BASE account to store the image under. Right-click a folder in BASE to copy its ID. |

---

## 📦 Node Behavior

This is an output node in ComfyUI. It performs an upload as a side effect and does not return any value to the graph.

---

## 💡 Example Workflow

Place this node at the end of your workflow as an output node. Connect the generated image (typically from a `VAEDecode` node), provide your BASE API key and (optionally) a folder ID. The node will upload the image to your BASE account as a side effect; it does not return any value to the graph.

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
