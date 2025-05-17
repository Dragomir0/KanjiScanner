import re
import os
import cv2
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
from surya.recognition import RecognitionPredictor
from surya.detection import DetectionPredictor
import pyperclip
from datetime import datetime

# TODO: Correct invalid camera indices printed by OpenCV's internal C++ backend
def list_available_cameras(max_choices=5):
    available_cameras = []
    for index in range(max_choices):
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

# Determine orientation
def is_vertical(text_lines) -> bool:
    v_count = h_count = 0
    for tl in text_lines:
        x1, y1, x2, y2 = tl.bbox
        if (y2 - y1) > (x2 - x1):
            v_count += 1
        else:
            h_count += 1
    return v_count > h_count

# Sort vertical lines right-to-left, top-to-bottom
def sorted_vertical_lines(text_lines):
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
    # extracts just the text from each tuple without coordinates
    texts = []
    for x1, y1, txt in buckets:
        texts.append(txt)
    return texts

class KanjiScannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("KanjiScanner GUI")
        self.geometry("900x800")

        # Load models
        self.rec = RecognitionPredictor()
        self.det = DetectionPredictor()

        # Camera selection and capture frequency frame
        self.top_controls = ctk.CTkFrame(self, fg_color="transparent")
        # Centered horizontally
        self.top_controls.pack(pady=10, anchor="n")

        # Camera input choice
        cam_values = [str(c) for c in list_available_cameras()] or ["None"]
        self.camera_label = ctk.CTkLabel( self.top_controls, text="Camera Input")
        self.camera_label.pack(side="left", padx=10)
        self.camera_menu = ctk.CTkOptionMenu( self.top_controls, values=cam_values, command=self.set_camera )
        self.camera_menu.pack(side="left", padx=10)

        # Camera Capture frequency choice
        self.freq_label = ctk.CTkLabel( self.top_controls, text="Scan frequency (sec)")
        self.freq_label.pack(side="left", padx=10)
        self.frequency_slider = ctk.CTkSlider(self.top_controls, from_=1, to=10, number_of_steps=9, command=self.freq_change)
        self.frequency_slider.set(5)      # slider default
        self.scan_interval = 5
        self.frequency_slider.pack(side="left", padx=10)

        # Start and Stop buttons
        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(pady=5)
        self.start_btn = ctk.CTkButton(self.btn_frame, text="Start", command=self.start_scanning)
        self.start_btn.grid(row=0, column=0, padx=5)
        self.stop_btn = ctk.CTkButton(self.btn_frame, text="Stop", command=self.stop_scanning, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=5)

        # Video camera display
        self.video_label = ctk.CTkLabel(self, text="Scanned camera feed will appear here")
        self.video_label.pack(pady=10)

        # Output
        self.text_box = ctk.CTkTextbox(self, width=800, height=300)
        self.text_box.pack(pady=10)

        self.cap = None
        self.running = False
        self.camera_port = int(cam_values[0]) if cam_values[0] != "None" else None
    
    def freq_change(self, raw_val):
        self.scan_interval = int(raw_val)

    def set_camera(self, val):
        try:
            self.camera_port = int(val)
        except ValueError:
            self.camera_port = None

    def start_scanning(self):
        if self.camera_port is None:
            return
        self.cap = cv2.VideoCapture(self.camera_port)
        if not self.cap.isOpened():
            ctk.CTkLabel(self, text="🔴 Failed to open camera").pack()
            return
        self.running = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.scan_loop()

    def stop_scanning(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")

    def scan_loop(self):
        if not self.running:
            return
        ret, frame = self.cap.read()
        if ret:
            # Display scanned camera frame
            # Convert OpenCV BGR to PIL RGB format, without it the colors are inverted!
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            w, h = image.width, image.height
            ctk_img = CTkImage(light_image=image, dark_image=image, size=(w, h))

            self.video_label.configure(image=ctk_img)
            self.video_label.image = ctk_img

            # Perform OCR with japanese configuration
            preds = self.rec([image], ["ocr_without_boxes"], self.det)
            lines = preds[0].text_lines

            # Detect vertical orientation, by default lines ordered horizontally
            if is_vertical(lines):
                ordered = sorted_vertical_lines(lines)
                print("🟢 Detected: Vertical text")
            else:
                ordered = [tl.text for tl in lines]
                print("🟢 Detected: Horizontal text")
            
            # Strip only japanese for output
            clean = [extract_japanese(txt) for txt in ordered if txt.strip()]
            text_out = "\n".join(clean)
            self.text_box.delete("0.0", ctk.END)
            self.text_box.insert("0.0", text_out)
            
            # Copy to clipboard for reading
            if text_out:
                pyperclip.copy(text_out)

            # Save frame + create output folder if needed 
            os.makedirs("scans", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            cv2.imwrite(f"scans/scan_{timestamp}.png", frame)

        # Repeat based on chosen frequency
        delay_ms = self.scan_interval * 1000
        self.after(delay_ms, self.scan_loop)

if __name__ == "__main__":
    ctk.set_appearance_mode("System")  
    ctk.set_default_color_theme("blue")
    app = KanjiScannerApp()
    app.mainloop()