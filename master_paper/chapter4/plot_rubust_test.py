import matplotlib.pyplot as plt
import numpy as np
import matplotlib

matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus']=False     # 正常显示负号
# 假设的数据和参数
noise_ratio = np.array([0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0])
F_AIS1 = np.array([97, 93, 68, 69, 67, 68, 68])
F_AIS18 = np.array([89, 88 , 57, 54, 49, 51, 52])
F_ICMP00 = np.array([93, 90, 60, 62, 59, 57, 58])
F_ICMP03 = np.array([67, 65, 55, 55, 42, 38, 40])


# 绘制折线图
plt.figure(figsize=(10, 6))
plt.plot(noise_ratio, F_AIS1, 'o-', label='S7COMM')
plt.plot(noise_ratio, F_AIS18, 'o--', label='Modbus')
plt.plot(noise_ratio, F_ICMP00, 'o-', label='DNP')
plt.plot(noise_ratio, F_ICMP03, 'o--', label='EGD')


# 设置图表标题和坐标轴标签
plt.xlabel('噪声比例/%',fontsize=20)
plt.ylabel('F值/%',fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
# 添加图例
plt.legend()

# 显示网格
plt.grid(True)

# 显示图表
plt.show()