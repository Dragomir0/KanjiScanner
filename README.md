# KanjiScanner: Real-Time Japanese OCR

OCR tool designed for real-time scanning of Japanese text. 

Using your camera to capture and extract Japanese characters, copying them and displaying them on a easy to read page, enabling popup dictionary use for japanese learners.

## 🎬 Demo workflow

https://github.com/user-attachments/assets/b595812e-1d5a-4ce8-a97c-39d05fc9e1ba

## 📦 Requirements

- Python 3.10+

## ⚙️ Recommended addons

- [Yomitan](https://github.com/yomidevs/yomitan) to use as a interactive popup dictionary
- [Clipboard Inserter](https://chromewebstore.google.com/detail/clipboard-inserter/deahejllghicakhplliloeheabddjajm?hl=en-US) for automatic text pasting to the texthooker
- [Texthooking page](https://anacreondjt.gitlab.io/texthooker.html) or use the included texthooker.html for offline use

### Installation

#### For Windows

1. **Clone** or download the project, then open PowerShell in that folder.  
2. Run the `run.bat` which installs the virtual environment, dependencies and starts the scanner.
3. Open the `texthooker.html` if necessary for scanned text output and enable the clipboard inserter.

#### For Linux

1. **Clone** or download the project, then open a terminal in that folder.  
2. **Install** using make:
```bash
make install  
make run       
```
3. Open the `texthooker.html` if necessary for scanned text output and enable the clipboard inserter.

## Thanks

This work would not have been possible without amazing open source AI work:
- [Surya OCR](https://github.com/VikParuchuri/surya) 
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
