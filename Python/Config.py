import numpy as np

boot = dict(
    waitTime = 1,              #second the program waits after boot
    updateFreq = 10             #How often the program updates
    )

debug = dict(                   
    enabled = True,            #Print to debug log
    saveOrig = True,            #Save the original image (.jpeg)
    saveRGB = False,            #Save a RGB copy of main image (.jpeg)
    saveCSV = False             #Save a HSV copy of main image (.jpeg)
    )

cam = dict(                     
    res = [1344, 768],
    shutterSpeed = 10000,       #In milliseconds
    #ISO = 0                    #ISO of the camera (not in use)
    #Exposure?                  #Not implemented yet
    )

colors = dict(                  #Color Threshold for each color
    gray = [np.array([0, 0, 50]), np.array([200, 100, 160])],
    Red = [],
    Yellow = [],
    Blue = [],
    playing = ["Red", "Yellow"] #Which teams are playing ("Red", "Yellow" og "Blue")
    )

webServer = dict(               #Connection data to webserver
    ip = "192.168.10.1",        #Ip of the webserver
    user = "test",              #Username of the mySQL database
    password = "test"           #Password for the mySQL database
    )


