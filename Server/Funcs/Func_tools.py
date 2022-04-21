"""
创建日期：2021.9.2
作者：乔毅
文件名：Func_tools.py
功能：实现功能需要的基本函数
"""

# 导入库
import os
import jieba
import numpy as np
from functools import reduce
from math import sqrt

"""
2022.4.21 为鸿蒙开发后端做调整。在已有功能的基础上做调整。
"""


# 生成停用词
def gen_stop_words() -> list:
    """
    函数名：gen_stop_words
    作用：生成停用词列表
    :return:停用词列表
    """
    with open(os.path.join("Funcs/stop_words.txt"), "r", encoding='UTF-8') as fp:
        # with open("/root/HM-HT/Server/Funcs/stop_words.txt", "r", encoding='UTF-8') as fp:
        stop_words = [_.strip() for _ in fp.readlines()]
    # 返回停用词列表
    return stop_words


# 分词函数
def text_seg(text: str, stop_words: list = None) -> list:
    """
    函数名：text_seg
    作用：对输入的字符串进行分词处理
    :param text: 带分词字符串
    :param stop_words: 停用词列表
    :return: 分词结果列表
    """
    # 分词结果
    seg_list = []
    if not stop_words:
        stop_words = gen_stop_words()
    # 分词处理
    for each in jieba.cut(text):
        if each not in stop_words and not each.isspace():
            seg_list.append(each.lower())
    # 返回分词结果列表
    return seg_list


# 余弦相似度计算
class CosineSimilarity(object):
    """
    余弦相似性计算相似度
    """

    # 初始化函数
    def __init__(self, init_query, target_data):
        """
        函数名：__init__
        作用：初始化余弦相似度计算类
        :param init_query: 输入文本分词后向量，为输入查询文本
        :param target_data: 对比文本以及文本向量构成的字典 Key分别为index和value，为待对比文本库
        """
        self.init_query = init_query
        self.target_data = target_data

    # 创建兴趣向量
    def create_vector(self):
        """
        函数名：create_vector
        作用：创建文本库的兴趣向量
        文本及文本向量 index: value
        index：标题
        value：标题的分词结果
        :return:兴趣向量 word_vector
        """

        # index：标题
        # value：标题的分词结果
        index, values = self.target_data['index'], self.target_data['value']
        # 文本向量结果
        word_vector = {
            # index：标题
            'index': index,
            # value：标题的兴趣向量
            'value': []
        }
        # title_vector：查询标题的词频向量列表
        # value_vector：文本库的词频向量列表
        title_vector, value_vector = [], []
        # 求所有单词集合
        all_word = set(self.init_query + values)
        # 计算含有单词数（词频向量）
        for each_word in all_word:
            # 统计查询标题的词频
            title_num = self.init_query.count(each_word)
            # 统计文本库的词频
            value_num = values.count(each_word)
            # 加入各自列表
            title_vector.append(title_num)
            value_vector.append(value_num)
        # word_vector['value'][0] 为查询标题的词频向量
        word_vector['value'].append(title_vector)
        # word_vector['value'][1] 为文本库的词频向量
        word_vector['value'].append(value_vector)

        # 返回兴趣向量
        return word_vector

    # 计算余弦相似度
    def calculate_cos(self, word_vector) -> dict:
        """
        函数名：calculate_cos
        作用：计算余弦相似度
        :param word_vector: 文本及文本向量，Key分别为index以及value
        :return: result_dic 各个用户相似度值
        """
        # 结果字典
        result_dic = {}
        # 提取词频向量
        values = word_vector['value']
        value_arr = np.array(values)

        # 余弦相似性
        # squares：存储所有的向量平方
        squares = []
        # numerator: A·B（A点乘B），计算分量乘积和
        # value_arr[0]和value_arr[1]对应查询标题词频向量和文本库词频向量
        numerator = reduce(lambda x, y: x + y, value_arr[0] * value_arr[1])

        # square_title：查询标题词频向量分量的平方和
        # square_data：文本库词频向量分量的平方和
        square_title, square_data = 0.0, 0.0
        # 计算各自词频向量的模||A||和||B||
        for num in range(len(value_arr[0])):
            square_title += pow(value_arr[0][num], 2)
            square_data += pow(value_arr[1][num], 2)
        # 加入向量平方列表，这一步进行了开方运算
        squares.append(sqrt(square_title))
        squares.append(sqrt(square_data))
        # 计算所有分量的模之积
        mul_of_squares = reduce(lambda x, y: x * y, squares)
        # 计算余弦相似度
        cos_simi = float(('%.5f' % (numerator / mul_of_squares)))
        # 加入结果字典
        result_dic['index'] = word_vector['index']
        result_dic['value'] = cos_simi

        # 返回结果字典
        return result_dic
