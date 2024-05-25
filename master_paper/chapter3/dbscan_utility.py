import logging

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from sklearn import decomposition
from sklearn.cluster import DBSCAN
def DBSCAN_CLUSTER(distance: np.ndarray, eps: float, minpts: int) -> dict:
    db = DBSCAN(eps=eps, min_samples=minpts, metric="precomputed")
    try:
        db.fit(distance)
    except Exception as err:
        print(err)
        ret = {
            'cluster_nums': 0,
            'db_labels': None,
            'unique_labels': None,
            'cluster_center': None
        }
        return ret
    db_labels = db.labels_
    unique_labels = np.unique(db_labels)  # 获得唯一的类别
    cluster_nums = len(unique_labels)
    cluster_center = db.components_
    ret = {
        'cluster_nums': cluster_nums,
        'db_labels': db_labels,
        'unique_labels': unique_labels,
        'cluster_center': cluster_center
    }
    return ret

def print_label_res(result: dict):
    labels = result['db_labels']
    la = {}
    for l in labels:
        if l not in la:
            la[l] = 0
        la[l] += 1
    print(la)

# def plot_dbscan_result(data, db_labels, unique_labels):
#     # cmap = plt.colormaps.get_cmap("Spectral")
#     cmap = cm.get_cmap("Spectral")
#     colors = cmap(np.linspace(0, 1, len(unique_labels)))
#     pca = decomposition.PCA(n_components=10)
#     features = pca.fit_transform(data)
#     # features = StandardScaler().fit_transform(data)
#     # for i in range(0, 9):
#     #     for j in range(i+1, 10):
#     plt.rcParams['font.sans-serif'] = ['Times New Roman']
#     plt.xticks(fontsize=20)
#     plt.yticks(fontsize=20)
#     for k, color in zip(unique_labels, colors):
#         if k == -1:
#             color = 'k'  # 黑色代表噪声
#         index = np.where(db_labels == k)  # 获得每一个类别的坐标
#         x = features[index]
#         plt.tick_params(labelsize=20)
#         plt.plot(x[:, 0], x[:, 7], 'o', markerfacecolor=color, markeredgecolor=None, markersize=6)
#
#
#     plt.show()

def plot_dbscan_result(data, db_labels, unique_labels):
    cmap = cm.get_cmap("Spectral")
    colors = cmap(np.linspace(0, 1, len(unique_labels)))
    pca = decomposition.PCA(n_components=5)
    features = pca.fit_transform(data)

    plt.rcParams['font.sans-serif'] = ['Times New Roman']
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    for k, color in zip(unique_labels, colors):
        if k == -1:
            color = 'k'  # 黑色代表噪声
        index = np.where(db_labels == k)  # 获得每一个类别的坐标
        x = features[index]
        plt.tick_params(labelsize=20)
        plt.plot(x[:, 0], x[:, 4], 'o', markerfacecolor=color, markeredgecolor=None, markersize=6, label=f'Cluster {k}')

    plt.legend(title='Cluster Labels', title_fontsize='large', fontsize='medium')  # 添加图例和标题
    plt.show()


