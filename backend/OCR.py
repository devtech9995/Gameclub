import pytesseract
import cv2

# Read the image
image = cv2.imread('image.jpg')
exit(0)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BpGR2GRAY)

# Apply thresholding to the image
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV)[1]

# Detect the contours in the image
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Extract the numbers from the image
numbers = []
for contour in contours:
    # Find the bounding box of the contour
    x, y, w, h = cv2.boundingRect(contour)

    # Crop the image to the bounding box
    cropped = thresh[y:y+h, x:x+w]

    # Recognize the number in the cropped image
    number = pytesseract.image_to_string(cropped)

    # Add the number to the list
    numbers.append(number)

# Print the recognized numbers
print(numbers)