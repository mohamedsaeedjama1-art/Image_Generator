# 🎨 Pollinations AI Image Generator

## 1. Introduction

A simple Python desktop app that generates images from text prompts using the Pollinations AI API. Enter a description, choose the image size, generate, preview, and save your image.

## 2. How It Works

1. Enter a description of the image you want.
2. Select the image width and height.
3. Click **Generate Image**.
4. The app sends your prompt to the Pollinations API.
5. The generated image appears in the preview area.
6. Click **Save Image** to save it to your computer.

## 3. Technologies

- **Python** – main programming language
- **Tkinter** – desktop user interface
- **Pillow** – image processing and preview
- **Requests** – sends requests to the API
- **Pollinations API** – generates images from prompts
- **Threading** – keeps the interface responsive during generation

## 4. Install Requirements

Make sure Python is installed, then open your terminal in the project folder and run:

```bash
python -m pip install pillow requests
```

Tkinter is included with many Python installations. If it is missing on your system, install it using your operating system's package manager.

To start the app:

```bash
python main.py
```

> If your Python file has a different name, replace `main.py` with that filename.
