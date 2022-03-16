import sys
from newform import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl

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

    # def link(self, linkStr):
    #     QDesktopServices.openUrl(QUrl(linkStr))

    # btn이 눌리면 작동할 함수
    def search_laws(self):
        # linkTemplate ='<a href={0}>{1}</a>'
        linkTemplate = '<a href=\"https://www.law.go.kr/DRF/lawService.do?OC=w0w1278&target=law&MST={0}&type=HTML\">{1}</a>'

        # self.law1.setOpenExternalLinks(True)
        # self.law1.linkActivated.connect(self.link)
        self.law1.setText(linkTemplate.format("210636","query1"))
        #self.law1.setTextInteractionFlags(TextSelectableByMouse)
        self.law2.setText(linkTemplate.format("240223","query2"))
        self.law3.setText(linkTemplate.format("224453","query3"))
        self.law4.setText(linkTemplate.format("224453","query4"))
        self.law5.setText(linkTemplate.format("224453","query5"))

    def Urls(self):
        pass

        #법령명
        #법령MST
        #url_form=https://www.law.go.kr/DRF/lawService.do?OC=w0w1278&target=law&MST={} 서식문제 화

app = QApplication(sys.argv)
ex = Main()
ex.show()
sys.exit(app.exec_())
