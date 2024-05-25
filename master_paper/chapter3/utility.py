"""
十六进制字符串转化为二进制字符串，例如"1a"->"00011010"
"""


def hex2bin(hex_str: str):
    new_hex_str = "1" + hex_str
    hex_int = bin(int(new_hex_str, 16))[3:]
    return hex_int


# todo:
#  方案一：因为n知道，所以ngram的可能性都确定了，共有2^n种。优点简单，但是ngram不会减少为最大值2^n
#  方案二：直接从切片的数据合并去重得到所有ngram，优点就是ngram种类<=2^n


'''
判断在一个packet上是否在loction+_theta上有指定ngram
'''


def judge_packet_hava_ngram_loction_theta(packet_removed_other_information_bin: set, ngram_loction: tuple,
                                          theta: int) -> bool:
    # length = len(packet)
    for loction in range(ngram_loction[1] - theta, ngram_loction[1] + theta + 1, 1):
        if (ngram_loction[0], loction) in packet_removed_other_information_bin:  # 在一个范围内存在这个ngram
            return True  # 有一个符合就行了
    return False


'''
给定一个切片类型集合，统计其中每种切片的数量
'''


# todo: 方案一：主动，去用ngram去匹配，方案二：被动，去统计每个packet中的ngram
def count_ngram_loction(all_ngram_loc: list, theta=0) -> dict:
    ngram_loction_count = {}  # {"ngram":[true_count1, theta_count2]} count1代表完全符合ngram-loction，count2代表在theta范围内符合的ngram-location+-theta
    # ngram_loction_count_of_every_packet = []  # 用来存每一个packet的ngram统计情况
    # ngram_loction_count_of_one_packet = {}  # 用来存储一个packet
    for one_packet_ngram_loc in all_ngram_loc:
        for ngram_loc in one_packet_ngram_loc:  # {(ngram,loc)}
            if ngram_loc not in ngram_loction_count:
                ngram_loction_count[ngram_loc] = [0, 0]
            ngram_loction_count[ngram_loc][0] += 1  # true_count
            if ngram_loc[1] - theta < 0:  # index越界
                left_index = 0
            else:
                left_index = ngram_loc[1] - theta
            if ngram_loc[1] + theta >= len(one_packet_ngram_loc):  # 即index越界
                right_index = len(one_packet_ngram_loc)
            else:
                right_index = ngram_loc[1] + theta + 1
            # print(left_index,right_index)
            for index in range(left_index, right_index, 1):
                if index != ngram_loc[1]:
                    if one_packet_ngram_loc[index][0] == ngram_loc[0]:  # 在theta范围内符合
                        ngram_loction_count[ngram_loc][1] += 1  # theta_count
    return ngram_loction_count


# def count_ngram_loction(packets_removed_other_information_bin: list, ngram_loction_set: set) -> dict:
#     ngram_loction_count = {}
#     ngram_loction_count_of_every_packet = []
#     for packet_removed_other_information_bin in packets_removed_other_information_bin:
#         ngram_loction_count_of_one_packet = {}
#         for ngram_loction in ngram_loction_set:
#             if ngram_loction not in ngram_loction_count:
#                 ngram_loction_count[ngram_loction] = 0
#             if
#             if judge_packet_hava_ngram_loction_theta(packet_removed_other_information_bin, ngram_loction):
#                 ngram_loction_count[ngram_loction] += 1
'''
根据支持度进行过滤
'''


def filter_by_support(ngram_loction_count: dict, support: int) -> dict:
    filter_ngram_loction_count = {}
    for value in ngram_loction_count.items():
        if value[1][0] >= support:
            filter_ngram_loction_count[value[0]] = value[1]
    return filter_ngram_loction_count


'''
获取边界候选集
'''


def get_bound_candidate(filter_ngram_loction_count: dict):
    bound_candidate = set()  # 所有候选边界混在一起
    ngram_loction_category_by_n = {}  # 按n分类的候选边界
    for value in filter_ngram_loction_count.items():
        bound_candidate.add((value[0][1], value[0][1] + len(value[0][0]) - 1))
        if len(value[0][0]) not in ngram_loction_category_by_n:
            ngram_loction_category_by_n[len(value[0][0])] = set()
        ngram_loction_category_by_n[len(value[0][0])].add((value[0][1], value[0][1] + len(value[0][0]) - 1))
    return (bound_candidate, ngram_loction_category_by_n)


'''
获取i位置左右长度为r的比特串
'''


def get_r_bits_between_i(packet: str, i: int, r: int):
    if i > len(packet):
        left_str = ""
        right_str = ""
    if i < r:  # 左边不够
        left_str = ""
        right_str = packet[i + 1: i + r + 1]
    if len(packet) - 1 - r < i <= len(packet):  # 右边不够
        right_str = ""

# # 分支度量
# def calculate_branch_metric(whr_whd: tuple, ):
#     branch_metric = {}  # {i: metric}
#     for i in range(self.min_packet_length):
#         self.branch_metric[i] = 1 / ((whr_whd[0] * ))