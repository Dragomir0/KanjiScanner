# KanjiScanner: Real-Time Japanese OCR & Texthooker

OCR tool designed for real-time scanning of Japanese text. 

Uses your camera to capture and extract Japanese characters, copying them to the clipboard which then allows them to be read easily on a texthooker page.

## 📦 Requirements

- Python 3.10+
- A working webcam (preferably run on native Windows)


## ⚙️ Recommended workflow

- [Yomitan](https://github.com/yomidevs/yomitan)
- [Texthooking page](https://anacreondjt.gitlab.io/texthooker.html)
- [Clipboard Inserter](https://chromewebstore.google.com/detail/clipboard-inserter/deahejllghicakhplliloeheabddjajm?hl=en-US) (for automatic text pasting to the texthooker)

### Installation

Install via pip in the project directory:

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