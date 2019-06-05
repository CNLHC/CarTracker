import sensor
import image
import time
import math
import network
import pyb
from tracking import TrackingFSM
from publish import PublishPeriodicly


SSID='nodegate'
KEY='2332332333'
wlan = network.WINC()
wlan.connect(SSID, key=KEY, security=wlan.WPA_PSK)

while not wlan.isconnected() :
    wlan.connect(SSID, key=KEY, security=wlan.WPA_PSK)
    pyb.delay(100)
    print("Trying to connect... (may take a while)...")


print(wlan.ifconfig())

PubObj  = PublishPeriodicly(interval = 200)
TrackingObj = TrackingFSM(relaxInDelay = 2000,relaxOutDelay =2000)
gNetworkPin =  pyb.Pin("P7", pyb.Pin.IN)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking



def parseImage(img,THRESHOLD = (30, 100, 15, 127, 15, 127)):
    blobs=img.find_blobs([THRESHOLD], pixels_threshold=600, area_threshold=600, merge=True)
    if len(blobs)>0:
        blob=blobs[0]
        return (blob.major_axis_line(),
        blob.min_corners(),
        blob.rect(),
        math.degrees(blob.rotation()))
    else:
        return False

def redrawImage(img,objectInfo=False):
    state = TrackingObj.getStateStr()
    if not objectInfo:
        img.draw_string(0,0,state,color=(0,255,0),scale=2)
    else:
        axis,corner,rect,degree = objectInfo
        img.draw_string(0,0,"%s\nangel-->%d"%(state,int(degree)),color=(0,255,0),scale=2)
        img.draw_line(axis,color=(255,255,255))
        img.draw_edges(corner, color=(0,0,255),thickness=2)
        img.draw_rectangle(rect,color=(0,255,0),thickness=2)

while(True):
    img = sensor.snapshot()
    objectInfo = parseImage(img)
    TrackingObj.feed(objectInfo)
    if gNetworkPin.value():
        if objectInfo != False:
            PubObj.pubInfo("%s,%d"%(TrackingObj.getStateStr(),objectInfo[3]))
        else:
            PubObj.pubInfo("%s,%d"%(TrackingObj.getStateStr(),-1))

    redrawImage(img,objectInfo=objectInfo)


