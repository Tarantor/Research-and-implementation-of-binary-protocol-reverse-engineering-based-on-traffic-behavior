# -*- coding: utf-8 -*-
#  creating on Oct 21 2019
import textdistance
import time
import math
import copy
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from chapter3.dbscan_utility import *
from chapter3.utility import Utility
from scipy.ndimage import gaussian_filter
from sklearn.metrics.cluster import homogeneity_completeness_v_measure, fowlkes_mallows_score
import matplotlib

matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus']=False     # 正常显示负号
def loadDataSet(fileName, splitChar='\t'):
    """
    description: 从文件读入数据集
    :param fileName: 文件名
    :param splitChar: 字符串分隔符
    :return: 数据集
    """
    dataSet = []
    with open(fileName) as fr:
        for line in fr.readlines():
            curline = line.strip().split(splitChar)
            fltline = list(map(float, curline))
            dataSet.append(fltline)
    return dataSet

def loadDataSetComplication(fileName, splitChar='\t'):
    """
    description: 从文件读入数据集
    :param fileName: 文件名
    :param splitChar: 字符串分隔符
    :return: 数据集
    """
    dataSet = []
    with open(fileName) as fr:
        for line in fr.readlines():
            curline = line.strip().split(splitChar)
            fltline = list(curline)
            formatData(fltline)
            dataSet.append(fltline)
    return dataSet

def dataToRightType(rowList):#这个函数暂时没用
    rowListLength = len(rowList)
    for i in range(rowListLength):
        try:
            rowList[i]=float(rowList[i])
        except BaseException:
            #do nothing
            rowList[i] = rowList[i]

def formatData(rowList):
    baseList = ['DAY','EVENING','MIDNIGHT','ARSON','ASSAULT W/DANGEROUS WEAPON','BURGLARY','HOMICIDE','MOTOR VEHICLE THEFT','ROBBERY','SEX ABUSE','THEFT F/AUTO','THEFT/OTHER']
    #索引0~2为时间段：白天，晚上，半夜
    #索引3~11为犯罪类型：纵火，使用危险武器攻击，入室盗窃，蓄意杀人，机动车盗窃，抢劫，性虐待，汽车盗窃，其他盗窃
    rowListLength = len(rowList)
    for i in range(rowListLength):
        if baseList.__contains__(rowList[i]):
            rowList[i] = baseList.index(rowList[i])+1
        else:
            rowList[i] = float(rowList[i])

def dist(a,b):
    """
    description: 用来计算两个样本点之间的距离
    :param a: 样本点
    :param b: 样本点
    :return: 两个样本点之间的距离
    """
    return math.sqrt(math.pow(a[0]-b[0],2) + math.pow(a[1]-b[1],2))
# levenshtein距离能够计算差异这里用的是相似度
def levenshteinDistance_lev(str1:list, str2:list):
    '''
    编辑距离——莱文斯坦距离,计算文本的相似度
    '''
    m = len(str1)
    n = len(str2)
    lensum = float(m + n)
    d = []
    if lensum == 0:  # 处理 lensum 为 0 的情况
        return 10
    for i in range(m+1):
        d.append([i])
    del d[0][0]
    for j in range(n+1):
        d[0].append(j)
    for j in range(1,n+1):
        for i in range(1,m+1):
            if str1[i-1] == str2[j-1]:
                d[i].insert(j,d[i-1][j-1])
            else:
                minimum = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+textdistance.levenshtein.normalized_distance(str1[i-1],str2[j-1]))
                d[i].insert(j, minimum)
    ldist = d[-1][-1]
    return ldist

def returnDk(matrix,k):
    """
    description: 用来计算第K最近的距离集合
    :param matrix: 距离矩阵
    :param k: 第k最近
    :return: 第k最近距离集合
    """
    Dk = []
    for i in range(len(matrix)):
        Dk.append(matrix[i][k]) #取出每一行的第k列
    return Dk


def returnDkAverage(Dk):
    """
    description: 求第K最近距离集合的平均值
    :param Dk: k-最近距离集合
    :return: Dk的平均值
    """
    sum = 0
    for i in range(len(Dk)):
        sum = sum + Dk[i]
    return sum/len(Dk)


