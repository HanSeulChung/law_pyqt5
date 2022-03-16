import sys
from newform import Ui_Form
from PyQt5.QtWidgets import QApplication, QMainWindow


class Main(QMainWindow,Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.set_ui()
        self.set_slot()

    def set_ui(self):
        pass

    def set_slot(self):
        self.search_btn.clicked.connect(self.search_laws)
        self.search_law.textChanged.connect(self.input_text)

    def input_text(self):
        self.input_text_data = self.search_law.text()
        pass


    # btn이 눌리면 작동할 함수
    def search_laws(self):
        # linkTemplate ='<a href={0}>{1}</a>'
        linkTemplate = '<a href=\"https://www.law.go.kr/DRF/lawService.do?OC=w0w1278&target=law&MST={0}&type=HTML\">{1}</a>'

        p = self.input_text_data
        s = "query2"
        d = "query3"
        f = "query4"
        c = "query5"

        number1 = str(3)

        # tatal_laws_data.iloc[i]["법령명"])
        # tatal_laws_data.iloc[i]["법령MST"])
        # numbertatal_laws_data.iloc[i]["조문번호"]

        #query1 = list(result_law_dic.keys())[0] key값 가져오기


        # self.law1.setOpenExternalLinks(True)
        # self.law1.linkActivated.connect(self.link)
        self.law1.setText(linkTemplate.format("210636",p) + "\t "+ number1 +"조")
        #self.law1.setTextInteractionFlags(TextSelectableByMouse)
        self.law2.setText(linkTemplate.format("240223",s ))

        self.law3.setText(linkTemplate.format("224453",d ))

        self.law4.setText(linkTemplate.format("224453",f ))

        self.law5.setText(linkTemplate.format("224453",c ))

    def Urls(self):
        pass

        #법령명
        #법령MST
        #url_form=https://www.law.go.kr/DRF/lawService.do?OC=w0w1278&target=law&MST={} 서식문제 화


import pandas as pd
import json
import re
import numpy as np
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import linear_kernel
import pypickle
from konlpy.tag import Okt
okt=Okt() #형태소 분해 객체 생성

#json file 불러오기
file_path = r'./data/clean_laws_jo_total.json'
with open(file_path, 'r', encoding="UTF-8") as jsonfile:
    json_data = json.load(jsonfile)

laws_data_list = json_data["laws"]

# TF-IDF 불러오기
with open("tfidf_fit.pickle", 'rb') as f:
    load_tfidf_fit = pypickle.load(f)

# TF-IDF transform 불러오기
with open("tfidf_vectors.pickle", 'rb') as f:
    load_tfidf_vectors = pypickle.load(f)

a = Main()
srch_vector = load_tfidf_fit.transform([a])
cosine_similar =  linear_kernel(srch_vector, load_tfidf_vectors).flatten()
sim_rank_idx = cosine_similar.argsort()[::-1]


#tfidf result
tf_idf_result_index = [] #실 데이터 인덱스
tf_idf_sentences = []# 결과 조문
for i in sim_rank_idx:
    if cosine_similar[i] > 0.13:
        # print('{} /score : {}'.format(laws_data_list[i],cosine_similar[i]))
        tf_idf_result_index.append(i)
        tf_idf_sentences.append(laws_data_list[i])


sbert_result_index = []

# 'sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens'
# "jhgan/ko-sroberta-multitask"
embedder = SentenceTransformer("jhgan/ko-sroberta-multitask")

# TF-IDF 결과 조문을 Corpus로
corpus = tf_idf_sentences
corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

# Query sentences:
q_list = []
a = Main()
q_list.append(a)
queries = q_list

# Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
top_k = 20
for query in queries:
    query_embedding = embedder.encode(query, convert_to_tensor=True)
    cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
    cos_scores = cos_scores.cpu()

     #We use np.argpartition, to only partially sort the top_k results
    top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]

    for idx in top_results[0:top_k]:
        sbert_result_index.append(tf_idf_result_index[idx])



tatal_laws_data = pd.read_csv('total.csv')

result_law_dic = {}  # {"우체국보험특별회계법 시행규칙":[123513,12345,234,123]}
for i in sbert_result_index:
    index_num = int(i)
    # print(laws_data_list_cut[index_num])
    data_detail = tatal_laws_data.iloc[[index_num], :]
    # print(tatal_laws_data.iloc[index_num]["법령명"])

    law_name = tatal_laws_data.iloc[index_num]["법령명"]
    # print('법령명 : ', tatal_laws_data.iloc[index_num]["법령명"])
    if law_name in result_law_dic:
        value_list = result_law_dic[law_name]
        value_list.append(index_num)

    else:
        result_law_dic[law_name] = [index_num]

# tatal_laws_data.iloc[i]["법령명"])
# tatal_laws_data.iloc[i]["법령MST"])
# numbertatal_laws_data.iloc[i]["조문번호"]

#query1 = list(result_law_dic.keys())[0] key값 가져오기



app = QApplication(sys.argv)
ex = Main()
ex.show()
sys.exit(app.exec_())
