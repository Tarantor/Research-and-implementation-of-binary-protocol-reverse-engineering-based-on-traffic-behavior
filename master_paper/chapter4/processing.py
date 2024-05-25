import pandas as pd
import dpkt
import csv
import socket
import datetime
from chapter4.message import Message
#

class Processing:
    def __init__(self, pcap_file_path: str, csv_file_path: str) -> object:
        self.pcap_file_path = pcap_file_path  # str
        self.csv_file_path = csv_file_path  # str
        self.messages = []  # [message1,...]

    def read_messages_from_pcap_and_transform_to_csv(self):
        if self.pcap_file_path is None:
            raise TypeError("pcap_file_path cannot be None")
        if self.csv_file_path is None:
            raise TypeError("csv_file_path cannot be None")
        f = open(self.pcap_file_path, 'rb')
        if self.pcap_file_path.split('.')[-1] == "pcapng":
            dp = dpkt.pcapng.Reader(f)
        else:
            dp = dpkt.pcap.Reader(f)

        for ts, buff in dp:
            base_timestamp = ts  # 获取第一条message的时间戳作为基准，以计算message之间的相对时间
            break
        f = open(self.pcap_file_path, 'rb')
        if self.pcap_file_path.split('.')[-1] == "pcapng":
            dp = dpkt.pcapng.Reader(f)
        else:
            dp = dpkt.pcap.Reader(f)

        cf = open(self.csv_file_path, 'w', newline="")
        cf.truncate()  # 清空文件

        w = csv.writer(cf)
        w.writerow(['time', 'src ip:port', 'dst ip:port', 'data'])
        for index, (ts, buf) in enumerate(dp):
            relative_time = ts - base_timestamp  # 相对时间
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            ip_src = socket.inet_ntop(socket.AF_INET, ip.src)
            ip_dst = socket.inet_ntop(socket.AF_INET, ip.dst)
            tcp = ip.data
            sport = tcp.sport
            dport = tcp.dport
            payload = tcp.data
            # print("ip:", ip)
            # print("tcp:", tcp)
            # print("payload", payload)
            payload = payload.hex()  # 转化为字符串

            w.writerow([relative_time, ip_src + ':' + str(sport), ip_dst + ':' + str(dport), payload])
        cf.close()

    def import_messages_from_csv(self):
        if self.csv_file_path is None:
            raise TypeError("csv_file_path cannot be None")
        csv = pd.read_csv(self.csv_file_path, encoding_errors="ignore")
        for index, row in csv.iterrows():
            time = row["time"]
            src_ip_port = row["src ip:port"]
            dst_ip_port = row["dst ip:port"]
            payload = row["data"]
            payload2bytes = bytes.fromhex(payload)
            self.messages.append(Message(index, time, src_ip_port, dst_ip_port, payload2bytes))

    # 将消息按方向进行分类
    def cluster_messages_by_direction(self) -> dict:
        if len(self.messages) == 0:
            self.import_messages_from_csv()
        messages_clustered_by_direction = {}
        for message in self.messages:
            if message.src_ip_port not in messages_clustered_by_direction:
                messages_clustered_by_direction[message.src_ip_port] = []
            messages_clustered_by_direction[message.src_ip_port].append(message)
        return messages_clustered_by_direction

    # 将消息按长度进行分类
    def cluster_messages_by_len(self, messages=None) -> dict:
        if messages is None:
            if len(self.messages) == 0:
                self.import_messages_from_csv()
            messages = self.messages
        assert len(messages) != 0
        messages_clustered_by_len = {}
        for message in messages:
            if len(message.data) not in messages_clustered_by_len:
                messages_clustered_by_len[len(message.data)] = []
            messages_clustered_by_len[len(message.data)].append(message)
        return messages_clustered_by_len

