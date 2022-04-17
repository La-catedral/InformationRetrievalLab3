from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5 import QtCore
import sys
from ir_login import Ui_MainWindow
from docx_ui import Docx_Ui_Form
from web_ui import Web_Ui_Form
from biuld_index import *
from docx import Document


# 主窗口
class MainWindow(QMainWindow, Ui_MainWindow):
    switch_window1 = QtCore.pyqtSignal()  # 跳转信号
    switch_window2 = QtCore.pyqtSignal()  # 跳转信号

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.web_button.clicked.connect(self.go_web)
        self.docx_button.clicked.connect(self.go_docx)

    def go_web(self):
        self.switch_window1.emit()

    def go_docx(self):
        self.switch_window2.emit()


# 网页内容检索窗口
class WebWindow(QWidget, Web_Ui_Form):
    def __init__(self,ir_system):
        super(WebWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.web_search_handle)
        self.listWidget.itemClicked.connect(self.item_click)
        self.result = []
        self.ir_system = ir_system


    def web_search_handle(self):
        question = self.quesiton.text()
        level =self.level.currentText()
        real_level = 3
        if level == '董事长':
            real_level = 0
        elif level == '总经理':
            real_level = 1
        elif level == '部门经理':
            real_level = 2
        # print(real_level)

        self.result = self.ir_system.web_search(real_level,question)
        res_num = len(self.result)
        list_count = self.listWidget.count()
        for idx in range(list_count):
            if idx >= res_num:
                break
            self.listWidget.item(idx).setText(''.join(self.result[idx]['title']))

    def item_click(self):
        idx = self.listWidget.selectedIndexes()[0].row()
        self.textBrowser.setText(' '.join(self.result[idx]['paragraphs']))


# 文档内容检索窗口
class DocxWindow(QWidget, Docx_Ui_Form):
    def __init__(self,ir_system):
        super(DocxWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.docx_search_handle)
        self.listWidget.itemClicked.connect(self.item_click)
        self.result = []
        self.ir_system = ir_system

    def docx_search_handle(self):
        question = self.quesiton.text()
        level =self.level.currentText()
        real_level = 3
        if level == '董事长':
            real_level = 0
        elif level == '总经理':
            real_level = 1
        elif level == '部门经理':
            real_level = 2
        # print(level)
        # self.listWidget.clear()  # todo 清理上次查询
        self.result = self.ir_system.file_search(real_level,question)
        # print(self.result)
        res_num = len(self.result)
        list_count = self.listWidget.count()
        # print(list_count)
        for idx in range(list_count):
            if idx >= res_num:
                break
            self.listWidget.item(idx).setText(''.join(self.result[idx]))  # 显示文件名

    def item_click(self):
        idx = self.listWidget.selectedIndexes()[0].row()
        file_name = self.result[idx]
        paragraphs = ''
        docx = Document('files/' +file_name)
        for paragraph in docx.paragraphs:
            text = paragraph.text
            paragraphs = paragraphs + text
        self.textBrowser.setText(paragraphs)



class Controller:
    def __init__(self,ir_system):
        self.hello = MainWindow()
        self.web_win = WebWindow(ir_system)
        self.doc_win = DocxWindow(ir_system)

    # 跳转到 hello 窗口
    def show_hello(self):
        self.hello.switch_window1.connect(self.show_web)
        self.hello.switch_window2.connect(self.show_docx)
        self.hello.show()

    def show_web(self):
        self.hello.close()
        self.web_win.show()

    def show_docx(self):
        self.hello.close()
        self.doc_win.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ir_system = RetriSystem()
    control = Controller(ir_system)
    control.show_hello()
    sys.exit(app.exec_())