def CalculateDistMatrix(dataset): #对KANN来说必须先求距离矩阵，
    """
    description: 计算距离矩阵
    :param dataset: 数据集
    :return: 距离矩阵
    """
    DistMatrix = [[0 for j in range(len(dataset))] for i in range(len(dataset))]    #建立一个dataSet大小的list
    for i in range(len(dataset)):
        for j in range(len(dataset)):
            a = textdistance.cosine.normalized_distance(dataset[i][0], dataset[j][0])
            b = textdistance.levenshtein.normalized_distance(dataset[i][1], dataset[j][1])
            if b == 0 :
                b = 0.1
            dis =a + b
            DistMatrix[i][j] = dis
    return DistMatrix


def returnEpsCandidate(dataSet, DistMatrix):
    """
    description: 计算Eps候选列表
    :param dataSet: 数据集
    :return: eps候选集合
    """
    #DistMatrix = CalculateDistMatrix(dataSet)
    tmp_matrix = copy.deepcopy(DistMatrix)#对象拷贝，深拷贝，相当于完全复制了一个新的对象
    for i in range(len(tmp_matrix)):
        tmp_matrix[i].sort()    #对每一行元素进行升序排列，即找到该行的第1~n近邻元素
    EpsCandidate = []   #排序完，第i**列**即为所有点的第i近邻距离，此时对所有点第i近邻取平均，得到第i平均近邻，作为Eps的候选项
    for k in range(1,len(dataSet)):
        Dk = returnDk(tmp_matrix,k) #第K近邻距离集合
        DkAverage = returnDkAverage(Dk) #第K近邻的平均距离，求均值
        if DkAverage ==0:
            DkAverage =0.1
        EpsCandidate.append(DkAverage)  #把求到的平均值塞进EpsCandidate里面
    return EpsCandidate


def returnMinptsCandidate(DistMatrix,EpsCandidate):
    """
    description: 计算Minpts候选列表
    :param DistMatrix: 距离矩阵
    :param EpsCandidate: Eps候选列表
    :return: Minpts候选列表
    """
    EpsLenth = len(EpsCandidate)
    MinptsCandidate = []
    for k in range(EpsLenth):
        tmp_eps = EpsCandidate[k]
        tmp_count = 0
        for i in range(len(DistMatrix)):
            for j in range(len(DistMatrix[i])):
                if DistMatrix[i][j] <= tmp_eps:
                    tmp_count = tmp_count + 1
        MinptsCandidate.append(tmp_count/(10*EpsLenth))  #求平均
    return MinptsCandidate


def returnClusterNumberList(dataset,EpsCandidate,MinptsCandidate): #生成最终聚类簇
    """
    description: 计算聚类后的类别数目 
    :param dataset: 数据集
    :param EpsCandidate: Eps候选列表
    :param MinptsCandidate: Minpts候选列表
    :return: 聚类数量列表
    """
    np_dataset = np.array(dataset)  #将dataset转换成numpy_array的形式，多维数组
    ClusterNumberList = []
    for i in range(len(EpsCandidate)):
        modle = DBSCAN(eps= EpsCandidate[i],min_samples= MinptsCandidate[i] ,metric='precomputed')    #这里是调用的DBSCAN类生成一个DBSCAN对象,生成DBSCAN聚类模型；可以选择另一种做法直接调用dbscan方法，结果一样
        clustering = modle.fit(np_dataset)  #对数据集进行聚类，要求数据集形状（n_samples，n_features）的数组或稀疏矩阵，返回值仍然是一个DBSCAN对象
        #clustering = modle.fit(dataSet)
        num_clustering = max(clustering.labels_) + 1    #.labels_ 为DBSCAN的聚类标签，也就是每一个类的序号(从0开始)，取最大值，即为聚类数目
        ClusterNumberList.append(num_clustering)    #把聚类数量放进list里面
    return ClusterNumberList

def returnDensity(Eps, Minpts):
    """
    description: 计算候选列表的密度阈值，density = MinPtds/(ΠEps²)
    :param Eps: Eps候选列表
    :param Minpts: Minpts候选列表
    :return: 对应的密度阈值列表
    """
    density = []
    # if(len(Eps) == len(Minpts)):
    #     for i in range(len(Eps)):
    #         density_tmp_value = Minpts[i]/(math.pi*Eps[i]*Eps[i])
    #         density.append(density_tmp_value)
    if len(Eps) == len(Minpts):
        for i in range(len(Eps)):
            if Eps[i] == 0:
                density.append(0.01)  # 如果 Eps[i] 为零，则将对应的密度阈值设为零
            else:
                density_tmp_value = Minpts[i] / (math.pi * Eps[i] * Eps[i])
                density.append(density_tmp_value)
    return density

