#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/6/20 下午7:37
# @Author  : Jingshuo Liu
# @File    : biuld_index

import os
import json
from docx import Document
import jieba
import gensim.summarization.bm25 as obm
import numpy as np


# 构建倒排索引
def preprocess_web(file_path='preprocessed.json'):
    """
    为web内容构建倒排索引
    :param obm_model:
    :param file_path: 存储web内容的json文件路径
    :return:
    """

    web_list = []  # list that save the json format webpages
    web_inv_index = {}  # inverted index for web pages
    corpus = []
    with open(file_path,'r') as web_f:
        for idx,line in enumerate(web_f):
            this_line = json.loads(line)
            web_list.append(this_line)
            seg_doc = []
            for sentence in this_line['paragraphs']:
                seg_sen = ' '.join(jieba.cut(sentence)).split(' ')
                seg_doc.append(' '.join(seg_sen))
                for word in seg_sen:
                    if word not in web_inv_index:
                        web_inv_index[word] = set()
                    web_inv_index[word].add(idx)
            corpus.append(' '.join(seg_doc).split(' '))
    web_obm = obm.BM25(corpus)
    # 输出到倒排索引文件
    with open('web_inverted_index.txt', 'w') as index_f:
        buf = ''
        for word in web_inv_index:
            strin = word
            for pid in web_inv_index[word]:
                strin += ' ' + str(pid)
            buf += strin + '\n'
        index_f.write(buf[:-1])
    return web_list,web_inv_index, web_obm


def preprocess_docx(from_dir='files'):
    """
    为下载的文档内容构建倒排索引
    :param omb_model:
    :param from_dir: 文档目录路径
    :return:
    """
    pid2filename = {}  # 从pid到docx文档的映射
    file_inv_index ={}  # 为docx建立的倒排索引
    corpus = []
    files = os.listdir(from_dir)
    cnt = 0
    for file in files:
        if file.endswith('.docx'):
            pid2filename[cnt] = file  # 构建pid到文档名字的映射
            cnt += 1
            doc = Document(from_dir + '/' + file)
            paras = []
            for paragraph in doc.paragraphs:
                text = paragraph.text
                if text.strip():
                    txt_list = ' '.join(jieba.cut(text.strip())).split(' ')
                paras = paras + txt_list
                for word in txt_list:
                    if word not in file_inv_index:
                        file_inv_index[word] = set()
                    file_inv_index[word].add(cnt)  # 为倒排索引添加文档序号
            corpus.append(paras)
    doc_obm = obm.BM25(corpus)
    # 输出到倒排索引文件
    with open('docx_inverted_index.txt', 'w') as index_f:
        buf = ''
        for word in file_inv_index:
            strin = word
            for pid in file_inv_index[word]:
                strin += ' ' + str(pid)
            buf += strin + '\n'
        index_f.write(buf[:-1])
    return pid2filename, file_inv_index, doc_obm


def index_search(inv_index,question):
    """
    使用倒排索引进行检索
    :param question: 问句字符串
    :return:the pid set
    """
    result = set()
    question = ' '.join(jieba.cut(question)).split(' ')  # 分词成词串到倒排索引中进行检索
    for word in question:
        if word in inv_index:
            result = result | inv_index[word]
    return result


class RetriSystem:  # 检索系统类
    def __init__(self):
        self.pid2filename, self.file_inv_index, self.doc_obm = preprocess_docx()
        self.web_list, self.web_inv_index, self.web_obm = preprocess_web()

    def web_search(self,level,question):  # level  0 1 2 3 权限逐渐减小
        """
        从网页文本内容中进行检索
        :param level:
        :param question:
        :return:
        """
        def satisfy_level(pid,level):
            if level == 0:
                return True
            elif level == 1 and pid < 750:
                return True
            elif level == 2 and pid < 500:
                return True
            elif level == 3 and pid < 250:
                return True
            return False
        res_set = index_search(self.web_inv_index,question)  # 从倒排索引中搜到的pid集合
        scores = self.web_obm.get_scores(question)
        sorted_scores = np.argsort(-np.array(scores))
        match_num = sum(np.array(scores) != 0)  # 记录当前question在语料库的命中数
        res_pids = []
        if match_num > 0:
            for i in range(match_num):
                pid = sorted_scores[i]
                if pid in res_set and satisfy_level(int(pid),level):  # 添加满足条件的pid
                    res_pids.append(sorted_scores[i])
        result_web = []
        for pid in res_pids:
            result_web.append(self.web_list[pid])
        # todo 客户端需求 返回对应网页条目内容
        return result_web

    def file_search(self,level,question):
        """
        从文档内容中进行检索
        :param level: 权限等级，0级最高
        :param question: 问句
        :return:
        """

        def satisfy_level(pid,level):
            total_num = len(self.pid2filename)
            print(self.pid2filename)
            print(pid)
            if level == 0:
                return True
            elif level == 1 and pid < 3 * (total_num / 4):
                return True
            elif level == 2 and pid <= total_num / 2:
                return True
            elif level == 3 and pid <= total_num / 4:
                return True
            return False

        res_set = index_search(self.file_inv_index, question)  # 从倒排索引中搜到的pid集合
        # scores = self.doc_obm.get_scores(question)
        # sorted_scores = np.argsort(-np.array(scores))
        # match_num = sum(np.array(scores) != 0)  # 记录当前question在语料库的命中数
        # print(match_num)
        # print(res_set)
        # res_pids = []
        # if match_num > 0:
        #     for i in range(match_num):
        #         pid = sorted_scores[i]
        #         print(pid)
        #         if pid in res_set and satisfy_level(int(pid), level):  # 添加满足条件的pid
        #             res_pids.append(sorted_scores[i])
        result_files = []
        # for pid in res_pids:
        #     result_files.append(self.pid2filename[pid])
        for pid in res_set:
            if satisfy_level(int(pid),level):
                result_files.append(self.pid2filename[pid])
        return result_files  # 返回文件名列表


