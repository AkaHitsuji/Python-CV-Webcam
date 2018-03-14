import cv2
import numpy as np

#pencil sketch function
def sketchPencil(image):
    #grayscale the image for processing
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #blur the immage with Gaussian blur
    img_gray_blur = cv2.GaussianBlur(img_gray, (5,5), 0)
    #extract the edges
    canny_edges = cv2.Canny(img_gray_blur, 10, 70)
    #invert binarize the image
    ret, mask = cv2.threshold(canny_edges, 70, 255, cv2.THRESH_BINARY_INV)
    return mask

def sketchShapes(image):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img_gray,127,255,1)
    #extracting contours
    

# Initialize webcam, cap is the object provided by VideoCapture
# It contains a boolean indicating if it was sucessful (ret)
# It also contains the images collected from the webcam (frame)
cap = cv2.VideoCapture(0)

#no.1 = 49, no.2 = 50
selection = 1
while True:
    ret, frame = cap.read()
    if selection==1:
        cv2.imshow('Live Sketcher', sketchPencil(frame))
        k = cv2.waitKey(100)
        if k == 27: #27 = escape key
            break
        elif k==50:
            selection = 2
    elif selection==2:
        cv2.imshow('Live Sketcher', sketchShapes(frame))
        k = cv2.waitKey(1)
        if k == 27: #27 = escape key
            break
        elif k==49:
            selection = 1

# Release camera and close windows
cap.release()
cv2.destroyAllWindows()
