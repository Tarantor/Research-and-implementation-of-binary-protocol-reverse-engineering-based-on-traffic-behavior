"""
位翻转
主要用来作垂直结构分析
当然啦，垂直结构不只是这边的方法，还包括以前使用的方法，例如频繁项挖掘，部分语义
"""
import matplotlib
from ngram import Ngram
from processing import Processing
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import math
import numpy as np

matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus']=False     # 正常显示负号
class Flip:
    '''
    class Message:
    def __init__(self, message_id, time, src_ip_port, dst_ip_port, data):
        self.message_id = message_id
        self.time = time
        self.src_ip_port = src_ip_port
        self.dst_ip_port = dst_ip_port
        self.data = data #bytes
    '''

    def __init__(self, messages):
        self.messages = messages  # Message list
        self.bins = []

    '''
    所有message转化为二进制
    '''

    def messages2bin(self):
        bins = []
        for message in self.messages:
            bins.append(self.message2bin(message))
        return bins

    '''
    单个message转化为二进制
    '''

    def message2bin(self, hex_str: str):
        new_hex_str = "1" + hex_str
        hex_int = bin(int(new_hex_str, 16))[3:]
        return hex_int

    '''
    计算翻转率
    bit_range:要计算的最大bit位数，例如8就代表要统计前8个比特
    '''

    def flip_rate(self, bit_range: int):
        bins = self.messages2bin()
        total_messages_num = len(bins)
        # print(total_messages_num)
        fr = []
        for position in range(0, bit_range):
            count = 0
            for index in range(0, total_messages_num - 1):
                if bins[index][position] != bins[index + 1][position]:
                    count += 1
            fr.append(count / (total_messages_num))  # 减一的主要作用是两两之间的变化比message的数量少一
        print(fr)
        return fr

    '''
    转化成幅度
    就是将rate进行一个离散化
    '''

    def magnitude(self, flip_rate: list):
        magnitude_num = []
        for rate in flip_rate:
            # print(math.log(rate+0.00000001, 10))
            magnitude_num.append(math.ceil(math.log(rate + 0.00000001, 10)))
        print(magnitude_num)
        return magnitude_num

    '''
    利用magnitude进行边界推测
    bit_mark:可能是边界的bit位
    boundary_mark:当边界以字节为单位时，要将bit位处理到byte粒度
    '''

    def use_magnitude_judge(self, magnitude_num: list):
        bit_mark = []
        boundary_mark = set()
        for bit_pos in range(0, len(magnitude_num) - 1):
            if magnitude_num[bit_pos] < magnitude_num[bit_pos + 1]:
                bit_mark.append(bit_pos+1)
                boundary_mark.add(math.floor(bit_pos / 8))
        return bit_mark, boundary_mark

    # def use_rate_judge(self, magnitude_num: list,threshold = 0.005):
    #     bit_mark = []
    #     boundary_mark = set()
    #     for bit_pos in range(0, len(magnitude_num) - 1):
    #         if magnitude_num[bit_pos] < magnitude_num[bit_pos + 1] and magnitude_num[bit_pos]<threshold and magnitude_num[bit_pos + 1]> threshold  :
    #             bit_mark.append(bit_pos)
    #             boundary_mark.add(math.ceil(bit_pos / 8))
    #         elif magnitude_num[bit_pos] > magnitude_num[bit_pos + 1] and magnitude_num[bit_pos]>threshold and magnitude_num[bit_pos + 1]< threshold :
    #             bit_mark.append(bit_pos+1)
    #             boundary_mark.add(math.ceil(bit_pos / 8))
    #     boundary_mark = sorted(boundary_mark)
    #     return bit_mark, boundary_mark
    # def use_rate_judge(self, magnitude_num: list, threshold=0.5):
    #     bit_mark = []
    #     boundary_mark = set()
    #     for bit_pos in range(0, len(magnitude_num) - 1):
    #         if magnitude_num[bit_pos] < magnitude_num[bit_pos + 1] :
    #             if magnitude_num[bit_pos] < threshold and magnitude_num[bit_pos + 1] > threshold and magnitude_num[bit_pos] < magnitude_num[bit_pos + 1]:
    #                 bit_mark.append(bit_pos+1)
    #                 boundary_mark.add(math.ceil(bit_pos / 8))
    #         elif (magnitude_num[bit_pos] > magnitude_num[bit_pos + 1] and
    #               magnitude_num[bit_pos] > threshold and
    #               magnitude_num[bit_pos + 1] < threshold and
    #               magnitude_num[bit_pos] > magnitude_num[bit_pos + 1]):
    #             bit_mark.append(bit_pos + 1)
    #             boundary_mark.add(math.ceil(bit_pos / 8))
    #     boundary_mark = sorted(boundary_mark)
    #     return bit_mark, boundary_mark
    def use_rate_judge(self, magnitude_num: list, threshold=0.05):
        bit_mark = []
        boundary_mark = set()
        for bit_pos in range(0, len(magnitude_num) - 1):
            if magnitude_num[bit_pos] < magnitude_num[bit_pos + 1]:
                bit_mark.append(bit_pos + 1)
                boundary_mark.add(math.ceil(bit_pos / 8))
            elif magnitude_num[bit_pos] > magnitude_num[bit_pos + 1] :
                bit_mark.append(bit_pos + 1)
                boundary_mark.add(math.ceil(bit_pos / 8))
        boundary_mark = sorted(boundary_mark)
        return bit_mark, boundary_mark
    '''
    gussian滤波
    '''

    def gaussian_filter(self, flip_rate: list, sigma: float):
        a = gaussian_filter(flip_rate, sigma)
        print(a)
        return a

    '''
    画图
    '''

    def plot_flip_rate(self, flip_rate: list):
        plt.figure(figsize=(8, 6))  # 设置图像大小
        plt.plot(flip_rate,label ='翻转率')
        plt.xlabel("位置")
        plt.ylabel("比特翻转率")



