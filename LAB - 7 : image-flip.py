import cv2

# Read the image
image = cv2.imread("D:/range-rover-velar-r-dynamic-luxury-suv-2020-5k-2560x1080-2817.jpeg")

# Flip the image
# 1 = horizontal flip
# 0 = vertical flip
# -1 = horizontal + vertical flip
flipped = cv2.flip(image, 1)

# Save the flipped image
cv2.imwrite("flipped.jpg", flipped)

# Display the images
cv2.imshow("Original Image", image)
cv2.imshow("Flipped Image", flipped)

cv2.waitKey(0)
cv2.destroyAllWindows()
