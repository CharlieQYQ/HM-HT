"""
创建日期：2022.3.27
作者：乔毅
文件名：Word2Vec.py
功能：利用词向量计算余弦相似度
备注：代码中被注释掉的print()为 测试时调用，控制台输出没有实际意义
"""

# 导入库
import jieba
import numpy as np
from scipy.linalg import norm
from Funcs.Func_tools import gen_stop_words

"""
2022.4.21 为鸿蒙开发后端做调整。在已有功能的基础上做调整。
"""


# 向量相似度，model为加载的预训练模型
def vector_similarity(s1: str, s2: str, model):
    # 生成停用词
    stop_words = gen_stop_words()

    # 定义词向量
    def sentence_vector(s):
        # 分词
        words = jieba.lcut(s)
        v = np.zeros(64)
        for word in words:
            # 过滤停用词和空格，并检查预训练模型中是否有这个词的Key
            if word not in stop_words and not word.isspace() and model.has_index_for(word):
                v += model[word]
        v /= len(words)
        return v

    # 处理输入语句
    v1, v2 = sentence_vector(s1), sentence_vector(s2)

    # 返回向量值
    return np.dot(v1, v2) / (norm(v1) * norm(v2))
