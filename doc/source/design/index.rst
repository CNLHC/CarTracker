软件设计
~~~~~~~~~~

终端摄像机程序设计
++++++++++++++++++++

.. include:: apidoc/openmv.rst

数据展示页面程序设计
++++++++++++++++++++

使用 React + Redux ，以MVVM的方式管理从Mqtt订阅得到的传感器数据。

使用百度开源可视化工具 ECharts 绘制实时数据。

前端页面维护一个状态树，内部包含预定义的数据结构。

使用 `MQTTjs` 订阅来自Broker转发的小车姿态信息。获取信息后，在接收信息回调里 `dispatch` 一个 `Action`

由 `Redux` 支持的 `Reducer` 会响应该 `Action` 并将数据同步到状态树内。

通过 `Connect`方法， 将包装过的`React-Echarts`状态连接到状态树内，当状态树的数据更新时，`React`底层会触发重渲染逻辑，将数据显示在前端页面。
