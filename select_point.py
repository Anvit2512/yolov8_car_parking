import cv2
import numpy as np

# Constants
WINDOW_NAME = "Select 4 Points"
VIDEO_PATH = "output_video.mp4"  # Change this to your actual video path

# Variables to store state
points = []

def mouse_callback(event, x, y, flags, param):
    global points, frame

    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"Point {len(points)}: ({x}, {y})")

        if len(points) > 1:
            cv2.line(frame, points[-2], points[-1], (0, 255, 0), 2)

        if len(points) == 4:
            cv2.line(frame, points[3], points[0], (0, 255, 0), 2)
            cv2.polylines(frame, [np.array(points, np.int32)], True, (255, 255, 0), 2)

            print("\nAll 4 Coordinates:")
            for i, pt in enumerate(points):
                print(f"Point {i+1}: {pt}")
                cv2.putText(frame, str(i+1), pt, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    cv2.imshow(WINDOW_NAME, frame)

# Load the video
cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("❌ Error opening video.")
    exit()

# Ask for frame number
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(f"Total frames in video: {total_frames}")
frame_number = int(input("Enter frame number to capture: "))

if frame_number >= total_frames:
    print("❌ Frame number exceeds total frames.")
    cap.release()
    exit()

# Set the frame position and read it
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
ret, frame = cap.read()

if not ret:
    print("❌ Couldn't read the selected frame.")
    cap.release()
    exit()

# Resize the frame to match YOLO detection
frame = cv2.resize(frame, (1020, 500))

cv2.namedWindow(WINDOW_NAME)
cv2.setMouseCallback(WINDOW_NAME, mouse_callback)

print("🖱️ Click 4 points on the frame...")

cv2.imshow(WINDOW_NAME, frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
cap.release()
