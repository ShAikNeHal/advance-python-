import cv2
import numpy as np

# Create a white canvas
img = np.ones((600, 800, 3), dtype=np.uint8) * 255

drawing = False
start_x, start_y = -1, -1

# Mouse callback function
def draw_rectangle(event, x, y, flags, param):
    global start_x, start_y, drawing, img

    # Left mouse button pressed
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_x, start_y = x, y

    # Mouse movement while button is pressed
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            temp = img.copy()
            cv2.rectangle(temp, (start_x, start_y), (x, y), (0, 0, 255), 2)
            cv2.imshow("Draw Rectangle", temp)

    # Left mouse button released
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img, (start_x, start_y), (x, y), (0, 0, 255), 2)
        cv2.imshow("Draw Rectangle", img)

# Create window
cv2.namedWindow("Draw Rectangle")

# Set mouse callback
cv2.setMouseCallback("Draw Rectangle", draw_rectangle)

# Display loop
while True:
    cv2.imshow("Draw Rectangle", img)

    key = cv2.waitKey(1) & 0xFF

    # Press ESC to exit
    if key == 27:
        break

cv2.destroyAllWindows()
