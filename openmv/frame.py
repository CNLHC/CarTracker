import image
import math
class FrameHandle:
    """该类用于封装处理单个帧的逻辑
    
    :return: [description]
    :rtype: [type]
    """
    def __init__(self,TrackingObj):
        self.TrackingObj = TrackingObj
        pass
    def parseImage(self,img,THRESHOLD = (30, 100, 15, 127, 15, 127)):
        """解析一帧数据.

        该函数用于解析一帧图片数据，并通过判断连续的色块来预测当前帧内是否有被锁定对象。如果有被锁定的对象，则返回该对象的相关信息，包括轴线，角度以及外轮廓.否则返回False对象.

        :param img: 传感器输出的图片对象
        :type img:  Sensor.Image
        :param THRESHOLD: 颜色检测使用的阈值，分别是三个通道的下限和上限, defaults to (30, 100, 15, 127, 15, 127)
        :type THRESHOLD: tuple, optional
        :return: 解析得到的图片数据或False
        :rtype: objectInfo | False
        """
        blobs=img.find_blobs([THRESHOLD], pixels_threshold=600, area_threshold=600, merge=True)
        if len(blobs)>0:
            blob=blobs[0]
            return (blob.major_axis_line(),
            blob.min_corners(),
            blob.rect(),
            math.degrees(blob.rotation()))
        else:
            return False
    def redrawImage(self,img,objectInfo=False):
        """重新绘制图片，在图片上添加当前状态信息
        
        :param img: 图像对象
        :type img: Sensor.Image
        :param objectInfo: 传感器图像信息, defaults to False
        :type objectInfo: bool|Tuple
        """
        state = self.TrackingObj.getStateStr()
        if not objectInfo:
            img.draw_string(0,0,state,color=(0,255,0),scale=2)
        else:
            axis,corner,rect,degree = objectInfo
            img.draw_string(0,0,"%s\nangel-->%d"%(state,int(degree)),color=(0,255,0),scale=2)
            img.draw_line(axis,color=(255,255,255))
            img.draw_edges(corner, color=(0,0,255),thickness=2)
            img.draw_rectangle(rect,color=(0,255,0),thickness=2)
