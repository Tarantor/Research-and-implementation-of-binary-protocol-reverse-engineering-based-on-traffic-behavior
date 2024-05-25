import csv
from time import *
from chapter4.processing import Processing
from ngram import Ngram
import chapter3.KANN_DbScan
import chapter3.dbscan_utility
import  numpy as np
from dbscan_utility import *
import time

a = [300,300,300,300,300]
b = [367,325,674,115,1968,495]
def true_label(index,label_list:list):
    true_label = []
    cur_label = 0
    for i in range(0,index):
        temp_label = [cur_label]*label_list[i]
        true_label +=temp_label
        cur_label +=1
    return true_label

if __name__ == '__main__':

    ngram = Ngram()
    index = 4
    true_label = true_label(index, a)
    ngram.read_csv_data_to_list("./pure_data_gram_300/filter_database{}.csv".format(index))
    # print(ngram.packets_removed_other_information)
    ngram.ngram((2, 6))
    ngram.count_ngram_loction()
    ngram.creat_loc_n_gram_database()
    # print(ngram.n1_to_n2_ngram_loction_base)

    # ngram.filter_by_threshold(0.1)
    # print(ngram.n1_to_n2_ngram_loction_base)
    # ngram.generate_Eigen_vectors((2,6))

    #动态生成
    start = time.perf_counter()
    ngram.D_generate_Eigen_vectors(thre=0.9,gram=(2,4),model=2,step =0.5,type_mode=0)
    end = time.perf_counter()
    print(ngram.Cluster_Vector_sum)
    print('finish generate_Eigen_vectors in %s s of %s' % (str(end - start), 'filter_database{}'.format(index)))
    chapter3.KANN_DbScan.kannDbscan(ngram.Cluster_Vector_sum,'filter_database{}'.format(index),ngram.packets_removed_other_information,100,true_label)
    # print( ClusterNumberList_bestK,EpsCandidate_bestK,MinptsCandidate_bestK)


