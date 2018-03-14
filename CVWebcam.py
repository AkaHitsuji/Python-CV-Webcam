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
    #extracting contours, we create a copy of thresh as findContours edits the image directly
    contours, hierachy, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        #get approximate polygons
        approx = cv2.approxPolyDP(c, 0.01*cv2.arcLength(c,True),True)

        if len(approx) == 3:
            shape_name = "Triangle"
            cv2.drawContours(image,[c],0,(0,255,0),-1)
            M = cv2.moments(c)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            #-50 to bring text to center
            cv2.putText(image, shape_name, (cx-50, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
        elif len(approx) == 4:
            x,y,w,h = cv2.boundingRect(c)
            M = cv2.moments(c)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            # Check to see if 4-side polygon is square or rectangle
            # cv2.boundingRect returns the top left and then width and
            if abs(w-h) <= 3:
                shape_name = "Square"

                # Find contour center to place text at the center
                cv2.drawContours(image, [c], 0, (0, 125 ,255), -1)
                cv2.putText(image, shape_name, (cx-50, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
            else:
                shape_name = "Rectangle"

                # Find contour center to place text at the center
                cv2.drawContours(image, [c], 0, (0, 0, 255), -1)
                M = cv2.moments(cnt)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                cv2.putText(image, shape_name, (cx-50, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
        elif len(approx) >= 15:
            shape_name = "Circle"
            cv2.drawContours(image, [c], 0, (0, 255, 255), -1)
            M = cv2.moments(c)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.putText(image, shape_name, (cx-50, cy), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)

    return image

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
