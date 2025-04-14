import cv2
import numpy as np

# Constants
WINDOW_NAME = "Select 4 Points"
VIDEO_PATH = "yolov8_car_parking\\output_video.mp4"  # Change this to your actual video path

# Variables to store state
all_polygons = []
current_polygon = []
num_polygons = 0
polygon_index = 0

def mouse_callback(event, x, y, flags, param):
    global current_polygon, all_polygons, polygon_index, frame_copy

    if event == cv2.EVENT_LBUTTONDOWN:
        current_polygon.append((x, y))
        print(f"Polygon {polygon_index+1} - Point {len(current_polygon)}: ({x}, {y})")

        if len(current_polygon) > 1:
            cv2.line(frame_copy, current_polygon[-2], current_polygon[-1], (0, 255, 0), 2)

        if len(current_polygon) == 4:
            cv2.line(frame_copy, current_polygon[3], current_polygon[0], (0, 255, 0), 2)
            cv2.polylines(frame_copy, [np.array(current_polygon, np.int32)], True, (255, 255, 0), 2)

            for i, pt in enumerate(current_polygon):
                cv2.putText(frame_copy, f'{i+1}', pt, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

            all_polygons.append(current_polygon.copy())
            current_polygon.clear()
            polygon_index += 1

            print(f"Polygon no. {polygon_index} completed!\n")

            if polygon_index < num_polygons:
                print(f"select points for Polygon{polygon_index+1}-")
            else:
                print("\nAll selected. Press any key to exit")
                cv2.imshow(WINDOW_NAME, frame_copy)

    cv2.imshow(WINDOW_NAME, frame_copy)


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

num_polygons = int(input("How many parking spaces you want to select? "))
print(f"You will be selecting {num_polygons} rect with 4 points each\n")
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
ret, frame = cap.read()
cap.release()
if not ret:
    print("❌ Couldn't read the selected frame.")
    exit()
frame = cv2.resize(frame, (1020, 500))
frame_copy = frame.copy()
cv2.namedWindow(WINDOW_NAME)
cv2.setMouseCallback(WINDOW_NAME, mouse_callback)
print(f"🖱️ Click 4 points for polygon no.{polygon_index+1}...")
cv2.imshow(WINDOW_NAME, frame_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()
print("\nAll coordinates:")
for i, polygon in enumerate(all_polygons):
    print(f"area{i+1}= {polygon}")