def showInitPoint(data):
    """
    description: 将数据集初始化以散点图显示出来
    :param data: 数据集列表
    :return: 
    """
    data = np.mat(data).transpose()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(data[0, :].flatten().A[0], data[1, :].flatten().A[0], c='black', s=5)
    plt.show()


def showRelationLineChart(y_data, y_name = "Eps"):
    """
    description: 将给定的数据列表以折线图形式画出
    :param y_data: 数据列表，纵坐标取值集合
    :param y_name: y轴名
    :return: 
    """
    x=range(len(y_data))
    plt.grid(linestyle='--')  # 生成网格,网格线样式为 端虚线
    plt.plot(x,y_data)
    #plt.plot()  x是可选的，如果x没有，将默认是从0到n-1，也就是y_data的索引，maker为目标点显示样式，mec(全名markeredgecolor)，也就是maker的边缘颜色
    #plt.xticks(x, dividedByScale(x,scale = getScale(len(x))))    #第一个参数表示坐标轴上对应位置，第二个参数表述第一个参数表示位置上显示的值,如([0,3],[1,4]),表示0~3位置上显示1~4
    #真辛酸，上面那根本没有必要，也算是踩一个坑吧
    plt.margins(0)  #设置或获取自动缩放量，挺重要的，要不很难看
    #plt.subplots_adjust(bottom=0.10)    #调整子图布局。
    plt.xlabel('K值') #X轴标签
    plt.ylabel(y_name) #Y轴标签
    #pyplot.yticks() #可以设置y轴的范围，默认是最小和最大值之间的区间，这里没必要设置
    plt.show()
    
def returnBestClusterNum(ClusterNumberList, expectConstantTimes = 10):
    """#当前这种写法个人不太满意，这样求出来的稳定值并不够好，因为上限就到10，如果这个值稳定了100次，也仅局限在前10次，就很不好，改进空间很大（可以增设变量，使用延时判断，判断上一个区间的稳定性而不是立刻判断当前区间的稳定性）
    description: 求聚类结果"收敛(稳定)"时，包含的簇的个数。定义默认连续10次聚类结果在不大于1的区间内波动算作稳定，如果无法找到稳定区间则缩短稳定区间定义，递归调用本函数，直到找到最佳连续为止
    :param ClusterNumberList: K值对应的聚类簇
    :param expectConstantTimes: 期望最小连续数，作为最佳聚类簇数
    :return: 
    """
    constantTimes = 1
    startIndex = endIndex = 0   #索引值取稳定区间的中位数，若为小数则向上取证
    sectionMax = sectionMin = ClusterNumberList[0]
    for i in range(1,len(ClusterNumberList)):
        if (abs(ClusterNumberList[i] - sectionMin) > 1) or (abs(ClusterNumberList[i] - sectionMax) > 1):
            sectionMax = ClusterNumberList[i]
            sectionMin = ClusterNumberList[i]
            constantTimes = 1
            startIndex = i
            endIndex = i
        else:
            if ClusterNumberList[i] < sectionMin:
                sectionMin = ClusterNumberList[i]
            elif ClusterNumberList[i] > sectionMax:
                sectionMax = ClusterNumberList[i]
            constantTimes += 1
            endIndex = i
        if constantTimes >= expectConstantTimes:
            break;

    maxConstantTimesIndex = math.ceil((endIndex + startIndex)/2)
    if constantTimes < expectConstantTimes:
        constantTimes, maxConstantTimesIndex = returnBestClusterNum(ClusterNumberList, expectConstantTimes-1)
    
    #print("StartIndex:",startIndex)
    #print("endIndex:",endIndex)
    return constantTimes, maxConstantTimesIndex

