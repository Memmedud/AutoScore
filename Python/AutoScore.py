import sys
import time
import datetime
import cv2 as cv
from picamera.array import PiRGBArray
from picamera import PiCamera
import Webserver
import Config
import Vision

def main(argv):
    if Config.debug["enabled"] == False:
        database = str(datetime.datetime.now())
    else:
        database = "stein"
    camera = PiCamera()
    camera.shutter_speed = Config.cam["shutterSpeed"]
    camera.resolution = (Config.cam["res"][0], Config.cam["res"][0])
    time.sleep(Config.boot["waitTime"])

    while True:
        rawCapture = PiRGBArray(camera)
        if Config.debug["enabled"] == False:
            Webserver.CreateStoneTable(database)
        camera.capture(rawCapture, format="bgr")
        img = rawCapture.array
        camera.stop_preview()
        #cv.imwrite("test.jpeg", img)
        img = Vision.white_balance(img)
        img = Vision.FindBo(img)
        if not img.any == -1:
            stones, score = Vision.FindStones(img)
            Webserver.ClearTable(database)
            print(stones)
            print(score)
            if stones != -1:
                temp = []
                Webserver.InsertData(database, ["Nummer", "PosX", "PosY", "Farge"], [0, score[0], score[1], 0])
                for i in range(len(stones[1])):
                    temp.append([i+1, stones[0][i][0], stones[0][i][1], stones[1][i]])
                for i in range(len(temp)):
                    Webserver.InsertData(database, ["Nummer", "PosX", "PosY", "Farge"], temp[i])
        time.sleep(Config.boot["updateFreq"])

if __name__ == "__main__":
    main(sys.argv[5:])








