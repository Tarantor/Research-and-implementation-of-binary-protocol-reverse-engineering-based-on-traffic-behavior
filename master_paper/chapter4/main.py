import csv
from time import *
from chapter4.processing import Processing
from ngram import Ngram
import  numpy as np
import time
from flip import Flip
import matplotlib.pyplot as plt

true_boundary_S7COMM_error = [0, 1, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 17, 18, 19, 20] #实验用S7src102
# true_boundary_S7COMM = [0, 1, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 17, 18] #实验用S7src2
true_boundary_S7COMM = [0, 1, 2, 4, 6, 8, 10, 11,12, 14, 16, 18] #实验用S7src2
# print(true_boundary_S7COMM)
true_boundary_S7COMM_bit = [x * 8 for x in true_boundary_S7COMM]
true_boundary_Modbus = [1, 3, 5, 6, 7]  # 实验用Modbus_S
true_boundary_Modbus_bit = [x * 8 for x in true_boundary_Modbus]
# true_boundary_EGD = [0, 1, 3, 7, 11, 19, 23, 27, 31]  # 实验用EGD
true_boundary_EGD = [ 1, 2, 4, 8, 12, 20, 24, 28,32]  # 实验用EGD
true_boundary_EGD_bit = [x * 8 for x in true_boundary_EGD]
# true_boundary_DNP = [1, 2, 3, 5, 7, 9, 10, 11, 12]  # 实验用DNP3.0
true_boundary_DNP = [0, 2, 3, 4, 6, 8, 10, 13]  # 实验用DNP3.0
true_boundary_DNP_bit = [x * 8 for x in true_boundary_DNP]
if __name__ == '__main__':
    prorocal = ['S7COMM_pure','modbus_H_pure','egd_pure','DNP_pure']
    name = ['S7COMM', 'Modbus', 'EGD', 'DNP']
    true_boundary = {0:true_boundary_S7COMM_bit,1:true_boundary_Modbus_bit,2:true_boundary_EGD_bit,3:true_boundary_DNP_bit}
    loction = [175,80,350,120]
    ngram = Ngram()
    index = 3
    ngram.read_csv_data_to_list("./data_extract/{}.csv".format(prorocal[index]))
    # print(ngram.packets_removed_other_information)
    # ngram.classify_by_length()
    # print(ngram.length_dict)

    flip = Flip(ngram.packets_removed_other_information)
    # rate = flip.flip_rate(loction[0])
    rate = flip.flip_rate(loction[index])
    magnitude = flip.magnitude(rate)
    gaussian = flip.gaussian_filter(magnitude, 1)
    bit_mark, boundary_mark = flip.use_magnitude_judge(gaussian)
    bit_mark_filter = [x * 8 for x in boundary_mark]
    bit_mark_filter.sort()
    a = true_boundary[index]
    plt.figure(figsize=(8, 6))  # 设置图像大小
    plt.plot(rate, label='翻转率')
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlabel("位置",fontsize=20)
    plt.ylabel("比特翻转率",fontsize=20)
    # plt.title("{}字节翻转率".format(name[index]),fontsize=20)
    for vertical_line_x in a:
        if vertical_line_x != a[-1]:
            plt.axvline(x=vertical_line_x, color='red', linestyle='-')
        else:
            plt.axvline(x=vertical_line_x, color='red', linestyle='-', label='真实边界')

    for i in bit_mark_filter:
        if i != bit_mark_filter[-1]:
            plt.axvline(x=i, color='green', linestyle='-.')
        else:
            plt.axvline(x=i, color='green', linestyle='-.', label='推断边界')
    plt.grid(True)
    plt.legend(loc='upper right')
    plt.show()


    #动态生成
    # start = time.perf_counter()
    # ngram.D_generate_Eigen_vectors(thre=0.9,gram=(2,4),model=2,step =0.5,type_mode=0 )0