# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import utility
from ngram import Ngram
import preprocess
from matplotlib import pyplot as plt
import numpy as np


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ngram = Ngram()
    ngram.read_csv_data_to_list("../data/csv_data/S7COMM_pure.csv") #读取csv文件data字段截尾后存入packets_removed_other_information[]
    # print(ngram.packets_removed_other_information)
    ngram.list_hex2bin()#packets_removed_other_information[]的每个message转化为二进制字符串存入新的packets_removed_other_information_bin[]
    ngram.ngram((3, 6))#对packets_removed_other_information_bin[]中的每个message进行切片操作切片范围3-6，获得ngram_loction格式的候选集
                        #this_packet_n1_to_n2_ngram_loction_dict[n][]当前message的3-6切片，all_ngam_loction[]这个协议包的所有ngram_loction，n1_to_n2_ngram_loction_dict[n][]
                        #n1_to_n2_ngram_loction_dict[n][]这个类型协议里3-6切片的存储，返回的packet1_to_packet2_ngram_loction_dict[][][]每个message针对3-6切片的集合
    ngram.count_ngram_loction()#获得n1_to_n2_ngram_loction_count[n][ngram_loction]记录了每个n切片下每个n-gram-location的出现次数
    # print(ngram.n1_to_n2_ngram_loction_count)#3: {('110', 0): 325, ('100', 1): 325, ...
    ngram.filter_by_support(0.95)#通过阈值来筛选频率较高的的n-gram-location字段
    print(ngram.n1_to_n2_ngram_loction_count_filtered_by_support)