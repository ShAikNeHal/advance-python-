import cv2
import numpy as np

# Create a blank image (Height, Width, Channels)
image = np.ones((700, 500, 3), dtype=np.uint8) * 255

# 7 shades of Orange (BGR format)
orange_shades = [
    (0, 69, 255),    # Dark Orange
    (0, 90, 255),
    (0, 110, 255),
    (0, 130, 255),
    (0, 150, 255),
    (0, 170, 255),
    (0, 200, 255)    # Light Orange
]

# Height of each shade
block_height = image.shape[0] // len(orange_shades)

# Draw stretched rectangles
for i, color in enumerate(orange_shades):
    y1 = i * block_height
    y2 = (i + 1) * block_height

    cv2.rectangle(
        image,
        (0, y1),                    # Start from left edge
        (image.shape[1], y2),       # Stretch to right edge
        color,
        -1                          # Filled rectangle
    )

# Display the image
cv2.imshow("7 Vertical Shades of Orange", image)

cv2.waitKey(0)
cv2.destroyAllWindows()
