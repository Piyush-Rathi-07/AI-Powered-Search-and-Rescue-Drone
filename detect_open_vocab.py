import cv2
import torch
from ultralytics import YOLO
from relsgg import RelateAnything


# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

VIDEO_SOURCE = "test10.mp4"   # Change to 0 for webcam

YOLO_MODEL = "yolov8n.pt"

# Relations we want RelateAnything to look for
RELATIONS = [
    "near",
    "far from",
    "above",
    "below",
    "behind",
    "in front of",
    "next to",
    "holding",
    "riding",
    "wearing",
]


# --------------------------------------------------
# DEVICE
# --------------------------------------------------

device = "cuda" if torch.cuda.is_available() else "cpu"

print("Using device:", device)

if device == "cuda":
    print("GPU:", torch.cuda.get_device_name(0))


# --------------------------------------------------
# LOAD YOLO
# --------------------------------------------------

print("Loading YOLO...")

detector = YOLO(YOLO_MODEL)

print("YOLO loaded.")


# --------------------------------------------------
# LOAD RELATEANYTHING
# --------------------------------------------------

print("Loading RelateAnything...")

model = RelateAnything.from_pretrained(
    "maelic/relsgg-vits16plus",
    device=device
)

model.set_vocabulary(RELATIONS)

print("RelateAnything loaded.")


# --------------------------------------------------
# OPEN VIDEO / WEBCAM
# --------------------------------------------------

cap = cv2.VideoCapture(VIDEO_SOURCE)

if not cap.isOpened():
    print("ERROR: Could not open video source.")
    exit()


# --------------------------------------------------
# VIDEO LOOP
# --------------------------------------------------

while True:

    ret, frame = cap.read()

    if not ret:
        print("Video ended.")
        break

    # ----------------------------------------------
    # YOLO DETECTION
    # ----------------------------------------------

    results = detector(
        frame,
        device=0 if device == "cuda" else "cpu",
        verbose=False
    )

    boxes = []
    labels = []

    for result in results:

        for box in result.boxes:

            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

            confidence = float(box.conf[0])
            class_id = int(box.cls[0])

            if confidence < 0.4:
                continue

            boxes.append([
                float(x1),
                float(y1),
                float(x2),
                float(y2)
            ])

            labels.append(
                detector.names[class_id]
            )

            # Draw YOLO box
            cv2.rectangle(
                frame,
                (int(x1), int(y1)),
                (int(x2), int(y2)),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"{detector.names[class_id]} {confidence:.2f}",
                (int(x1), int(y1) - 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )


    # ----------------------------------------------
    # RELATEANYTHING
    # ----------------------------------------------

    if len(boxes) >= 2:

        try:

            triplets = model.predict(
                frame,
                boxes,
                topk=10
            )

            # Display relations
            y_position = 30

            for triplet in triplets:

                print(triplet)

                cv2.putText(
                    frame,
                    str(triplet),
                    (10, y_position),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    1
                )

                y_position += 20

        except Exception as e:

            print("RelateAnything error:", e)


    # ----------------------------------------------
    # DISPLAY
    # ----------------------------------------------

    cv2.imshow(
        "YOLO + RelateAnything",
        frame
    )


    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# --------------------------------------------------
# CLEANUP
# --------------------------------------------------

cap.release()
cv2.destroyAllWindows()
