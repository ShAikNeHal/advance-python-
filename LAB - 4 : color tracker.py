import cv2
import numpy as np

# Open webcam (0 = default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Flip for a mirror-like view
    frame = cv2.flip(frame, 1)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # HSV range for black color
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 60])

    # Create mask
    mask = cv2.inRange(hsv, lower_black, upper_black)

    # Remove small noise
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Largest contour
        largest = max(contours, key=cv2.contourArea)

        # Ignore tiny objects
        if cv2.contourArea(largest) > 500:
            x, y, w, h = cv2.boundingRect(largest)

            # Draw rectangle
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Find center
            cx = x + w // 2
            cy = y + h // 2

            # Draw center point
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            # Display coordinates
            cv2.putText(frame,
                        f"Center: ({cx}, {cy})",
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 0, 0),
                        2)

    # Show windows
    cv2.imshow("Live Tracking", frame)
    cv2.imshow("Black Mask", mask)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
