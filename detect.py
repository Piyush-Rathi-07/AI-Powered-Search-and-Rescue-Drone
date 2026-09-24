import cv2
import time
import subprocess
import os
from ultralytics import YOLO


# ==========================================
# MODEL
# ==========================================
model = YOLO("yolov8m.pt")


# ==========================================
# VIDEO INPUT
# ==========================================
cap = cv2.VideoCapture("videos/test8.mp4")
#cap = cv2.VideoCapture(0)


# ==========================================
# GET VIDEO PROPERTIES
# ==========================================
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
input_fps = cap.get(cv2.CAP_PROP_FPS)

print("Resolution:", width, "x", height)
print("Input FPS:", input_fps)


# ==========================================
# OUTPUT FILES
# ==========================================
temp_output = "output/output.mp4"
final_output = "output/whatsapp.mp4"

os.makedirs("output", exist_ok=True)


# ==========================================
# VIDEO WRITER
# ==========================================
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

out = cv2.VideoWriter(
    temp_output,
    fourcc,
    input_fps,
    (width, height)
)


# ==========================================
# COCO CLASS IDs
# ==========================================
PERSON = 0
CAR = 2
MOTORBIKE = 3
BUS = 5
TRUCK = 7

allowed_classes = [
    PERSON,
    CAR,
    MOTORBIKE,
    BUS,
    TRUCK
]


# ==========================================
# CLASS NAMES
# ==========================================
class_names = {
    PERSON: "Person",
    CAR: "Car",
    MOTORBIKE: "Motorbike",
    BUS: "Bus",
    TRUCK: "Truck"
}


# ==========================================
# FPS
# ==========================================
prev_time = time.time()


# ==========================================
# PROCESS VIDEO
# ==========================================
while True:

    ret, frame = cap.read()

    if not ret:
        break


    # ======================================
    # YOLO DETECTION + TRACKING
    # ======================================
    results = model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        device=0,
        imgsz=960,
        conf=0.25,
        verbose=False
    )


    # ======================================
    # START WITH ORIGINAL FRAME
    # ======================================
    annotated = frame.copy()


    # ======================================
    # DRAW THIN DETECTION BOXES
    # ======================================
    if results[0].boxes.id is not None:

        boxes = results[0].boxes.xyxy.cpu().numpy()
        ids = results[0].boxes.id.cpu().numpy().astype(int)
        classes = results[0].boxes.cls.cpu().numpy().astype(int)
        confidences = results[0].boxes.conf.cpu().numpy()


        for box, track_id, cls, confidence in zip(
            boxes,
            ids,
            classes,
            confidences
        ):

            # Ignore unwanted objects
            if cls not in allowed_classes:
                continue


            # Coordinates
            x1, y1, x2, y2 = map(int, box)


            # ==================================
            # THIN BOUNDING BOX
            # ==================================
            cv2.rectangle(
                annotated,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                1
            )


            # ==================================
            # CENTER POINT
            # ==================================
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            cv2.circle(
                annotated,
                (cx, cy),
                4,
                (255, 0, 0),
                -1
            )


            # ==================================
            # OBJECT NAME + TRACK ID
            # ==================================
            object_name = class_names[cls]

            label = f"{object_name} ID:{track_id}"


            # ==================================
            # LABEL
            # ==================================
            cv2.putText(
                annotated,
                label,
                (x1, max(y1 - 7, 15)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1
            )


    # ======================================
    # CALCULATE PROCESSING FPS
    # ======================================
    current_time = time.time()

    fps = 1 / (current_time - prev_time)

    prev_time = current_time


    # ======================================
    # DISPLAY FPS
    # ======================================
    cv2.putText(
        annotated,
        f"FPS: {int(fps)}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )


    # ======================================
    # SAVE FRAME
    # ======================================
    out.write(annotated)


    # ======================================
    # DISPLAY VIDEO
    # ======================================
    cv2.imshow(
        "Real-Time Object Detection & Tracking",
        annotated
    )


    # ESC TO EXIT
    if cv2.waitKey(1) & 0xFF == 27:
        break


# ==========================================
# RELEASE
# ==========================================
cap.release()
out.release()
cv2.destroyAllWindows()


print("\nYOLO processing completed.")
print("Converting video for WhatsApp...")


# ==========================================
# FFMPEG CONVERSION
# ==========================================
ffmpeg_command = [
    "ffmpeg",
    "-y",

    "-i", temp_output,

    # H.264 video
    "-c:v", "libx264",

    # WhatsApp-compatible pixel format
    "-pix_fmt", "yuv420p",

    # AAC audio
    "-c:a", "aac",

    # Fast start
    "-movflags", "+faststart",

    final_output
]


try:

    subprocess.run(
        ffmpeg_command,
        check=True
    )


    print("\n===================================")
    print("VIDEO READY!")
    print("===================================")
    print("WhatsApp video:")
    print(final_output)
    print("===================================")


    # Delete temporary file
    os.remove(temp_output)

    print("Temporary file deleted.")


except FileNotFoundError:

    print("\n===================================")
    print("ERROR: FFmpeg not found!")
    print("===================================")
    print("Install FFmpeg and add it to PATH.")

    print("\nYour YOLO output is still available at:")
    print(temp_output)


except subprocess.CalledProcessError:

    print("\nFFmpeg conversion failed.")

    print("Your original output is available at:")
    print(temp_output)
