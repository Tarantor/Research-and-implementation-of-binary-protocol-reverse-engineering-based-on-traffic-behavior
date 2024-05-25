# import matplotlib.pyplot as plt
# from sklearn.datasets import make_moons
# from sklearn.cluster import DBSCAN
#
# # 创建数据集
# X, _ = make_moons(n_samples=300, noise=0.1)
#
# # 使用DBSCAN进行聚类
# dbscan = DBSCAN(eps=0.2, min_samples=5)
# clusters = dbscan.fit_predict(X)
#
# # 绘制聚类结果
# plt.figure(figsize=(8, 6))
# plt.scatter(X[:, 0], X[:, 1], c=clusters, cmap='viridis', marker='o', edgecolor='k')
# plt.title('DBSCAN Clustering')
# plt.xlabel('Feature 1')
# plt.ylabel('Feature 2')
# plt.colorbar(label='Cluster ID')
# plt.show()
import math
# import textdistance
# a=[[0, 12, 24, 36, 45, 57, 69, 81, 89, 97, 107, 119, 131, 139], ['000bab', '001c06', '080045', '012', 'e0617a', '166c0a', '06604e', '31', '8e', '0008', '003000', '080320', '1f', '028000']]
# b=[[6, 14, 23, 28, 44, 56], ['001c06', '000bab', '080045', '2b', '80064a', '0102c0']]
# c=[[0, 12, 24, 36, 44, 56, 68, 86, 96, 106, 118, 130, 139], ['000bab', '001c06', '080045', '012', 'e0617a', '166c0a', '06604e', '31', '8e', '0008', '003000', '080320', '1f', '028000']]
#
#
#
# dis_feature1 = textdistance.hamming.normalized_distance(a[1], c[1])
#
# print("dis_feature1:",dis_feature1)




# import numpy as np
# import matplotlib.pyplot as plt
#
# # 生成一些示例数据
# x = np.linspace(0, 10, 100)
# y = np.sin(x)
#
# # 找到数据中的最小值
# y_min = np.min(y)
#
# # 设置 y 轴的范围，将下限设置为比最小值稍小的值
# plt.ylim(y_min - 0.1, 1.0)  # 0.1 是一个适当的偏移量，可以根据需要调整
#
# # 绘制数据
# plt.plot(x, y)
# plt.show()

import textdistance
a =[[0, 8, 18], ['030000', '02f080', '00']]
b = [[0, 8, 16], ['030000', '02f080', '0300']]
c = [[0, 8, 17], ['03000', '2f0807', '30']]
d = [[0, 4, 12], ['3d', '000000', 'ff']]
# dis1 = textdistance.cosine.distance(a[0],b[0])
# print('dis1 = ',dis1)
# dis2 = textdistance.damerau_levenshtein.normalized_distance(a[1],b[1])
# print('dis2 = ',dis2)


# array1 =[[[0, 8, 16, 26, 31, 36], ['030000', '02f080', '010000', '000', '000', '000']],\
#         [[0, 8, 16, 26, 31], ['030000', '02f080', '030000', '000', '0000']], \
#         [[0, 8, 16, 26, 31, 39], ['030000', '02f080', '010000', '000', '000040', '20a10']], \
#         [[0, 8, 16, 26, 34], ['030000', '02f080', '030000', '000200', '000004']], \
#         [[0, 8, 16, 26, 31, 36], ['030000', '02f080', '010000', '000', '000', '000']],\
#         [[0, 8, 16, 26, 31], ['030000', '02f080', '030000', '000', '0000']],\
#         [[0, 8, 16, 26, 30, 35, 39], ['030000', '02f080', '010000', '00', '002', '50', '20a10']], \
#         [[0, 8, 16, 26, 34, 42], ['030000', '02f080', '030000', '000200', '000005', 'ff']], \
#         [[0, 8, 16, 26, 34, 42], ['030000', '02f080', '010000', '002600', '040312', '10']], \
#         [[0, 8, 16, 26, 34, 42], ['030000', '02f080', '030000', '000200', '000004', 'ff']],]
# array2 =[[[0, 8, 16, 26], ['030000', '02f080', '010000', '000']],\
#         [[0, 8, 16, 26], ['030000', '02f080', '030000', '000']], \
#         [[0, 8, 16, 26], ['030000', '02f080', '010000', '000', ]], \
#         [[0, 8, 16, 26], ['030000', '02f080', '030000', '000200',]], \
#         [[0, 8, 16, 26], ['030000', '02f080', '010000', '000']],\
#         [[0, 8, 16, 26], ['030000', '02f080', '030000', '000']],\
#         [[0, 8, 16, 26], ['030000', '02f080', '010000', '00']], \
#         [[0, 8, 16, 26], ['030000', '02f080', '030000', '000200']], \
#         [[0, 8, 16, 26], ['030000', '02f080', '010000', '002600']], \
#         [[0, 8, 16, 26], ['030000', '02f080', '030000', '000200']],]
# import numpy as np
# #
# def generate_distance_matrix(data):
#     """
#     生成距离矩阵的函数
#
#     参数：
#         data：包含数据点的列表或数组
#
#     返回：
#         distance_matrix：距离矩阵
#     """
#     num_points = len(data)
#     distance_matrix = np.zeros((num_points, num_points))
#
#     # 计算每对数据点之间的距离，并填充距离矩阵
#     for i in range(num_points):
#         for j in range(num_points):
#             # 在这里根据自定义的距离计算方式计算距离
#             dis1 =textdistance.cosine.distance(data[i][0], data[j][0])
#             dis2 = textdistance.levenshtein.distance(data[i][1], data[j][1])
#             distance = (dis1 +dis2)/2
#             distance_matrix[i][j] = distance
#
#     return distance_matrix
#
# # 生成距离矩阵
# array1 = [a,b,c,d]
# distance_matrix = generate_distance_matrix(array1)
#
# print("距离矩阵：")
# print(distance_matrix)
#
# import matplotlib.pyplot as plt
# def plot_distance_matrix(distance_matrix):
#     plt.imshow(distance_matrix, cmap='hot', interpolation='nearest')
#     plt.colorbar()
#     plt.title('Distance Matrix')
#     plt.xlabel('Data Points')
#     plt.ylabel('Data Points')
#     # 在每个单元格内添加文本标签
#     num_points = distance_matrix.shape[0]
#     for i in range(num_points):
#         for j in range(num_points):
#             plt.annotate(str(round(distance_matrix[i, j], 2)), xy=(j, i),
#                          horizontalalignment='center', verticalalignment='center',
#                          color='blue')
#     plt.show()

# plot_distance_matrix(distance_matrix)

# a = [300,300,300,300,300]
# b = [368,325,674,115,1968,495]
# def true_label(index,label_list:list):
#     true_label = []
#     cur_label = 0
#     for i in range(0,index):
#         temp_label = [cur_label]*label_list[i]
#         true_label +=temp_label
#         cur_label +=1
#     return true_label
#
# true_label = true_label(3,a)
# print(true_label)

x = 5  # 你想要的长度

# 生成二维空列表
empty_2d_list =[]
empty_2d_list = [[None] * 2 for _ in range(x)]

empty_2d_list[1] =[1,2]
# 打印结果
print(empty_2d_list)