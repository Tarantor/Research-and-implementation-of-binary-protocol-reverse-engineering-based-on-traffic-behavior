import pandas as pd
import csv
import utility
import math


class PcapData:
    def __init__(self):
        self.packets_removed_other_information = []
        self.packets_removed_other_information_bin = []
        self.min_packet_length = 100000
        self.r1_r2_bits_string_around_i = {}  # {(i,r):[string]}
        self.r1_r2_bits_string_around_i_count = {}  # {(i,r):({"left_string":count}, {"right_string":count})}
        self.left_and_right_entropy = {}  # {(i,r):(left_entropy, right_entropy))
        self.left_and_right_entropy_sum_from_r1_to_r2 = {}  # {i:(left_entropy, right_entropy)}
        self.left_and_right_entropy_difference = {}  # {i:difference}

    # 读取filter_database.csv文件中的packet
    def read_csv_data_to_list(self, file_path: str) -> object:
        with open(file_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            listreport = [row[0] for row in csvreader]
        for row in listreport:
            self.packets_removed_other_information.append(row)

    # 全部转01字符串，方便后面的切片操作
    def list_hex2bin(self) -> object:
        for value in self.packets_removed_other_information:
            result = utility.hex2bin(value)
            if len(result) < self.min_packet_length:
                self.min_packet_length = len(result)
            self.packets_removed_other_information_bin.append(result)

    # 寻找第i比特左右r位比特串
    def achieve_r_bits_string_around_i(self, i: int, r: int) -> tuple:  # i从0开始
        r_bits_string_around_i_of_every_packet = []
        left_r_bits_string_around_i_of_every_packet = []
        right_r_bits_string_around_i_of_every_packet = []
        for packet in self.packets_removed_other_information_bin:
            if i < r:  # eg.00101,i=1,r=2
                fill_bits_number = r - i
                left_r_bits_string_around_i = packet[: i]
                right_r_bits_string_around_i = packet[i + 1: i + 1 + r]
                for j in range(fill_bits_number):
                    left_r_bits_string_around_i = '0' + left_r_bits_string_around_i
                    # 把最左侧补齐
            elif i > len(packet) - r - 1:  # eg.010011,i=4,r=2
                fill_bits_number = r - (len(packet) - 1 - i)
                left_r_bits_string_around_i = packet[i - r: i]
                right_r_bits_string_around_i = packet[i + 1:]
                for j in range(fill_bits_number):
                    right_r_bits_string_around_i += '0'
                    # 把最右侧侧补齐
            else:
                left_r_bits_string_around_i = packet[i - r: i]
                right_r_bits_string_around_i = packet[i + 1: i + 1 + r]
            r_bits_string_around_i_of_every_packet.append((left_r_bits_string_around_i, right_r_bits_string_around_i))
            left_r_bits_string_around_i_of_every_packet.append(left_r_bits_string_around_i)
            right_r_bits_string_around_i_of_every_packet.append(right_r_bits_string_around_i)
        return r_bits_string_around_i_of_every_packet, left_r_bits_string_around_i_of_every_packet, right_r_bits_string_around_i_of_every_packet

    def achieve_r1_r2_bits_string_around_i(self, r1_r2: tuple) -> object:#位置 i 和范围 r，及i位置左右rbit的信息
        for i in range(self.min_packet_length):
            for r in range(r1_r2[0], r1_r2[1] + 1, 1):
                result = self.achieve_r_bits_string_around_i(i, r)
                self.r1_r2_bits_string_around_i[(i, r)] = result[1:]#不要第一个是去掉本位置的

    # 统计一下p(b(i-r)...b(i-1))和p(b(i+1)...b(i+r))
    # self.r1_r2_bits_string_around_i_count = {}  # {(i,r):({"left_string":count}, {"right_string":count})}
    def count_r1_r2_bits_string_around_i(self):
        for i_r, left_right in self.r1_r2_bits_string_around_i.items():
            if i_r not in self.r1_r2_bits_string_around_i_count:
                self.r1_r2_bits_string_around_i_count[i_r] = ({}, {})
            for left_string, right_string in zip(left_right[0], left_right[1]):
                if left_string not in self.r1_r2_bits_string_around_i_count[i_r][0]:
                    self.r1_r2_bits_string_around_i_count[i_r][0][left_string] = 0
                self.r1_r2_bits_string_around_i_count[i_r][0][left_string] += 1
                if right_string not in self.r1_r2_bits_string_around_i_count[i_r][1]:
                    self.r1_r2_bits_string_around_i_count[i_r][1][right_string] = 0
                self.r1_r2_bits_string_around_i_count[i_r][1][right_string] += 1

    # 计算左右分支信息熵，给定（i,r）
    def calculate_left_and_right_entropy_given_i_r(self, i_r: tuple):
        packets_number = len(self.packets_removed_other_information_bin)
        H_left = 0
        H_right = 0
        for left_string, count in self.r1_r2_bits_string_around_i_count[i_r][0].items():#计算左边的信息熵
            p = count / packets_number
            H_left -= p * math.log2(p)
        for right_string, count in self.r1_r2_bits_string_around_i_count[i_r][1].items():#计算右边的信息熵
            p = count / packets_number
            H_right -= p * math.log2(p)
        self.left_and_right_entropy[i_r] = (H_left, H_right)#得到i位置的左右信息熵元组

    # 计算左右分支信息熵 (i, r)
    def calculate_left_and_right_entropy(self, r1_r2: tuple) -> object:
        for i in range(self.min_packet_length):
            for r in range(r1_r2[0], r1_r2[1] + 1, 1):
                self.calculate_left_and_right_entropy_given_i_r((i, r))

    # 计算左右信息熵和 i,r belong to [r1, r2]
    def calculate_left_and_right_entropy_sum_from_r1_to_r2(self, r1_r2: tuple):
        for i in range(self.min_packet_length):
            H_left = 0
            H_right = 0
            for r in range(r1_r2[0], r1_r2[1] + 1, 1):
                H_left += self.left_and_right_entropy[(i, r)][0] / r
                H_right += self.left_and_right_entropy[(i, r)][1] / r
            self.left_and_right_entropy_sum_from_r1_to_r2[i] = (H_left, H_right)

    # 计算i处的左右信息熵差
    def calculate_left_and_right_entropy_difference(self):
        for i in range(self.min_packet_length):
            self.left_and_right_entropy_difference[i] = math.fabs(self.left_and_right_entropy_sum_from_r1_to_r2[i][0] -
                                                                  self.left_and_right_entropy_sum_from_r1_to_r2[i][1])

