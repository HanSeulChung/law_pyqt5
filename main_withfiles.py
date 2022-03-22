# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import uic, QtCore
import functools
import json
import pypickle
from konlpy.tag import Okt
from sklearn.metrics.pairwise import linear_kernel
from sentence_transformers import SentenceTransformer, util
import numpy as np
import pandas as pd



form_main = uic.loadUiType("mainwindow.ui")[0]  # main창 불러오기
form_second = uic.loadUiType("secondwindow3.ui")[0]  # 두번째창 불러오기


def tokenizer(raw, pos = ['Noun', 'Verb', 'Adjective']):
    okt = Okt()
    # 길이가 1 이하인 토근은 제외, 위에서 지정한 (Okt 사전에 따른) 토큰들만 특징으로 삼기
    return [word for word, tag in okt.pos(raw) if len(word) > 1 and tag in pos]


tatal_laws_data = pd.read_csv('total.csv')
file_path = r'./data/clean_laws_jo_total.json'
with open(file_path, 'r', encoding="UTF-8") as jsonfile:
    json_data = json.load(jsonfile)
laws_data_list = json_data["laws"]

load_tfidf_fit = pypickle.load("tfidf_fit.pickle")
load_tfidf_vectors = pypickle.load("tfidf_vectors.pickle")
dic_data = {}

class MainWindow(QMainWindow, QWidget, form_main):

    def __init__(self):
        super().__init__()
        self.dic_data_1 = {}
        self.initUIMain()
        self.show()

    def initUIMain(self):
        self.setupUi(self)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "law similarity"))
        self.label.setText(_translate("MainWindow", " "))
        self.law1.setText(_translate("MainWindow", " "))
        self.law2.setText(_translate("MainWindow", " "))
        self.law3.setText(_translate("MainWindow", " "))
        self.law3_2.setText(_translate("MainWindow", " "))
        self.law3_3.setText(_translate("MainWindow", " "))
        self.setWindowIcon(QIcon('law.png'))

        self.law1.mousePressEvent = functools.partial(MainWindow.first_law, self.law1)
        self.law2.mousePressEvent = functools.partial(MainWindow.second_law, self.law2)
        self.law3.mousePressEvent = functools.partial(MainWindow.third_law, self.law3)
        self.law3_2.mousePressEvent = functools.partial(MainWindow.fourth_law, self.law3_2)
        self.law3_3.mousePressEvent = functools.partial(MainWindow.fifth_law, self.law3_3)

    def first_law(self, event):
        self.close()  # hide main window
        self.second = SecondWindow()
        self.second.exec()
        self.show()

    def second_law(self, event):
        self.close()  # hide main window
        self.second = SecondWindow2()
        self.second.exec()
        self.show()

    def third_law(self, event):
        self.close()  # hide main window
        self.second = SecondWindow3()
        self.second.exec()
        self.show()

    def fourth_law(self, event):
        self.close()  # hide main window
        self.second = SecondWindow4()
        self.second.exec()
        self.show()

    def fifth_law(self, event):
        self.close()  # hide main window
        self.second = SecondWindow5()
        self.second.exec()
        self.show()

    def input_text(self):
        global text_data
        text_data = self.search_law.text()
        return text_data

    def search_laws(self):
        global dic_data
        input_text_data = self.input_text()
        dic_data = algorithm(input_text_data)
        #self.lawname1 = list(dic_data.keys())[0]

        self.lawname1 = list(dic_data.keys())[0]
        self.lawname2 = list(dic_data.keys())[1]
        self.lawname3 = list(dic_data.keys())[2]
        self.lawname4 = list(dic_data.keys())[3]
        self.lawname5 = list(dic_data.keys())[4]

        self.law1.setText(self.lawname1)
        self.law2.setText(self.lawname2)
        self.law3.setText(self.lawname3)
        self.law3_2.setText(self.lawname4)
        self.law3_3.setText(self.lawname5)

#input_text_data =text_data
#input_text_data = """ 소방 """


def algorithm(input_text_data):
    srch_vector = load_tfidf_fit.transform([input_text_data])
    cosine_similar = linear_kernel(srch_vector, load_tfidf_vectors).flatten()
    sim_rank_idx = cosine_similar.argsort()[::-1]
    tf_idf_result_index = []  # 실 데이터 인덱스
    tf_idf_sentences = []  # 결과 조문
    for i in sim_rank_idx:
        if cosine_similar[i] > 0.13:
            tf_idf_result_index.append(i)
            tf_idf_sentences.append(laws_data_list[i])

    sbert_result_index = []

    embedder = SentenceTransformer("jhgan/ko-sroberta-multitask")

    # TF-IDF 결과 조문을 Corpus로
    corpus = tf_idf_sentences
    corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

    # Query sentences:
    q_list = []
    q_list.append(input_text_data)
    queries = q_list

    # Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
    top_k = 20
    for query in queries:
        query_embedding = embedder.encode(query, convert_to_tensor=True)
        cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
        cos_scores = cos_scores.cpu()

        # We use np.argpartition, to only partially sort the top_k results
        top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]

        for idx in top_results[0:top_k]:
            sbert_result_index.append(tf_idf_result_index[idx])

    result_law_dic = {}  # {"우체국보험특별회계법 시행규칙":[123513,12345,234,123]}
    for j in sbert_result_index:
        index_num = int(j)
        law_name = tatal_laws_data.iloc[index_num]["법령명"]
        if law_name in result_law_dic:
            value_list = result_law_dic[law_name]
            value_list.append(index_num)
            result_law_dic[law_name] = value_list

        else:
            result_law_dic[law_name] = [index_num]

    return result_law_dic





