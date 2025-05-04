# KanjiScanner: Real-Time Japanese OCR

OCR tool designed for real-time scanning of Japanese text. 

Uses your camera to capture and extract Japanese characters, copying them to the clipboard which then allows them to be read easily on a texthooker page.

## 🎬 Demo workflow



## 📦 Requirements

- Python 3.10+
- A working camera

## ⚙️ Recommended workflow

- [Yomitan](https://github.com/yomidevs/yomitan)
- [Clipboard Inserter](https://chromewebstore.google.com/detail/clipboard-inserter/deahejllghicakhplliloeheabddjajm?hl=en-US) (for automatic text pasting to the texthooker)
- [Texthooking page](https://anacreondjt.gitlab.io/texthooker.html) or included texthooker.html for offline 

### Installation

#### For Windows

1. **Clone** or download the project, then open PowerShell in that folder.  
1. Run the `run.bat` which installs the virtual environment, dependencies and starts the scanner.
2. Open the `texthooker.html` if necessary for scanned text output.

#### For Linux

1. **Clone** or download the project, then open a terminal in that folder.  
2. **Install** using make:
```bash
make install  
make run       
```
3. Open the `texthooker.html` if necessary for scanned text output.

## Thanks

This work would not have been possible without amazing open source AI work:
- [Surya OCR](https://github.com/VikParuchuri/surya) 
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)