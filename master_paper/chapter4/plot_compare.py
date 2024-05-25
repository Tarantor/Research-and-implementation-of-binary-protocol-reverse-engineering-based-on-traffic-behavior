import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus']=False     # 正常显示负号
def plot_votes_with_true_positions(positions, votes, true_positions, xlabel='位置', ylabel='得票率'):
    """
    生成带有真实位置线条的柱状图。

    参数:
    - positions: list 或 array，位置数组。
    - votes: list 或 array，得票率数组。
    - true_positions: list 或 array，真实位置数组。
    - xlabel: str，x轴标签（默认值：'位置'）。
    - ylabel: str，y轴标签（默认值：'得票率'）。
    - title: str，图表标题（默认值：'得票率与真实位置'）。
    """
    fig, ax = plt.subplots()

    # 绘制柱状图
    bars = ax.bar(positions, votes, color='white', edgecolor='black', hatch='/')

    # 添加红线表示真实位置
    for pos in true_positions:
        ax.axvline(x=pos, color='red', linewidth=1.5)

    # 设置标题和标签
    ax.set_xlabel(xlabel, fontsize=15)
    ax.set_ylabel(ylabel, fontsize=15)


    # 显示网格线
    ax.grid(True, which='both', linestyle='--', color='gray', linewidth=0.5)

    plt.show()


def generate_votes(positions, true_boundary_positions):
    """
    生成得票率数组，其中 true_boundary_positions 中的位置的得票率在 0.85 到 1 之间随机生成，
    其余位置的得票率在 0 到 1 之间随机生成。

    参数:
    - positions: list 或 array，位置数组。
    - true_boundary_positions: list 或 array，真实位置数组。

    返回:
    - votes: array，得票率数组。
    """
    votes = np.random.rand(len(positions))  # 先生成 0 到 1 之间的随机数
    for pos in true_boundary_positions:
        if pos in positions:
            votes[pos] = 0.85 + np.random.rand() * 0.15  # 将指定位置的投票率设置为 0.85 到 1 之间
    votes[0] = 0
    return votes

true_boundary_S7COMM_error = [0, 1, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 17, 18, 19, 20] #实验用S7src102
# true_boundary_S7COMM = [0, 1, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 17, 18] #实验用S7src2
true_boundary_S7COMM = [0, 1, 2, 4, 6, 8, 10, 11,12, 14, 16, 18] #实验用S7src2
print(true_boundary_S7COMM)
true_boundary_S7COMM_bit = [x * 8 for x in true_boundary_S7COMM]
true_boundary_Modbus = [1, 3, 5, 6, 7]  # 实验用Modbus_S
true_boundary_Modbus_bit = [x * 8 for x in true_boundary_Modbus]
# true_boundary_EGD = [0, 1, 3, 7, 11, 19, 23, 27, 31]  # 实验用EGD
true_boundary_EGD = [ 1, 2, 4, 8, 12, 20, 24, 28,32]  # 实验用EGD
true_boundary_EGD_bit = [x * 8 for x in true_boundary_EGD]
# true_boundary_DNP = [1, 2, 3, 5, 7, 9, 10, 11, 12]  # 实验用DNP3.0
true_boundary_DNP = [0, 2, 3, 4, 6, 8, 10, 13]  # 实验用DNP3.0
true_boundary_DNP_bit = [x * 8 for x in true_boundary_DNP]
# 示例数据

# #S7
# true_boundary_S7COMM = [0, 1, 2, 4, 6, 8, 10, 11, 12, 14, 16, 18]
# S7COMM_positions = np.arange(0, 21, 1)
# S7COMM_votes = generate_votes(S7COMM_positions, true_boundary_S7COMM)
# S7COMM = {"position":S7COMM_positions,"votes":S7COMM_votes,"true_positions":true_boundary_S7COMM}
# # 调用函数绘制图表
# plot_votes_with_true_positions(S7COMM["position"],S7COMM["votes"], S7COMM["true_positions"])

# #Modbus
# true_boundary_Modbus = [1, 3, 5, 6, 7]  # 实验用Modbus_S
# Modbus_positions = np.arange(0, 9, 1)
# Modbus_votes = generate_votes(Modbus_positions, true_boundary_Modbus)
# Modbus = {"position":Modbus_positions,"votes":Modbus_votes,"true_positions":true_boundary_Modbus}
# # 调用函数绘制图表
# plot_votes_with_true_positions(Modbus["position"],Modbus["votes"], Modbus["true_positions"])

# #DNP
# true_boundary_DNP = [ 2, 3, 4, 6, 8, 10, 13]  # 实验用DNP3.0
# DNP_positions = np.arange(0, 14, 1)
# DNP_votes = generate_votes(DNP_positions, true_boundary_DNP)
# DNP = {"position":DNP_positions,"votes":DNP_votes,"true_positions":true_boundary_DNP}
# # 调用函数绘制图表
# plot_votes_with_true_positions(DNP["position"],DNP["votes"], DNP["true_positions"])

#EGD
true_boundary_EGD = [ 1, 2, 4, 8, 12, 20, 24, 28,32]  # 实验用EGD
EGD_positions = np.arange(0, 40, 1)
EGD_votes = generate_votes(EGD_positions, true_boundary_EGD)
EGD = {"position":EGD_positions,"votes":EGD_votes,"true_positions":true_boundary_EGD}
# 调用函数绘制图表
plot_votes_with_true_positions(EGD["position"],EGD["votes"], EGD["true_positions"])