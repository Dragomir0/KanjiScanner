import re
from PIL import Image
from surya.recognition import RecognitionPredictor
from surya.detection import DetectionPredictor

import time
import cv2
import pyperclip
import os
from datetime import datetime

def extract_japanese(text):
    return "".join(re.findall(r'[\u3040-\u30FF\u4E00-\u9FFF]+', text))

# TODO: Correct invalid camera indices printed by OpenCV's internal C++ backend
def list_available_cameras(max_index=5):
    available_cameras = []
    for index in range(max_index):
        cap = cv2.VideoCapture(index)
        if cap is None or not cap.isOpened():
            cap.release()
            continue
        available_cameras.append(index)
        cap.release()
    return available_cameras

if __name__ == "__main__":    
    # Load models
    recognition_predictor = RecognitionPredictor()
    detection_predictor = DetectionPredictor()

    # Prompt user for camera choice
    cameras = list_available_cameras()
    print("Started Kanji Scanner, choose the input camera from the list below:")
    if cameras:
        print("📷 Available cameras found:")
        for cam in cameras:
            print(f"  -> Camera {cam}")
    else:
        print("❌ No camera detected")
    cameraPort = int(input())

    # Start camera capture based on chosen video input source
    cap = cv2.VideoCapture(cameraPort)
    if not cap.isOpened():
        print("❌ Failed to open camera")
        exit()
    print("📸 Starting OCR...")

    # Webcam capture loop
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Frame capture failed.")
                break

            # Convert OpenCV BGR to PIL RGB format, without it the colors are inverted!
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            # Run OCR with japanese text configuration
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
            
            # Create output folder and save scanned frames
            os.makedirs("scans", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scans/scan_{timestamp}.png"
            cv2.imwrite(filename, frame)
            print(f"🖼️ Saved scan as: {filename}")

            # Time until next capture
            time.sleep(3)

    except KeyboardInterrupt:
        print("⛔ Interrupted manually")

    finally:
        cap.release()
        cv2.destroyAllWindows()

    # Image Processing workflow: 
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