import math
import cv2 as cv
import numpy as np

import FindColor as FC


def FindStones(Image):
    stones = []
    stonesimg = []
    stonesclr = []
    src = cv.resize(Image, (500, 500), interpolation = cv.INTER_AREA)
    gray = cv.cvtColor(src, cv.COLOR_BGR2HSV)
    lower_gray = np.array([0, 0, 50])
    upper_gray = np.array([200, 100, 160])
    mask1 = cv.inRange(gray, lower_gray, upper_gray)
    res1 = cv.bitwise_and(gray, gray, mask = mask1)
    res1 = cv.cvtColor(res1, cv.COLOR_HSV2RGB)
    res1 = cv.cvtColor(res1, cv.COLOR_RGB2GRAY)
    circles = cv.HoughCircles(res1, cv.HOUGH_GRADIENT, 1, 20,
                               param1=100, param2=20,
                               minRadius=10, maxRadius=30)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center, radius = (i[0], i[1]), i[2]

            stones.append(center)
            
            #Kutt ut alt som ikke er steinen og lag ett nytt bilde av det
            stone = src[center[1] - radius:center[1] + radius, center[0] - radius:center[0] + radius]
            height, width, depth = stone.shape
            mask1 = np.zeros((height, width), np.uint8)
            mask1 = cv.circle(mask1,(int(width/2),int(height/2)),int((width-10)/2),(255, 0, 255),-1)
            stone = cv.bitwise_and(stone, stone, mask = mask1)
            stonesimg.append(stone)
            stonesclr.append(FC.FindColor(stone, 2))

            cv.circle(src, center, 5, (0, 100, 100), 2)
            cv.circle(src, center, radius, (255, 0, 255), 2)
            cv.line(src, center, (250, 250), (255, 0, 255), 2)

    cv.imshow("detected circles", src)
    cv.imwrite("final.jpeg", src)
    cv.imshow("test", res1)
    #cv.imshow("hsv", gray)
    cv.imwrite("hsv.jpeg", res1)
    print(stonesclr)
    print(stones)
    liste = [list(a) for a in zip(FindDistance(stones), stonesclr)]
    SortStones(liste)
    #print(liste)
    #cv.waitKey(0)

    return(stones)

def FindDistance(stones):
    lengder = []
    for i in range(0, len(stones)):
        vektor = ([stones[i][0] - 250, stones[i][1] - 250])
        #3print(vektor)
        lengder.append(math.sqrt(vektor[0]**2 + vektor[1]**2))
    return(lengder)


#Stones = [[dist, team], ...]
def SortStones(stones):
    if len(stones) <= 1:
        MakeScores(stones)
        return(stones)
    sortedList = sorted(stones,key=lambda l:l[0], reverse=False)
    print(sortedList)
    MakeScores(sortedList)
    return(sortedList)

def MakeScores(stones):
    Scores = [0, 0]
    Scores[stones[0][1]-1] += 1
    for i in range(1, len(stones)):
        if stones[i][1] == stones[0][1]:
            Scores[(stones[0][1] - 1)] += 1
        else:
            break
    print(Scores)
