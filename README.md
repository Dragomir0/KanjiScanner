# KanjiScanner: Real-Time Japanese OCR & Texthooker

OCR tool designed for real-time scanning of Japanese text. 

Uses your camera to capture and extract Japanese characters and copies them to the clipboard, allowing them to be read easily on a texthooker page with Yomichan for exmaple.

## Features

-  Automatically copies recognized text to clipboard to use to any Texthooker
-  Saves captured frames

---

## 📦 Requirements

- Python 3.10+
- A working webcam (preferably run on native Windows)

### 🧪 Python Dependencies

Install via pip:

```bash
pip install opencv-python 
pip install -r requirements.txt
python main.py
```

## Notes

Make sure your camera works in your current environment as WSL2 does not support direct camera usage.

## Thanks

This work would not have been possible without amazing open source AI work:
- [Surya OCR](https://github.com/VikParuchuri/surya) 
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

