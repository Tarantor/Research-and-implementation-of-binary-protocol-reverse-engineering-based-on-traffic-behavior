
from processing import Processing
import csv


class Ngram:
    '''
    传message初始化
    '''
    def __init__(self):
        self.loc_ngrams = {}  # 每个location对应的n-gram
        self.loc_field_messageid = {}  # {location:{field:[messageid]}}
        self.loc_ngram_kinds = {}  # 存放每个位置的种类数以及有这个字段的总的message数，{loc:(kindsNums, totalMessageNum)}
        self.loc_ngram_rate = {} #{loc:{ngram:rate}}
        self.packets_removed_other_information = []
        self.length_dict = {}
    '''
    直接传Slice来进行初始化
    '''
    # @classmethod
    # def messageSlice_init(cls, messagesSlices):
    #     cls.__init__(messages=None, messagesSlices=messagesSlices)
    #
    #
    def read_csv_data_to_list(self, file_path: str) -> object:
        with open(file_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            listreport = [row[0] for row in csvreader]
            del listreport[0]
        for row in listreport:
            self.packets_removed_other_information.append(row)

    def classify_by_length(self):
        # 遍历输入列表中的每个字符串
        for item in self.packets_removed_other_information:
            # 获取字符串长度
            length = len(item)

            # 如果该长度已存在于字典中，则添加字符串到相应的列表
            if length in self.length_dict:
                self.length_dict[length].append(item)
            else:
                # 如果该长度不在字典中，创建一个新的列表
                self.length_dict[length] = [item]
        return self.length_dict
    '''
    对每条报文进行n-gram切片
    '''
    # def ngram(self, n: int):
    #     self.messagesSlices.clear()
    #     for message in self.messages:
    #         data = message.data  # bytes
    #         messageSlice = MessageSlice(message, n, {})
    #         for loc in range(0, len(data)-n+1):
    #             ngram_name = data[loc: loc + n].hex()  # 转化为字符串，以便于区分，bytes会有点问题
    #             messageSlice.fields[loc] = ngram_name # {loc:ngram}
    #         self.messagesSlices.append(messageSlice)
    # '''
    # 统计每个位置上的ngram
    # '''
    # def statistic_loc_ngram(self):
    #     for message_id, messagesSlice in enumerate(self.messagesSlices):  # messageSlice一条消息的切片
    #         for index, field in messagesSlice.fields.items():
    #             if index not in self.loc_ngrams:  #{loc:[32,00]}
    #                 self.loc_ngrams[index] = []
    #             a = (messagesSlice.message.message_id, field)
    #             self.loc_ngrams[index].append(a) #位置:[(第几条报文，取什么值)]
    # '''
    # 统计每个位置ngram的种类
    # '''
    # def loc_ngram_kind(self) -> dict:
    #     for location, message_id_and_fields in self.loc_ngrams.items():
    #         self.loc_field_messageid[location] = {}
    #         for message_id_and_field in message_id_and_fields:
    #             if message_id_and_field[1] not in self.loc_field_messageid[location]:
    #                 self.loc_field_messageid[location][message_id_and_field[1]] = []
    #             self.loc_field_messageid[location][message_id_and_field[1]].append(message_id_and_field[0])
    # '''
    # 统计每个位置的gram的种类数
    # '''
    # def statistic_loc_ngram_kinds(self):
    #     for loc, field_messageid in self.loc_field_messageid.items(): #{location:{field:[messageid]}}
    #         messageNum = 0
    #         for field, messageids in field_messageid.items():
    #             messageNum += len(messageids)
    #         self.loc_ngram_kinds[loc] = (len(field_messageid), messageNum)
    # '''
    # 统计每个位置每种ngram的频率
    # self.loc_ngram_rate = {} #{loc:{ngram:rate}}
    # '''
    # def statistic_loc_ngram_rate(self):
    #     for loc, field_messageid in self.loc_field_messageid.items():#{location:{field:[messageid]}}
    #         for field, messageids in field_messageid.items():
    #             self.loc_ngram_rate[loc][field] = len(messageids)

'''
p = Processing(pcap_file_path='../data/pcap_data/modbus_S_newest.pcap', csv_file_path="../data/csv_data/modbus_S_newest.csv")
#p.read_messages_from_pcap_and_transform_to_csv()
p.import_messages_from_csv()
#print(p.messages)
ngram = Ngram(messages=p.messages)
ngram.ngram(n=1)
ngram.statistic_loc_ngram()
ngram.loc_ngram_kind()
ngram.statistic_loc_ngram_kinds()
# for index, num in kinds.items():
#     print(index, num[1])
#print(kinds)
# print(len(ngram.loc_field_messageid[17]))
# print(ngram.loc_field_messageid[17])
print(ngram.loc_field_messageid[2])
for loc, ngram_kinds in ngram.loc_field_messageid.items():
    print("loc:{loc},kinds:{kinds}:".format(loc=loc, kinds=len(ngram_kinds)))
    print(ngram.loc_ngram_kinds)
'''