# import matplotlib.pyplot as plt
# import matplotlib
#
# matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
# matplotlib.rcParams['axes.unicode_minus']=False     # 正常显示负号
# # 准备数据
# algorithms = ['S7COMM', 'Modbus', 'DNP','EGD' ]
# a1 = [82, 82, 75, 93]  # 准确率数据，假设为百分比
# a2 = [94, 85, 86, 42]  # 召回率数据，假设为百分比
# a3 = [85,92,80,64]
# self_exp = [97, 89, 93, 67]  # F 值数据，假设为百分比
#
# # 绘制柱状图
# plt.figure(figsize=(10, 6))
#
# plt.bar([i-0.2 for i in range(len(algorithms))], a1, width=0.2, label='NEMESYS')
# plt.bar([i for i in range(len(algorithms))], a2, width=0.2, label='Netzob')
# plt.bar([i for i in range(len(algorithms))], a3, width=0.2, label='VDV')
# plt.bar([i+0.2 for i in range(len(algorithms))], self_exp, width=0.2, label='F值')
#
# plt.xlabel('协议')
# plt.ylabel('值/%')
# plt.xticks(range(len(algorithms)), algorithms)
# plt.legend(bbox_to_anchor=(0.95, 1))
# plt.grid(True, axis='y', linestyle='--', color='gray', linewidth=0.5)
#
#
# plt.show()



import matplotlib.pyplot as plt
import matplotlib

# 用黑体显示中文
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
# 正常显示负号
matplotlib.rcParams['axes.unicode_minus'] = False

# 准备数据
algorithms = ['S7COMM', 'Modbus', 'DNP', 'EGD']
a1 = [82, 82, 75, 93]  # 准确率数据，假设为百分比
a2 = [94, 85, 86, 42]  # 召回率数据，假设为百分比
a3 = [85, 92, 80, 64]
self_exp = [97, 89, 93, 67]  # F 值数据，假设为百分比

# 绘制柱状图
plt.figure(figsize=(10, 6))

# 增加宽度间隙，通过修改i的偏移量和宽度参数
bar_width = 0.15  # 减小宽度以便有更多空间
plt.bar([i - 0.3 for i in range(len(algorithms))], a1, width=bar_width, label='NEMESYS')
plt.bar([i - 0.1 for i in range(len(algorithms))], a2, width=bar_width, label='Netzob')
plt.bar([i + 0.1 for i in range(len(algorithms))], a3, width=bar_width, label='AutoReEngine')
plt.bar([i + 0.3 for i in range(len(algorithms))], self_exp, width=bar_width, label='本文实验方法')
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
# plt.xlabel('协议')
plt.ylabel('值/%',fontsize=20)
plt.xticks(range(len(algorithms)), algorithms)
plt.legend(bbox_to_anchor=(0.81, 0.8))
plt.grid(True, axis='y', linestyle='--', color='gray', linewidth=0.5)

plt.show()
# import seaborn as sns
# import matplotlib.pyplot as plt
#
# # 创建一些示例数据
# data = sns.load_dataset("tips")  # 使用seaborn内置的餐厅小费数据集
#
# # 绘制小提琴图
# sns.violinplot(x="day", y="total_bill", data=data)
#
# # 添加标题和标签
# plt.title('Violin Plot of Total Bills by Day')
# plt.xlabel('Day of the Week')
# plt.ylabel('Total Bill')
#
# # 显示图形
# plt.show()