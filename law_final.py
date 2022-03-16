import sys
from newform import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QMainWindow


# import json
#
# file_path = r'./data/clean_laws_jo_total.json'
# with open(file_path, 'r', encoding="UTF-8") as jsonfile:
#     json_data = json.load(jsonfile)
#
# laws_data_list = json_data["laws"]




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

app = QApplication(sys.argv)
ex = Main()
ex.show()
sys.exit(app.exec_())
