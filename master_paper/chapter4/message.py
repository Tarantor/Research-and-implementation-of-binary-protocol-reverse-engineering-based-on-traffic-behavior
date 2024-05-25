class Message:
    def __init__(self, message_id, time, src_ip_port, dst_ip_port, data):
        self.message_id = message_id
        self.time = time
        self.src_ip_port = src_ip_port
        self.dst_ip_port = dst_ip_port
        self.data = data #bytes
        #self.len = len
'''
保存着每条报文的切片结果
'''
class MessageSlice:
    def __init__(self, message: Message, n: int, fields: dict):
        self.message = message  # 具体的那条报文
        self.n = n  # n-gram
        self.fields = fields  # n-gram后的分词{0:32,1:00}