# law1 누르면 나오는 두번째 창
class SecondWindow(QDialog, QWidget, form_second):
    def __init__(self):
        super(SecondWindow, self).__init__()
        self.initUIsecond()
        self.show()  #두번째창 실행

    def initUIsecond(self):
        global dic_data
        self.setupUi(self)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "law similarity"))
        self.setWindowIcon(QIcon('law.png'))

        self.lawname_1 = list(dic_data.keys())[0]
        self.label.setText(self.lawname_1)

        jo_list = list(dic_data.values())[0]
        text = []
        number = len(jo_list)
        for i in range(number):
            texts = tatal_laws_data.iloc[jo_list[i]]["조문내용"].replace('\t',"")
            text.append(texts)
            self.show_laws.setText("")

        for j in range(number):
            self.show_laws.append(text[j])

        self.back_btn.clicked.connect(self.back_to_main)

    def back_to_main(self):
        self.close()


#law2 누르면 나오는 두번째 창
class SecondWindow2(QDialog, QWidget, form_second):
    def __init__(self):
        super(SecondWindow2, self).__init__()
        self.initUIsecond()
        self.show()  #두번째창 실행

    def initUIsecond(self):
        self.setupUi(self)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "law similarity"))
        self.setWindowIcon(QIcon('law.png'))
        self.lawname_2 = list(dic_data.keys())[1]
        self.label.setText(self.lawname_2)

        jo_list = list(dic_data.values())[1]
        text = []
        number = len(jo_list)
        for i in range(number):
            texts = tatal_laws_data.iloc[jo_list[i]]["조문내용"].replace('\t',"")
            text.append(texts)
            self.show_laws.setText("")

        for j in range(number):
            self.show_laws.append(text[j])

        self.back_btn.clicked.connect(self.back_to_main)

    def back_to_main(self):
        self.close()


#law3 누르면 나오는 두번째 창
class SecondWindow3(QDialog, QWidget, form_second):
    def __init__(self):
        super(SecondWindow3, self).__init__()
        self.initUIsecond()
        self.show()  #두번째창 실행

    def initUIsecond(self):
        self.setupUi(self)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "law similarity"))
        self.setWindowIcon(QIcon('law.png'))

        self.lawname_3 = list(dic_data.keys())[2]
        self.label.setText(self.lawname_3)

        jo_list = list(dic_data.values())[2]

        text = []
        number = len(jo_list)
        for i in range(number):
            texts = tatal_laws_data.iloc[jo_list[i]]["조문내용"].replace('\t',"")
            text.append(texts)
            self.show_laws.setText("")

        for j in range(number):
            self.show_laws.append(text[j])

        self.back_btn.clicked.connect(self.back_to_main)

    def back_to_main(self):
        self.close()


#law4 누르면 나오는 두번째 창
class SecondWindow4(QDialog, QWidget, form_second):
    def __init__(self):
        super(SecondWindow4, self).__init__()
        self.initUIsecond()
        self.show()  #두번째창 실행

    def initUIsecond(self):
        self.setupUi(self)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "law similarity"))
        self.setWindowIcon(QIcon('law.png'))

        self.lawname_4 = list(dic_data.keys())[3]
        self.label.setText(self.lawname_4)

        jo_list = list(dic_data.values())[3]
        text = []
        number = len(jo_list)
        for i in range(number):
            texts = tatal_laws_data.iloc[jo_list[i]]["조문내용"].replace('\t',"")
            text.append(texts)
            self.show_laws.setText("")

        for j in range(number):
            self.show_laws.append(text[j])

        self.back_btn.clicked.connect(self.back_to_main)

    def back_to_main(self):
        self.close()

#law5 누르면 나오는 두번째 창
class SecondWindow5(QDialog, QWidget, form_second):
    def __init__(self):
        super(SecondWindow5, self).__init__()
        self.initUIsecond()
        self.show()  #두번째창 실행

    def initUIsecond(self):
        self.setupUi(self)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "law similarity"))
        self.setWindowIcon(QIcon('law.png'))

        self.lawname_5 = list(dic_data.keys())[4]
        self.label.setText(self.lawname_5)

        jo_list = list(dic_data.values())[4]
        text = []
        number = len(jo_list)
        for i in range(number):
            texts = tatal_laws_data.iloc[jo_list[i]]["조문내용"].replace('\t', "")
            text.append(texts)
            self.show_laws.setText("")

        for j in range(number):
            self.show_laws.append(text[j])
        self.back_btn.clicked.connect(self.back_to_main)

    def back_to_main(self):
        self.close()


if __name__ == "__main__":
    def tokenizer(raw, pos=['Noun', 'Verb', 'Adjective']):
        okt = Okt()
        # 길이가 1 이하인 토근은 제외, 위에서 지정한 (Okt 사전에 따른) 토큰들만 특징으로 삼기
        return [word for word, tag in okt.pos(raw) if len(word) > 1 and tag in pos]

    app = QApplication(sys.argv)
    ex = MainWindow()

    ex.show()
    sys.exit(app.exec_())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
