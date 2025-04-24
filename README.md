# 🈶 KanjiScanner: Real-Time Japanese OCR & Translation Assistant

KanjiScanner is a Python-based OCR tool designed for real-time scanning to recognize and scan physical Japanese text that might be hard to read otherwise

It uses any camera to capture and extract Japanese characters by implementing the Surya image OCR toolkit and adapting it to Japanese Text. 

---

## 🚀 Features

<!-- -  Configurable webcam capture steps -->
-  Automatically copies recognized text to clipboard to use to any Texthooker
-  Saving of captured frames

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

Make sure your camera works in your current environment as WSL2 does not support direct webcam usage.

## Thanks

This work would not have been possible without amazing open source AI work:
- [Surya OCR](https://github.com/VikParuchuri/surya) 
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

