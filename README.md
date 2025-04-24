# 🖼️ Interactive Image Enhancer CLI

This is a simple yet powerful Python CLI tool for enhancing images interactively. It supports contrast, brightness, color saturation, sharpening, and several simulated exposure effects with live preview and adjustable settings.

---

## 📂 Folder Structure

project/ ├── imgs/ # Place your input images here ├── adjustedImgs/ # Temporarily adjusted images (auto-generated) ├── editedImgs/ # Final saved images after user confirmation ├── cached_image.jpg # Cache for preview image ├── enhancer.py # Main Python script


---

## 🔧 Features

- Interactive CLI with user-friendly prompts
- Fine-tune parameters like contrast, brightness, color saturation, and sharpness
- Simulated image effects:
  - Exposure
  - Shadows
  - Highlights
  - Black Point
- Real-time image preview before saving
- Color-coded terminal interface using `colorama`

---

## 📦 Requirements

Install dependencies using pip:

```bash
pip install pillow numpy colorama
```

🚀 Usage
Place your images inside the imgs/ folder.

Run the script:

bash
Copy
Edit
python enhancer.py
Follow the interactive prompts to adjust the image.

After preview, choose to:

✅ Save (y)

🔁 Retry (n)

❌ Quit (q)

🔍 Parameter Descriptions
Contrast: Boost shadows and highlights.

Brightness: Overall lightness.

Saturation: Color vividness.

Sharpness Strength: How strong to sharpen edges.

Sharpness Radius: Area affected around each edge pixel.

Sharpness Threshold: Skip sharpening areas below a contrast threshold.

Exposure: Adds artificial light (not true exposure).

Shadows: Brighten dark regions.

Highlights: Dim overly bright regions.

Black Point: Deepen dark tones.

📝 Notes
Press Enter to use default values.

Enter 'q' at any prompt to quit immediately.

Only standard image formats are supported: .jpg, .jpeg, .png, .bmp, .tif, .tiff.

📸 Sample Workflow

🎨 === Processing: sunset.jpg ===

📸 Let's fine-tune your image!
🛠️  Parameters explained:
• Contrast: ...
• Brightness: ...
...

Contrast [1.0]:
Brightness [1.0]: 1.2
...
💬 Are you satisfied with the result? (y = save, n = retry, q = quit):

🧼 Cleanup
Temporary images in adjustedImgs/ are deleted automatically if not saved. Final images are moved to editedImgs/.
