from preprocess import PcapData
import math
from matplotlib.pyplot import plot as plt
import copy
class Ngram(PcapData):
    def __init__(self):
        super(Ngram, self).__init__()
        #PcapData.__init__(self)
        self.n1_to_n2_ngram_loction_dict = {}  # {1:[(ngram,loc)],2:[(ngram,loc)]...}按照n-gram大小存储
        self.packet1_to_packet2_ngram_loction_dict = []  # [{1:[(ngram,loc)]}]
        self.all_ngam_loction = []  # [(ngram, loction)...]
        self.ngram_loction_count = {}  # {(ngram,loc):count}
        self.n1_to_n2_ngram_loction_count = {}  # {1:{(ngram,loc):count}}
        self.message_Eigen_vectors=[]
        self.Cluster_Vector_sum = []
        self.ngram_loction_count_filtered_by_support = {}
        self.n1_to_n2_ngram_loction_base = {}
        self.n1_to_n2_ngram_loction_count_filtered_by_support = {}
        self.bound_candidate = set()  # 所有候选边界混在一起
        self.n1_to_n2_bound_candidate = {}  # 按n分类的候选集边界
        self.hit_count = {}  # 统计命中数，{loc: count}
        self.hit_rate = {}  # 命中率， {loc, rate}
        self.branch_metric = {}  # {i: metric}
        self.i_to_j_ngram_change_rate = {}  # {(i,j):} 暂时n取3，所以就不详细记录n了
        self.change_rate_var = {}  # {(i, j):var}
        self. packets_removed_other_information_bin = []
        self.evaluate_score = []
        self.deduced_boundarys_cluster = []
        self.loc_count = []
    # 对每个package进行多个不同切片大小切片
    def ngram_loction(self, packet: str, start_end: tuple) -> list:
        this_packet_n1_to_n2_ngram_loction_dict = {}#按照数据包存储
        for n in range(start_end[0], start_end[1] + 1, 1):
            if n not in self.n1_to_n2_ngram_loction_dict:
                self.n1_to_n2_ngram_loction_dict[n] = []
            if n not in this_packet_n1_to_n2_ngram_loction_dict:
                this_packet_n1_to_n2_ngram_loction_dict[n] = []
            length = len(packet)
            for loc in range(0, length - n + 1):  # 对字符串滑动窗口切片
                ngram = packet[loc: loc + n]  # 切片
                n_l = (ngram, loc)  # ngram-loction，从0开始计数
                self.all_ngam_loction.append(n_l)  # 加入到所有ngram-loc统计里面去
                this_packet_n1_to_n2_ngram_loction_dict[n].append(n_l)  # 以packet进行分类存储
                self.n1_to_n2_ngram_loction_dict[n].append(n_l)  # 以n进行分类存储
            self.packet1_to_packet2_ngram_loction_dict.append(this_packet_n1_to_n2_ngram_loction_dict)  # 与packet列表一一对应

    # 按packet顺序切片
    def ngram(self, start_end: tuple) -> list:
        for packet in self.packets_removed_other_information:
            self.ngram_loction(packet, start_end)

    #提取报文集针对每个字段的频繁项集合

    # todo: 方案一：主动，去用ngram去匹配，方案二：被动，去统计每个packet中的ngram
    def count_ngram_loction(self) -> object:
        for n, ngram_loctions in self.n1_to_n2_ngram_loction_dict.items():#返回的是n-gram,和ngram_loctions
            if n not in self.n1_to_n2_ngram_loction_count:
                self.n1_to_n2_ngram_loction_count[n] = {}
            for ngram_loction in ngram_loctions:
                if ngram_loction not in self.ngram_loction_count:
                    self.ngram_loction_count[ngram_loction] = 0
                if ngram_loction not in self.n1_to_n2_ngram_loction_count[n]:
                    self.n1_to_n2_ngram_loction_count[n][ngram_loction] = 0
                self.ngram_loction_count[ngram_loction] += 1
                self.n1_to_n2_ngram_loction_count[n][ngram_loction] += 1

    # 以位置为基准建立数据集的n-gram库(0, 80): {'81': 16, '810': 16, '810a': 16, '810a0': 16, '810a00': 16}(位置，该位置总次数)：{字段：字段出现次数}
    def creat_loc_n_gram_database(self) -> None:
        for (ngram, loc), count in self.ngram_loction_count.items():
            if loc not in self.n1_to_n2_ngram_loction_base:
                self.n1_to_n2_ngram_loction_base[loc] = {}
            self.n1_to_n2_ngram_loction_base[loc][ngram]=count
        position_counts = {}
        for position, data in self.n1_to_n2_ngram_loction_base.items():
            total_count = sum(data.values())
            position_counts[position] = total_count
        new_data = {}
        for position, data in self.n1_to_n2_ngram_loction_base.items():
            total_count = position_counts[position]
            new_key = position
            new_data[new_key] = data
        self.n1_to_n2_ngram_loction_base.clear()
        self.n1_to_n2_ngram_loction_base=new_data

    # 筛选频繁项
    def filter_by_threshold(self,thre):
        keys_to_delete = []  # 用于存储要删除的键
        thea = thre * len(self.packets_removed_other_information)
        for loc, gram_count in self.n1_to_n2_ngram_loction_base.items():
            for gram, count in gram_count.items():
                n = len(gram)
                if count <= thea:
                    keys_to_delete.append((loc,gram))  # 将要删除的键添加到列表中
        # 删除键值对
        for key in keys_to_delete:
            loc, gram = key
            self.n1_to_n2_ngram_loction_base[loc].pop(gram)

    #生成特征向量CV
    def generate_Eigen_vectors(self,gram:tuple):
        for message in self.packets_removed_other_information:
            length = len(message)
            loc = 0
            Length_Vector=[]
            Frequence_Candidates=[]
            while loc+gram[0] <= length:
                for i in range(gram[1],gram[0]-1,-1):
                    if loc + i  <= length:
                        gram_1 = message[loc:loc+i]
                    else:
                        gram_1 = message[loc:length]
                    if gram_1 in self.n1_to_n2_ngram_loction_base[loc]:#最长匹配原则
                        Length_Vector.append(loc)
                        Frequence_Candidates.append(message[loc:loc+i])
                        loc += i
                        break
                loc+=gram[1]
            self.Cluster_Vector_sum.append([Length_Vector, Frequence_Candidates])

    #动态生成频繁项列表
    def D_filter_by_threshold(self,thre):
        keys_to_delete = []  # 用于存储要删除的键
        temp_n1_to_n2_ngram_loction_base =copy.deepcopy(self.n1_to_n2_ngram_loction_base)
        for loc, gram_count in temp_n1_to_n2_ngram_loction_base.items():
            for gram, count in gram_count.items():
                n = len(gram)
                thea = thre *len(self.packets_removed_other_information)
                if count <= thea:
                    keys_to_delete.append((loc,gram))  # 将要删除的键添加到列表中
        # 删除键值对
        for key in keys_to_delete:
            loc, gram = key
            temp_n1_to_n2_ngram_loction_base[loc].pop(gram)
        return temp_n1_to_n2_ngram_loction_base
    #动态生成特征向量CV
    def D_generate_Eigen_vectors(self, thre: float, gram: tuple, model: int,step :float,type_mode:bool):
        handle_threshold = 0.008 * len(self.packets_removed_other_information)

        # 初始阈值筛选
        temp_n1_to_n2_ngram_loction_base =copy.deepcopy( self.D_filter_by_threshold(thre))
        empty_value_count = 0
        for key, value in temp_n1_to_n2_ngram_loction_base.items():
            if not value:
                empty_value_count += 1
        while empty_value_count/len(self.packets_removed_other_information[0])>0.1 and type_mode ==0:
            thre = step *thre
            temp_n1_to_n2_ngram_loction_base = copy.deepcopy(self.D_filter_by_threshold(thre))
            empty_value_count = 0
            for key, value in temp_n1_to_n2_ngram_loction_base.items():
                if not value:
                    empty_value_count += 1

        # 初始化消息标记列表0为已标记，1为未标记
        message_none = [1] * len(self.packets_removed_other_information)
        self.Cluster_Vector_sum =[[None] * 2 for _ in range(len(self.packets_removed_other_information))]
        # 遍历每个消息
        for index, message in enumerate(self.packets_removed_other_information):
            length = len(message)
            loc = 0
            Length_Vector = []
            Frequence_Candidates = []

            # 遍历消息中的 n-gram
            while loc + gram[0] <= length:
                for i in range(gram[1], gram[0] - 1, -1):
                    if loc + i <= length:
                        gram_1 = message[loc:loc + i]
                    else:
                        gram_1 = message[loc:length]
                    if gram_1 in temp_n1_to_n2_ngram_loction_base[loc] and len(Length_Vector)< model:  # 最长匹配原则
                        Length_Vector.append(loc)
                        Frequence_Candidates.append(message[loc:loc + i])
                        loc += i
                        break
                    else:
                        loc += gram[0]
                        break

            # 判断是否满足模型要求
            if len(Length_Vector)< model:
                message_none[index] = 1
            else:
                self.Cluster_Vector_sum[index] = Length_Vector, Frequence_Candidates
                message_none[index] = 0
        if type_mode == 0 :
            # 处理剩余消息
            count = 0
            while sum(message_none) > handle_threshold and count<20:

                # 调整阈值
                thre = step * thre
                temp_n1_to_n2_ngram_loction_base = copy.deepcopy(self.D_filter_by_threshold(thre))
                count +=1
                # 遍历消息标记列表
                for index, value in enumerate(message_none):
                    if value == 1:
                        # 获取消息
                        current_message = self.packets_removed_other_information[index]
                        length = len(current_message)
                        loc = 0
                        Length_Vector = []
                        Frequence_Candidates = []

                        # 遍历消息中的 n-gram
                        while loc + gram[0] <= length:
                            for i in range(gram[1], gram[0] - 1, -1):
                                if loc + i <= length:
                                    gram_1 = current_message[loc:loc + i]
                                else:
                                    gram_1 = current_message[loc:length]
                                if gram_1 in temp_n1_to_n2_ngram_loction_base[loc] and len(Length_Vector)< model:  # 最长匹配原则
                                    Length_Vector.append(loc)
                                    Frequence_Candidates.append(current_message[loc:loc + i])
                                    loc += i
                                    break
                                else:
                                    loc += gram[0]
                                    break
                        if len(Length_Vector)< model :
                            message_none[index] = 1
                        else:
                            self.Cluster_Vector_sum[index] = [Length_Vector, Frequence_Candidates]
                            message_none[index] = 0
                    else:
                        continue
            #对剩余为负值的向量进行噪声处理
            for index, value in enumerate(message_none):
                if value == 1:
                    # 获取消息
                    current_message = self.packets_removed_other_information[index]
                    length = len(current_message)
                    loc = 0
                    Length_Vector = []
                    Frequence_Candidates = []

                    # 遍历消息中的 n-gram
                    while loc + gram[0] <= length:
                        for i in range(gram[1], gram[0] - 1, -1):
                            if loc + i <= length:
                                gram_1 = current_message[loc:loc + i]
                            else:
                                gram_1 = current_message[loc:length]
                            if gram_1 in self.n1_to_n2_ngram_loction_base[loc] and len(Length_Vector) < model:  # 最长匹配原则
                                Length_Vector.append(loc)
                                Frequence_Candidates.append(current_message[loc:loc + i])
                                loc += i
                                break
                            else:
                                loc += gram[0]
                                break
                    self.Cluster_Vector_sum[index] = [Length_Vector, Frequence_Candidates]
                    message_none[index] = 0
        else:
            return




    '''
    获取边界候选集
    '''

    def generate_bound_candidate(self) -> object:
        for n, ngram_loc_counts in self.n1_to_n2_ngram_loction_count_filtered_by_support.items():
            if n not in self.n1_to_n2_bound_candidate:
                self.n1_to_n2_bound_candidate[n] = set()
            for ngram_loc, count in ngram_loc_counts.items():
                self.bound_candidate.add(ngram_loc[1])
                self.bound_candidate.add(ngram_loc[1] + n - 1)
                self.n1_to_n2_bound_candidate[n].add(ngram_loc[1])
                self.n1_to_n2_bound_candidate[n].add(ngram_loc[1] + n - 1)

    def achieve_hit_count(self):
        for n, bound in self.n1_to_n2_bound_candidate.items():
            for boundary in bound:
                if boundary not in self.hit_count:
                    self.hit_count[boundary] = 0
                self.hit_count[boundary] += 1

    def achieve_hit_rate(self):
        n1_n2 = len(self.n1_to_n2_ngram_loction_count)
        #print("n1_n2:", n1_n2)
        for boundary, count in self.hit_count.items():
            self.hit_rate[boundary] = count / n1_n2

    # 分支度量
    def calculate_branch_metric(self, whr_whd: tuple):  # 权值
        for boundary, count in self.hit_count.items():
            self.branch_metric[boundary] = 1 / ((whr_whd[0] * self.hit_rate[boundary] +
                                                 whr_whd[1] * self.left_and_right_entropy_difference[boundary]))

    #
    # def i_to_j_ngram_change_rate_given_string(self, package_i_j_string: str, n: int) -> float:
    #     all_possible = math.pow(2, n)
    #     if len(package_i_j_string) < n:
    #         return 0
    #     for i in range(len(package_i_j_string) - n + 1):
    #         different_slice = set()
    #         for
    def calculate_var_i_j_n(self, i: int, j: int, n: int):
        all_possible = math.pow(2, n)
        sum_change_rate = 0
        for t, n_strings_change_rate in self.i_to_j_ngram_change_rate[(i, j)][0].items():
            #t_different_strings_number = 0
            self.i_to_j_ngram_change_rate[(i, j)][0][t][1] = \
                len(self.i_to_j_ngram_change_rate[(i, j)][0][t][0]) / all_possible
            sum_change_rate += self.i_to_j_ngram_change_rate[(i, j)][0][t][1]
        average_change_rate = sum_change_rate / (j - i - n + 2) # or len(i_to_j...)
        sum_var = 0
        for t, n_strings_change_rate in self.i_to_j_ngram_change_rate[(i, j)][0].items():
            sum_var += pow((n_strings_change_rate[1] - average_change_rate), 2)
        self.i_to_j_ngram_change_rate[(i, j)][1] = sum_var / (j - i - n + 2)

    #{(i,j):({0:({string1,string2},change_rate)}, change_rate_var)}
    def i_to_j_ngram_change_rate_given_i_j_n(self, i: int, j: int, n: int):
        if (i, j) not in self.i_to_j_ngram_change_rate:
            self.i_to_j_ngram_change_rate[(i, j)] = [{}, 0]
        if j - i + 1 >= n:
            for package in self.packets_removed_other_information_bin:
                package_i_j_string = package[i: j+1]  # 将i-j这一段先截取下来，也可以不截取下来
                for index in range(0, j-i-n+2):
                    if index not in self.i_to_j_ngram_change_rate[(i, j)][0]:
                        self.i_to_j_ngram_change_rate[(i, j)][0][index] = [set(), 0]
                   # print("PPPP",self.i_to_j_ngram_change_rate[(i, j)][0])
                    self.i_to_j_ngram_change_rate[(i, j)][0][index][0].add(
                        package_i_j_string[index: index+n])
            self.calculate_var_i_j_n(i, j, n)


    #
    def achieve_i_to_j_ngram_change_rate(self, n: int):
        bound_candidate_list = list(self.bound_candidate)
        for i in range(len(bound_candidate_list)):
           for j in range(i + 1, len(bound_candidate_list), 1):
                self.i_to_j_ngram_change_rate_given_i_j_n(bound_candidate_list[i], bound_candidate_list[j], n)
        for i_j, t_string_change_rate_var in self.i_to_j_ngram_change_rate.items():
            self.change_rate_var[i_j] = t_string_change_rate_var[1]

    #第一数字定律
    def get_boundary_score(self) -> list:
        self.evaluate_score = [[] for _ in range(len(self.packets_removed_other_information))]
        for i in range(0, len(self.packets_removed_other_information) - 1, 1):#packets_removed_other_information是message集合
            for j in range(0,len(self.packets_removed_other_information[i]) - 1, 1):#j表示位置
                first_byte2int = int(self.packets_removed_other_information[i][j],16)
                second_byte_first_half_byte = int(self.packets_removed_other_information[i][j + 1] ,16)// 16
                self.evaluate_score[i].append(first_byte2int * math.log(1 + 1 / (1 + second_byte_first_half_byte), 17))
        return self.evaluate_score
    #像拓展第一数字定律到二进制
    # def get_boundary_score_2(self) -> list:
    #     self.evaluate_score = [[] for _ in range(len(self.packets_removed_other_information_bin))]
    #     for i in range(0, len(self.packets_removed_other_information_bin) - 1, 1):#packets_removed_other_information是message集合
    #         for j in range(0,len(self.packets_removed_other_information[i]) - 1, 1):#j表示位置
    #             first_byte2int = bin(self.packets_removed_other_information[i][j],16)[2:]
    #             second_byte_first_half_byte = int(self.packets_removed_other_information[i][j + 1] ,16)// 16
    #             self.evaluate_score[i].append(first_byte2int * math.log(1 + 1 / (1 + second_byte_first_half_byte), 17))
    #     return self.evaluate_score

    def calculate_branch_metric_v2(self, whr_whd: tuple):  # 权值
        for boundary, count in self.hit_count.items():
            self.branch_metric[boundary] = 1 / ((whr_whd[0] * self.hit_rate[boundary] +
                                                 whr_whd[1] * self.left_and_right_entropy_difference[boundary]))