
"""追踪主模块

"""
import sensor

import time
import network
import pyb
from tracking import TrackingFSM
from publish import PublishPeriodicly
from frame import FrameHandle

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
FrameObj = FrameHandle(TrackingObj)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking




while(True):
    img = sensor.snapshot()
    objectInfo = FrameObj.parseImage(img)
    TrackingObj.feed(objectInfo)

    if objectInfo != False:
        PubObj.pubInfo("%s,%d"%(TrackingObj.getStateStr(),objectInfo[3]))
    else:
        PubObj.pubInfo("%s,%d"%(TrackingObj.getStateStr(),-1))

    FrameObj.redrawImage(img,objectInfo=objectInfo)