# true_boundary_S7COMM_error = [0, 1, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 17, 18, 19, 20] #实验用S7src102
# # true_boundary_S7COMM = [0, 1, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 17, 18] #实验用S7src2
# true_boundary_S7COMM = [0, 1, 2, 4, 6, 8, 10, 11,12, 14, 16, 18] #实验用S7src2
# print(true_boundary_S7COMM)
# true_boundary_S7COMM_bit = [x * 8 for x in true_boundary_S7COMM]
# true_boundary_Modbus = [1, 3, 5, 6, 7]  # 实验用Modbus_S
# true_boundary_Modbus_bit = [x * 8 for x in true_boundary_Modbus]
# # true_boundary_EGD = [0, 1, 3, 7, 11, 19, 23, 27, 31]  # 实验用EGD
# true_boundary_EGD = [ 1, 2, 4, 8, 12, 20, 24, 28,32]  # 实验用EGD
# true_boundary_EGD_bit = [x * 8 for x in true_boundary_EGD]
# # true_boundary_DNP = [1, 2, 3, 5, 7, 9, 10, 11, 12]  # 实验用DNP3.0
# true_boundary_DNP = [0, 2, 3, 4, 6, 8, 10, 13]  # 实验用DNP3.0
# true_boundary_DNP_bit = [x * 8 for x in true_boundary_DNP]
#
# protocal = "Modbus_H"
# p = Processing(pcap_file_path='../data/pcap_data/S7COMM_pure.pcap', csv_file_path="../data/csv_data/{}.csv".format(protocal))
# p.import_messages_from_csv()
# # def max_len(messages:list):
# #     lens = []
# #     for i in range(len(messages)):
# #         paylodes = messages[i].data
# #         length = len(paylodes)
# #         lens.append(length)
# #     return max(lens)
# #
# # max_len = max_len(p.messages)
# # print(max_len)
# flip = Flip(p.messages)
# rate = flip.flip_rate(80)
# magnitude = flip.magnitude(rate)
# gaussian = flip.gaussian_filter(magnitude,1)
# bit_mark, boundary_mark = flip.use_magnitude_judge(gaussian)
#
#
#
#
# bit_mark_filter = [x * 8 for x in boundary_mark]
#
# bit_mark_filter.sort()
# print(bit_mark_filter)
# a = true_boundary_Modbus_bit
#
# plt.figure(figsize=(8, 6))  # 设置图像大小
# plt.plot(rate,label='翻转率')
# plt.xlabel("位置")
# plt.ylabel("比特翻转率")
# for vertical_line_x in a:
#     if vertical_line_x != a[-1]:
#         plt.axvline(x=vertical_line_x, color='red', linestyle='-')
#     else:
#         plt.axvline(x=vertical_line_x, color='red', linestyle='-',label='真实边界')
#
# for i in bit_mark_filter:
#     if i != bit_mark_filter[-1]:
#         plt.axvline(x=i, color='green', linestyle='-.')
#     else:
#         plt.axvline(x=i, color='green', linestyle='-.',label='推断边界')
# plt.grid(True)
# plt.legend(loc='upper right')
# plt.show()


