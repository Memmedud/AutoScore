import sys
import time
import cv2 as cv
import FinnStein as FS
from picamera.array import PiRGBArray
from picamera import PiCamera
import Webserver as WS
import io
import numpy
import config
import Vision

def main(argv):
    camera = PiCamera()
    camera.shutter_speed = config.cam["shutterSpeed"]
    camera.resolution = (config.cam["res"][0], config.cam["res"][0])
    rawCapture = PiRGBArray(camera)

    time.sleep(config.boot["waitTime"])

    while True:
        camera.capture(rawCapture, format="bgr")
        img = rawCapture.array
        cv.imwrite("test.jpeg", img)
        img = Vision.FindBo(img)
        stones = Vision.FindStones(img)

        time.sleep(config.boot["updateFreq"])

if __name__ == "__main__":
    main(sys.argv[5:])








