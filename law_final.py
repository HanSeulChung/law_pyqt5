import sys
import webbrowser
# from form1 import Ui_MainWindow
from newform import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl

import json

file_path = r'./data/clean_laws_jo_total.json'
with open(file_path, 'r', encoding="UTF-8") as jsonfile:
    json_data = json.load(jsonfile)

laws_data_list = json_data["laws"]



class HyperlinkLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__()
        self.setOpenExternalLinks(True)
        assert isinstance(parent, object)
        self.setParent(parent)

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

    def link(self, linkStr):
        QDesktopServices.openUrl(QUrl(linkStr))

    # btn이 눌리면 작동할 함수
    def search_laws(self):
        # query1 = law1
        # query2 = law2
        # query3 = law3
        # query4 = law4
        # query5 = law5


        # linkTemplate ='<a href={0}>{1}</a>'

        # query1 = HyperlinkLabel(self)
        self.law1.setOpenExternalLinks(True)
        self.law1.linkActivated.connect(self.link)
        self.law1.setText('<a href = \"https://www.law.go.kr/DRF/lawService.do?OC=w0w1278&target=law&MST=210636&type=HTML\"> 해당법 </a>')
        #self.law1.setText(linkTemplate.format("https://www.naver.com",query1))
        # self.law1.append("hi")
        #self.law1.setTextInteractionFlags(TextSelectableByMouse)

        # self.law2.setText(str(query2))
        # self.law3.setText(str(query3))
        # self.law4.setText(str(query4))
        # self.law5.setText(str(query5))

    def Urls(self):
        pass

        #법령명
        #법령MST
        #url_form=https://www.law.go.kr/DRF/lawService.do?OC=w0w1278&target=law&MST={} 서식문제화
app = QApplication(sys.argv)
ex = Main()
ex.show()
sys.exit(app.exec_())
