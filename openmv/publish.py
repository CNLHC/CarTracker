from tracking import TrackingFSM
from mqtt import MQTTClient
import pyb
class PublishPeriodicly():
    """发布对象

    该类用于管理信息发布逻辑。可以通过在构造是设置interval参数，实现以一定的频率进行信息发布。

    该类的pubInfo方法是可以被连续调用. 通过内部的定时器可以实现在连续调用时以一定频率Pub。

    本质上是对数据流的降采样过程。
    """
    def __init__(self,interval=1000):
        """构造函数
        
        :param interval: 发布信息的周期, defaults to 1000
        :type interval: int, optional
        """
        self.__interval=interval
        self.__MQTTC = MQTTClient("openmv", server="ali.cnworkshop.xyz", port=20000)
        self.__MQTTC.connect()
        self.__InnerCounter=pyb.millis()
    def pubInfo(self,info):
        """发布信息

        该函数可以被重复调用。但是会按照预设的周期发布信息。在两次有效发布之间的调用会立即返回。
        
        :param info: 要发布到MQTT Broker 的信息
        :type info: str
        """
        if  pyb.millis()-self.__InnerCounter >self.__interval:
            print("pub%s"%info)
            self.__InnerCounter=pyb.millis()
            self.__MQTTC.publish("openmv/data",info)
