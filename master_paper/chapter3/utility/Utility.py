# 将报文中的data按字节转化为向量，eg: 0102afd4->[01,02,af,d4]
def data2vector(data: bytes) -> list:
    data_vector = []
    for B in data:
        data_vector.append(B)
    return data_vector


# 将所有消息的data转化为向量，返回向量列表
def data_list2vector(data_list: list) -> list:
    data_vector_list = []
    for data in data_list:
        data_vector = data2vector(data)
        data_vector_list.append(data_vector)
    return data_vector_list


# 将向量按指定长度对齐，即将长的截尾，短的就添0,返回对齐后的vector（新的）
def align_vector(length: int, data_vector_list: list) -> list:
    data_vector_aligned_list = []
    for data_vector in data_vector_list:
        cur_len = len(data_vector)
        gap = length - cur_len
        if gap > 0:
            temp = data_vector
            temp.extend(0 for _ in range(gap))
            data_vector_aligned_list.append(temp)
        elif gap < 0:
            data_vector_aligned_list.append(data_vector[: length])
        else:
            data_vector_aligned_list.append(data_vector)
    return data_vector_aligned_list


def divide_flow_by_ip():
    pass


'''
用来读取txt文件，主要用来读取NEMESYS的结果文件.txt
'''


class DecodeTxt2List:
    # def __init__(self, txt_file: str):
    #     self.txt_file = txt_file
    @staticmethod
    def decode_txt2list(txt_file: str):
        result = []
        with open(txt_file, 'r') as f:
            for line in f:
                result.append(list(line.replace(' ', '').strip('\n').strip('[').strip(']').split(',')))
        return result

    @staticmethod
    def translate2boundary(result: list):
        '''
        将原数据重新解释
        这边返回的边界不是01向量，而是[1,2,4,7,10]这种
        '''
        boundarys = []
        for one_message_seg in result:
            boundary = []
            start_index = 0
            for field in one_message_seg:
                boundary.append(start_index + int(field) - 1)
                start_index += int(field)
            boundarys.append(boundary)
        return boundarys

    @staticmethod
    def decode_txt2boundary(txt_file: str) -> list:
        res = DecodeTxt2List.decode_txt2list(txt_file)
        return DecodeTxt2List.translate2boundary(res)