def plot_distance_matrix(distance_matrix):
    plt.imshow(distance_matrix, cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.xlabel('数据点')
    plt.ylabel('数据点')
    plt.show()

def kannDbscan(dataSet, dimesionName,data_array,expectConstantTimes,true_label):
    """
    description: 进行KANN-DBSCAN,
    :param dataSet: 输入的数据集，以二维列表形式
    :return: 返回最优聚类簇数以及两个对应的DBScab参数eps和minPts
    """
    cur_index =len(dataSet)
    print(cur_index)
    start = time.perf_counter()
    print("Start KANN-DBSCAN of "+dimesionName)
    # showInitPoint(dataSet)     #把初始点先画出来

    DistMatrix = CalculateDistMatrix(dataSet)   #获得距离矩阵，方便用KANN
    plot_distance_matrix(DistMatrix)
    end = time.perf_counter()
    print('finish Calculate Distance Matrix in %s s of %s' % (str(end - start),dimesionName))
    print(len(DistMatrix))


    # result = DBSCAN_CLUSTER(distance=DistMatrix, eps=0.12273333333333043, minpts=40.23575717144763)
    # homogeneity, completeness, v_measure_score = homogeneity_completeness_v_measure(true_label, result['db_labels'])
    # fmi = fowlkes_mallows_score(true_label, result['db_labels'])
    # la = {}
    # for l in result['db_labels']:
    #     if l not in la:
    #         la[l] = 0
    #     la[l] += 1
    # if la.__contains__(-1):
    #     noise = la[-1]
    # else:
    #     noise = 0
    # coverage = 1 - noise / cur_index
    # print(result)
    # print('homogeneity:', homogeneity, 'completeness:', completeness, 'v_measure_score:', v_measure_score, 'fmi:', fmi,
    #       'coverage:', coverage)


    EpsCandidate = returnEpsCandidate(dataSet, DistMatrix)  #获得Eps候选集
    smoothed_distance_matrix_E = gaussian_filter(EpsCandidate, sigma=5)
    showRelationLineChart(smoothed_distance_matrix_E, "Eps of "+dimesionName)    #画出K与Eps候选集的关系
    end = time.perf_counter()
    print('finish Eps Candidates in %s s of %s' % (str(end - start),dimesionName))

    MinptsCandidate = returnMinptsCandidate(DistMatrix,EpsCandidate)
    smoothed_distance_matrix_M = gaussian_filter(MinptsCandidate, sigma=5)#获得MinPts候选集
    showRelationLineChart(smoothed_distance_matrix_M, "MinPts of "+dimesionName)    #画出K与MinPts候选集的关系
    end = time.perf_counter()
    print('finish Minpts Candidates in %s s of %s' % (str(end - start),dimesionName))

    Density = returnDensity(EpsCandidate, MinptsCandidate)
    smoothed_distance_matrix_D = gaussian_filter(Density, sigma=5)
    showRelationLineChart(smoothed_distance_matrix_D, "Density Result of "+dimesionName)    #画出K与Density的关系
    end = time.perf_counter()
    print('finish Density in %s s of %s' % (str(end - start),dimesionName))

    ClusterNumberList = returnClusterNumberList(DistMatrix,EpsCandidate,MinptsCandidate)   #获得最终聚类结果
    smoothed_distance_matrix_C = gaussian_filter(ClusterNumberList, sigma=5)
    showRelationLineChart( smoothed_distance_matrix_C, "Cluster Result Number of "+dimesionName)   #画出K与最终聚类结果聚类簇数的关系
    end = time.perf_counter()
    print('finish Cluster List in %s s of %s' % (str(end - start),dimesionName))

    maxConstantTimes, bestK = returnBestClusterNum(ClusterNumberList, expectConstantTimes = expectConstantTimes)
    end = time.perf_counter()
    print('finish find best parameter and all in %s s of %s' % (str(end - start),dimesionName))
    print("ClusterNumberList_best:",ClusterNumberList[bestK],"EpsCandidate_best:",EpsCandidate[bestK],"MinptsCandidate_best:",MinptsCandidate[bestK])
    result = DBSCAN_CLUSTER(distance= DistMatrix, eps=EpsCandidate[bestK], minpts= MinptsCandidate[bestK])
    homogeneity, completeness, v_measure_score = homogeneity_completeness_v_measure(true_label,result['db_labels'])
    fmi = fowlkes_mallows_score(true_label, result['db_labels'])
    la = {}
    for l in result['db_labels']:
        if l not in la:
            la[l] = 0
        la[l] += 1
    if la.__contains__(-1):
        noise = la[-1]
    else:
        noise = 0
    coverage = 1 - noise / cur_index
    print(result)
    print('homogeneity:',homogeneity,'completeness:',completeness,'v_measure_score:',v_measure_score,'fmi:',fmi,'coverage:',coverage)
    data = []
    for row in data_array:
        data.append(bytes.fromhex(row))
    data_vector = Utility.data_list2vector(data)
    aligned_data = Utility.align_vector(20, data_vector)
    plot_dbscan_result(aligned_data,result['db_labels'],result['unique_labels'])
    # return ClusterNumberList[bestK],EpsCandidate[bestK],MinptsCandidate[bestK]
        
    
    
    