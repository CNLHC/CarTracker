软件测试
~~~~~~~~~~~~

由于软件规模较小及项目时间较为紧迫，未实现单元测试。仅实现了系统功能测试。


测试硬件条件
=============

1. OpenMV H6 摄像头
2. OpenMV 堆叠式Wifi模块
3. 拥有公网IP的Web服务器
4. 个人计算机
5. wifi热点
6. 一辆红色的小车


测试软件条件
===============

1. Cartracker-Frontend 已在云端部署
2. 个人计算机中安装了 OpenMV IDE

测试方法
==============

1. 在浏览器中打开部署的CarTracker-Frontend 页面
2. 打开OpenMV IDE, 加载CarTracker-Openmv 中的 python程序
3. 运行CarTracker程序
4. 将摄像机对准红色小车
5. 变换摄像机角度


测试预期结果
===============

1. OpenMV IDE中能够显示视频流
2. 红色的小车可被正确识别

    + 画面左上角出现 `Locking` 字样与小车的角度信息。
    + 小车外轮廓被一个蓝色矩形框住

3. 晃动摄像机，小车能够保持被锁定的状态
4. 观察前端页面，实时角度信息可以被同步

实际测试结果
==============

与预期相吻合