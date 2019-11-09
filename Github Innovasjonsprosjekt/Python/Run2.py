import sys
import time
import cv2 as cv
import FinnStein as FS
import Curling_stor_sirkel as CSS    
from picamera.array import PiRGBArray
from picamera import PiCamera
import Webserver as WS
import io
import numpy

url = ""
user = ""
password = ""
debug = True

tabellnavn = "stein"
databasenavn = "test"

def main(argv):
        if debug == False:
                url = input("What is the URL of the server? ")
                user = input("Username? ")
                password = input("Password? ")
        
    #while True:
        camera = PiCamera()
        rawCapture = PiRGBArray(camera)
        camera.shutter_speed = 10000
        camera.resolution = (1344, 768)
        camera.start_preview()
        time.sleep(0.5)
        rawCapture = PiRGBArray(camera)
        camera.capture(rawCapture, format="bgr")
        img = rawCapture.array
        camera.stop_preview()
        cv.imwrite("test.jpeg", img)
        img = CSS.stor_sirkel(img)
        stones = FS.FindStones(img)
        print(FS.FindDistance(stones))
        #time.sleep(1)
if __name__ == "__main__":
    main(sys.argv[5:])








