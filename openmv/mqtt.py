import usocket as socket
import ustruct as struct
from ubinascii import hexlify

class MQTTException(Exception):
    """MQTT模块异常
    
    :param Exception: [description]
    :type Exception: [type]
    """
    pass

class MQTTClient:
    """MQTT客户端。
    
    该类用于实现通过板载的Wifi模块和硬件厂商提供的usocket接口，模拟MQTT客户端的行为，向远程MQTT服务器发送数据。
    
    :raises MQTTException: 在出现MQTT协议错误时抛出
    :raises OSError: 出现系统IO错误时抛出
    """

    def __init__(self, client_id, server, port=0, user=None, password=None, keepalive=0,
                 ssl=False, ssl_params={}):
        """MQTT客户端构造函数
        
        :param client_id: MQTT客户端ID
        :type client_id: str
        :param server: 服务器域名或IP
        :type server: string
        :param port: 服务器监听MQTT请求的端口, defaults to 0
        :type port: int, optional
        :param user: 是否开启用户控制, defaults to None
        :type user: Boolean, optional
        :param password: 用户密码, defaults to None
        :type password: string, optional
        :param keepalive: 心跳包发送间隔, defaults to 0
        :type keepalive: int, optional
        :param ssl: 是否启用套接字层, defaults to False
        :type ssl: Boolean, optional
        """
        if port == 0:
            port = 8883 if ssl else 1883
        self.client_id = client_id
        self.sock = None
        self.server = server
        self.port = port
        self.ssl = ssl
        self.ssl_params = ssl_params
        self.pid = 0
        self.cb = None
        self.user = user
        self.pswd = password
        self.keepalive = keepalive
        self.lw_topic = None
        self.lw_msg = None
        self.lw_qos = 0
        self.lw_retain = False

    def _send_str(self, s):
        """通过socket发送字符串
        
        :param s: 即将发送的字符串
        :type s: str
        """
        self.sock.send(struct.pack("!H", len(s)))
        self.sock.send(s)

    def _recv_len(self):
        """返回socket缓冲区长度
        
        :return: 缓冲区长度
        :rtype: int
        """
        n = 0
        sh = 0
        while 1:
            b = self.sock.recv(1)[0]
            n |= (b & 0x7f) << sh
            if not b & 0x80:
                return n
            sh += 7

    def set_callback(self, f):
        """设置订阅回调

        :todo: 尚未实现
        
        :param f: 函数对象
        :type f: Callable
        """
        self.cb = f

    def set_last_will(self, topic, msg, retain=False, qos=0):
        """设置Lastwill信息
        
        :param topic: MQTT 会话名称
        :type topic: str
        :param msg: lastwill消息内容
        :type msg: str
        :param retain: 是否重发, defaults to False
        :type retain: bool, optional
        :param qos: qos等级, defaults to 0
        :type qos: int, optional
        """
        assert 0 <= qos <= 2
        assert topic
        self.lw_topic = topic
        self.lw_msg = msg
        self.lw_qos = qos
        self.lw_retain = retain

    def connect(self, clean_session=True):
        """尝试连接到远程MQTT服务器
        
        :param clean_session: 是否重新连接, defaults to True
        :type clean_session: bool, optional
        """
        self.sock = socket.socket()
        addr = None
        addr = socket.getaddrinfo(self.server, self.port)[0][-1]
        self.sock.connect(addr)
        if self.ssl:
            import ussl
            self.sock = ussl.wrap_socket(self.sock, **self.ssl_params)
        premsg = bytearray(b"\x10\0\0\0\0\0")
        msg = bytearray(b"\x04MQTT\x04\x02\0\0")

        sz = 10 + 2 + len(self.client_id)
        msg[6] = clean_session << 1
        if self.user is not None:
            sz += 2 + len(self.user) + 2 + len(self.pswd)
            msg[6] |= 0xC0
        if self.keepalive:
            assert self.keepalive < 65536
            msg[7] |= self.keepalive >> 8
            msg[8] |= self.keepalive & 0x00FF
        if self.lw_topic:
            sz += 2 + len(self.lw_topic) + 2 + len(self.lw_msg)
            msg[6] |= 0x4 | (self.lw_qos & 0x1) << 3 | (self.lw_qos & 0x2) << 3
            msg[6] |= self.lw_retain << 5

        i = 1
        while sz > 0x7f:
            premsg[i] = (sz & 0x7f) | 0x80
            sz >>= 7
            i += 1
        premsg[i] = sz

        self.sock.send(premsg[0:i + 2])
        self.sock.send(msg)
        #print(hex(len(msg)), hexlify(msg, ":"))
        self._send_str(self.client_id)
        if self.lw_topic:
            self._send_str(self.lw_topic)
            self._send_str(self.lw_msg)
        if self.user is not None:
            self._send_str(self.user)
            self._send_str(self.pswd)
        resp = self.sock.recv(4)
        assert resp[0] == 0x20 and resp[1] == 0x02
        if resp[3] != 0:
            raise MQTTException(resp[3])
        return resp[2] & 1

    def disconnect(self):
        """断开与远程服务器的连接
        """
        self.sock.send(b"\xe0\0")
        self.sock.close()

    def ping(self):
        """向远程服务器发送Ping请求
        """
        self.sock.send(b"\xc0\0")

    def publish(self, topic, msg, retain=False, qos=0):
        """向特定的Topic发布一条消息
        
        :param topic: MQTT Topic名称
        :type topic: str
        :param msg: 要发送的消息
        :type msg: BytesArray
        :param retain: 是否重发, defaults to False
        :type retain: bool, optional
        :param qos: qos等级, defaults to 0
        :type qos: int, optional
        """
        pkt = bytearray(b"\x30\0\0\0")
        pkt[0] |= qos << 1 | retain
        sz = 2 + len(topic) + len(msg)
        if qos > 0:
            sz += 2
        assert sz < 2097152
        i = 1
        while sz > 0x7f:
            pkt[i] = (sz & 0x7f) | 0x80
            sz >>= 7
            i += 1
        pkt[i] = sz
        #print(hex(len(pkt)), hexlify(pkt, ":"))
        self.sock.send(pkt[0:i + 1])
        self._send_str(topic)
        if qos > 0:
            self.pid += 1
            pid = self.pid
            struct.pack_into("!H", pkt, 0, pid)
            self.sock.send(pkt[0:2])
        self.sock.send(msg)
        if qos == 1:
            while 1:
                op = self.wait_msg()
                if op == 0x40:
                    sz = self.sock.recv(1)
                    assert sz == b"\x02"
                    rcv_pid = self.sock.recv(2)
                    rcv_pid = rcv_pid[0] << 8 | rcv_pid[1]
                    if pid == rcv_pid:
                        return
        elif qos == 2:
            assert 0

    def wait_msg(self):
        """阻塞的等待服务器回复消息
        
        :rtype: [type]
        """
        res = self.sock.recv(1)
        self.sock.setblocking(True)
        if res is None:
            return None
        if res == b"":
            raise OSError(-1)
        if res == b"\xd0":  # PINGRESP
            sz = self.sock.recv(1)[0]
            assert sz == 0
            return None
        op = res[0]
        if op & 0xf0 != 0x30:
            return op
        sz = self._recv_len()
        topic_len = self.sock.recv(2)
        topic_len = (topic_len[0] << 8) | topic_len[1]
        topic = self.sock.recv(topic_len)
        sz -= topic_len + 2
        if op & 6:
            pid = self.sock.recv(2)
            pid = pid[0] << 8 | pid[1]
            sz -= 2
        msg = self.sock.recv(sz)
        self.cb(topic, msg)
        if op & 6 == 2:
            pkt = bytearray(b"\x40\x02\0\0")
            struct.pack_into("!H", pkt, 2, pid)
            self.sock.send(pkt)
        elif op & 6 == 4:
            assert 0

    def check_msg(self):
        """获取一条消息
        
        """
        self.sock.setblocking(False)
        return self.wait_msg()
