import cv2
import numpy as np

# Start webcam
cap = cv2.VideoCapture(0)

# Drawing variables
drawing = False
last_x, last_y = -1, -1

# Drawing canvas
canvas = None


# Mouse function
def draw(event, x, y, flags, param):
    global drawing, last_x, last_y, canvas

    # Start drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        last_x, last_y = x, y

    # Draw while moving mouse
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.line(
                canvas,
                (last_x, last_y),
                (x, y),
                (0, 0, 255),
                4
            )

            last_x, last_y = x, y

    # Stop drawing
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        last_x, last_y = -1, -1


cv2.namedWindow("Webcam Drawing")
cv2.setMouseCallback("Webcam Drawing", draw)


while True:

    ret, frame = cap.read()

    if not ret:
        print("Cannot access webcam")
        break

    # Flip webcam
    frame = cv2.flip(frame, 1)

    # Create canvas once
    if canvas is None:
        canvas = np.zeros_like(frame)

    # Combine webcam and drawing
    result = cv2.add(frame, canvas)

    cv2.imshow("Webcam Drawing", result)

    key = cv2.waitKey(1) & 0xFF

    # Press C to clear drawing
    if key == ord('c'):
        canvas = np.zeros_like(frame)

    # Press Q to quit
    elif key == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
