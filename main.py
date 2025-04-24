import re
from PIL import Image
from surya.recognition import RecognitionPredictor
from surya.detection import DetectionPredictor

import time
import cv2
import pyperclip

# Matches Hiragana (\u3040–\u309F), Katakana (\u30A0–\u30FF), Kanji (\u4E00–\u9FFF)
def extract_japanese(text):
    return "".join(re.findall(r'[\u3040-\u30FF\u4E00-\u9FFF]+', text))

if __name__ == "__main__":
    
    # Load models
    recognition_predictor = RecognitionPredictor()
    detection_predictor = DetectionPredictor()

    # Start webcam capture
    cap = cv2.VideoCapture(3)
    if not cap.isOpened():
        print("❌ Failed to open webcam.")
        exit()

    print("📸 Starting OCR loop...")

    # Webcam capture loop
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Frame capture failed.")
                break

            # Convert OpenCV BGR to PIL RGB format
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            # Run OCR
            predictions = recognition_predictor([image], [["ja"]], detection_predictor)

            # Extract and print clean Japanese text
            text_lines = predictions[0].text_lines
            clean_text = [extract_japanese(t.text) for t in text_lines if t.text.strip()]
            print("OCR Output:")
            for line in clean_text:
                print(line)
            
            # Copy to clipboard for translation scanning
            if clean_text:
                text_to_copy = "\n".join(clean_text)
                pyperclip.copy(text_to_copy)
                print("📋 Text copied to clipboard!")
            
            # Time until next capture
            time.sleep(5)

    except KeyboardInterrupt:
        print("⛔ Interrupted manually.")

    finally:
        cap.release()
        cv2.destroyAllWindows()

    # Image Processing: 
    # image = Image.open("samples/kanji2.png")

    # # Load models
    # recognition_predictor = RecognitionPredictor()
    # detection_predictor = DetectionPredictor()

    # # Run OCR
    # predictions = recognition_predictor([image], [["ja"]], detection_predictor)

    # # Extract and clean text
    # text_lines = predictions[0].text_lines
    # clean_text = [extract_japanese(t.text) for t in text_lines if t.text.strip()]

    # # Print cleaned Japanese text only
    # print("".join(clean_text))