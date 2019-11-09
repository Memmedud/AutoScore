import sys
import cv2 as cv
import numpy as np

def sjekk_bilde(src):
    
    if src is None:                                               # Check if image is loaded fine
        print ('Error opening image!')
        print ('Usage: hough_circle.py [image_name -- default ' + default_file + '] \n')
        return -1

def stor_sirkel(src):
    gray1 = cv.cvtColor(src, cv.COLOR_BGR2GRAY)                       # Image gray
    gray = cv.medianBlur(gray1, 5)
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, gray.shape[0] / 4,
                           param1=200, param2=100,
                           minRadius=200, maxRadius=768)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])                       
            cv.circle(src, center, 5, (0, 100, 100), 2)              # circle center
            radius = i[2]
            print(radius)
            cv.circle(src, center, radius + 300, (255, 0, 255), 600) # circle outline
            src = src[center[1] - radius:center[1] + radius, center[0] - radius:center[0] + radius]
            break
        circles = []
        
    #Skaler ned bilde:
    src = cv.resize(src, (500, 500), interpolation = cv.INTER_AREA)
    cv.imshow("detected circles", src)
    #cv.imwrite("final.jpeg", src)
    #cv.waitKey(0)

    return src
