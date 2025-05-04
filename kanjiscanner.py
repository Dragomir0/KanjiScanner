import re
from PIL import Image
from surya.recognition import RecognitionPredictor
from surya.detection import DetectionPredictor
import time
import cv2
import pyperclip
import os
from datetime import datetime

# TODO: Correct invalid camera indices printed by OpenCV's internal C++ backend
def list_available_cameras(max_index=3):
    available_cameras = []
    for index in range(max_index):
        cap = cv2.VideoCapture(index)
        if cap is None or not cap.isOpened():
            cap.release()
            continue
        available_cameras.append(index)
        cap.release()
    return available_cameras
    
# Append only japanese: Hiragana (\u3040–\u309F), Katakana (\u30A0–\u30FF) ,Kanji (\u4E00–\u9FFF)
def extract_japanese(text):
    return "".join(re.findall(r'[\u3040-\u30FF\u4E00-\u9FFF]+', text))

def sorted_vertical_lines(text_lines):
    """
    Sort lines for vertical text order by using bbox attribute:
    bbox is (x1,y1,x2,y2): -x1 = left edge, y1 = top edge
    -x1 = rightmost columns first
    y1  = top lines before lower ones
    """
    buckets = []
    for tl in text_lines:
        txt = tl.text.strip()
        if not txt:
            continue

        # use bbox coordinates to sort
        x1, y1, x2, y2 = tl.bbox
        buckets.append((x1, y1, txt))

    # sort by (-x1, y1)
    buckets.sort(key=lambda it: (-it[0], it[1]))
    # extract only the text in order
    return [t for _, _, t in buckets]

def is_vertical(text_lines):
    """
    Each line, width = x2-x1, height = y2-y1
    height > width = always vertical reading!
    """
    v_count = 0
    h_count = 0

    for tl in text_lines:
        x1, y1, x2, y2 = tl.bbox
        width = x2 - x1
        height = y2 - y1
        if height > width:
            v_count += 1
        else:
            h_count += 1

    # return True if more vertical boxes
    return v_count > h_count

if __name__ == "__main__":
    # Load models
    rec = RecognitionPredictor()
    det = DetectionPredictor()

    # Prompt user for camera choice
    cameras = list_available_cameras()
    print("📷Input the number of the camera you want to use below:")
    if cameras:
        for cam in cameras:
            print(f"  -> Camera {cam}")
    else:
        print("🔴 No camera detected!")
        exit()
    cameraPort = int(input())

    # Start camera capture based on chosen video input source
    cap = cv2.VideoCapture(cameraPort)
    if not cap.isOpened():
        print("🔴 Failed to open camera")
        exit()

    try:
        while True:
            print("⭐ Starting OCR...")
            ret, frame = cap.read()
            if not ret:
                print("🔴 Frame capture failed.")
                break

            # Convert OpenCV BGR to PIL RGB format, without it the colors are inverted!
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            # Run detection
            preds = rec([image], [["ja"]], det)
            lines = preds[0].text_lines  # list of TextLine objects

            # Detect vertical orientation, by default lines ordered horizontally
            if is_vertical(lines):
                ordered = sorted_vertical_lines(lines)
                print("🟢 Detected: Vertical text")
            else:
                ordered = [tl.text for tl in lines]
                print("🟢 Detected: Horizontal text")

            # Strip only japanese for output
            clean = [
                extract_japanese(txt.strip())
                for txt in ordered
                if txt.strip()
            ]
            print("\n".join(clean))
            
            # Copy to clipboard for easier scanning
            if clean:
                text_to_copy = "\n".join(clean)
                pyperclip.copy(text_to_copy)
                print("📋 Text copied to clipboard!")
            
            # Save scanned frame + create output folder if needed 
            os.makedirs("scans", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scans/scan_{timestamp}.png"
            cv2.imwrite(filename, frame)
            print(f"🖼️ Saved scan as: {filename}")

            # Time until next capture
            time.sleep(5)

    except KeyboardInterrupt:
        print("🔴 Interrupted manually")

    finally:
        cap.release()