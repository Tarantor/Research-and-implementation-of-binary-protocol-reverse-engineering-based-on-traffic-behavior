import csv
'''
这个文件用来处理csv文件得到聚类的大实验数据集
pure_data中的数据就是data文件夹用下面两个函数提取的
'''

protocal_list_branch_1= ["S7COMM","S7COMM-PLUS","modbus_H","EGD","OMRON","DNP",]
protocal_list_branch_2= ["S7COMM","OMRON","EGD","DNP","modbus_H","S7COMM-PLUS",]

#提纯单种协议的报文
def csv2pure(protocal):
        with open("../../data/csv_data/{}.csv".format(protocal)) as csvfile:
            csvreader = csv.reader(csvfile)
            listreport = list(csvreader)

        with open("./{}.csv".format(protocal), 'w', newline='') as csvwrite:
            csvwriter = csv.writer(csvwrite)
            for row in listreport:
                cleaned_row = [cell.strip() for cell in row]  # 去除每个字段的前后空白字符
                csvwriter.writerow([cleaned_row[3]])

#提取大的数据集
def pure_data(protocal_list_branch:list):
    for j in range (1,7):
        with open("./pure_data/c_database_{}.csv".format(j), 'w', newline='') as csvwrite:
            csvwriter = csv.writer(csvwrite)
            for k in range(0,j):
                option = protocal_list_branch[k]
                with open("./data_extract_300/{}_pure.csv".format(option), 'r') as csvfile:
                    csvreader = csv.reader(csvfile)
                    listreport = list(csvreader)
                    del listreport[0]
                for row in listreport:
                    cleaned_row = [cell.strip() for cell in row]
                    # print(cleaned_row[1])# 去除每个字段的前后空白字符
                    csvwriter.writerow([cleaned_row[0]])

c_database = ["c_database_1","c_database_2","c_database_3","c_database_4","c_database_5","c_database_6"]
#对数据集进行切片
def database_filter():
    for j in range(1, 7):
        with open("pure_data_gram_300/filter_database{}.csv".format(j), 'w', newline='') as csvwrite:
            csvwriter = csv.writer(csvwrite)
            min_length = float('inf')  # 初始化为正无穷大
            with open("pure_data/c_database_{}.csv".format(j), 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                listreport = list(csvreader)
            for message in listreport:
                min_length = min(min_length, len(message[0]))  # 更新最小长度
            for row in listreport:
                trimmed_row = row[0][:min_length]  # 修剪为最小长度
                 # 打印修剪前后的长度
                csvwriter.writerow([trimmed_row])

# csv2pure("BACnet_pure")
pure_data(protocal_list_branch_1)
database_filter()
