from preprocess import PcapData
import math
from matplotlib.pyplot import plot as plt
class Ngram(PcapData):
    def __init__(self):
        super(Ngram, self).__init__()
        #PcapData.__init__(self)
        self.n1_to_n2_ngram_loction_dict = {}  # {1:[(ngram,loc)],2:[(ngram,loc)]...}按照n-gram大小存储
        self.packet1_to_packet2_ngram_loction_dict = []  # [{1:[(ngram,loc)]}]
        self.all_ngam_loction = []  # [(ngram, loction)...]
        self.ngram_loction_count = {}  # {(ngram,loc):count}
        self.n1_to_n2_ngram_loction_count = {}  # {1:{(ngram,loc):count}}
        self.ngram_loction_count_filtered_by_support = {}
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
        for packet in self.packets_removed_other_information_bin:
            self.ngram_loction(packet, start_end)

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

    def filter_by_support(self, support: float):
        filter_ngram_loction_count = {}
        threshold = support * len(self.packet1_to_packet2_ngram_loction_dict)
        # print(len(self.packet1_to_packet2_ngram_loction_dict))
        # print(threshold)
        for n, ngram_loc_counts in self.n1_to_n2_ngram_loction_count.items():
            if n not in self.n1_to_n2_ngram_loction_count_filtered_by_support:
                self.n1_to_n2_ngram_loction_count_filtered_by_support[n] = {}
            for ngram_loc, count in ngram_loc_counts.items():
                if count >= threshold:
                    self.n1_to_n2_ngram_loction_count_filtered_by_support[n][ngram_loc] = count
                    self.ngram_loction_count_filtered_by_support[ngram_loc] = count

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