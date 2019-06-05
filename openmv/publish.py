from tracking import TrackingFSM
from mqtt import MQTTClient
import pyb
class PublishPeriodicly():
    def __init__(self,interval=1000):
        self.__interval=interval
        self.__MQTTC = MQTTClient("openmv", server="ali.cnworkshop.xyz", port=20000)
        self.__MQTTC.connect()
        self.__InnerCounter=pyb.millis()
    def pubInfo(self,info):
        if  pyb.millis()-self.__InnerCounter >self.__interval:
            print("pub%s"%info)
            self.__InnerCounter=pyb.millis()
            self.__MQTTC.publish("openmv/data",info)
