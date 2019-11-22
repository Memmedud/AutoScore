import numpy as np
import cv2 as cv
import Config
import Color

### Innholdsfortegnelse #####################################

    #FindBo
    #FindStones
    #FindDistance
    #SortStones
    #MakeScores

###########################################################    

def FindBo(src):
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)                       # Image gray
    gray = cv.medianBlur(gray, 5)
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, gray.shape[0] / 4,
                           param1=200, param2=100,
                           minRadius=200, maxRadius=768)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center, radius = (i[0], i[1]), i[2]                       
            cv.circle(src, center, 5, (0, 100, 100), 2)              # circle center
            cv.circle(src, center, radius + 300, (255, 0, 255), 600) # circle outline
            src = src[center[1] - radius:center[1] + radius, center[0] - radius:center[0] + radius]
            break
        src = cv.resize(src, (500, 500), interpolation = cv.INTER_AREA)
        #cv.imwrite("bo.jpeg", src)
        return src
    else:
        return -1

############################################################
    
def FindStones(src):
    stones, stonesimg, stonesclr = [], [], []
    gray = cv.cvtColor(src, cv.COLOR_BGR2HSV)
    mask = cv.inRange(gray, Config.colors["gray"][0], Config.colors["gray"][1])
    res1 = cv.bitwise_and(gray, gray, mask = mask)
    hue, saturation, gray = cv.split(res1)
    circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 20,
                               param1=100, param2=20,
                               minRadius=10, maxRadius=30)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center, radius = (i[0], i[1]), i[2]
            stones.append(center)
            stone = src[center[1] - radius:center[1] + radius, center[0] - radius:center[0] + radius]
            height, width, depth = stone.shape
            mask1 = np.zeros((height, width), np.uint8)
            mask1 = cv.circle(mask1,(int(width/2),int(height/2)),int((width-10)/2),(255, 0, 255),-1)
            stoneimg = cv.bitwise_and(stone, stone, mask = mask1)
            cv.imwrite("stone.jpeg", stoneimg)
            stonesimg.append(stoneimg)
            clr = Color.FindColor(stone, 2)
            if clr != 0:
                stonesclr.append(clr)
            #cv.circle(src, center, 5, (0, 100, 100), 2)
            #cv.circle(src, center, radius, (255, 0, 255), 2)
            #cv.line(src, center, (250, 250), (255, 0, 255), 2)
    else:
        return -1, -1

    #cv.imshow("detected circles", src)
    #cv.imwrite("final.jpeg", src)
    #cv.imshow("test", res1)
    #cv.imshow("hsv", gray)
    #cv.imwrite("hsv.jpeg", res1)
    print(stonesclr)
    #print(stones)
    liste = [list(a) for a in zip(FindDistance(stones), stonesclr)]
    score = SortStones(liste)
    return([stones, stonesclr], score)

###########################################################

def white_balance(img):
    result = cv.cvtColor(img, cv.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result = cv.cvtColor(result, cv.COLOR_LAB2BGR)
    return result

###########################################################

def FindDistance(stones):
    lengder = []
    for i in range(len(stones)):
        vektor = ([stones[i][0] - 250, stones[i][1] - 250])
        lengder.append(np.sqrt(vektor[0]**2 + vektor[1]**2))
    return(lengder)

###########################################################

def SortStones(stones):
    if len(stones) == 1:
        return(MakeScores(stones))
    else:
        sortedList = sorted(stones,key=lambda l:l[0], reverse=False)
        return(MakeScores(sortedList))

############################################################

def MakeScores(stones):
    Scores = [0, 0]
    Scores[stones[0][1]-1] += 1
    for i in range(1, len(stones)):
        if stones[i][1] == stones[0][1]:
            Scores[(stones[0][1] - 1)] += 1
        else:
            break
    print(Scores)
    return(Scores)

############################################################




