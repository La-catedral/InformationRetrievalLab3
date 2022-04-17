# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ir_login.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(461, 298)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(160, 10, 171, 61))
        self.label.setObjectName("label")
        self.web_button = QtWidgets.QPushButton(self.centralwidget)
        self.web_button.setGeometry(QtCore.QRect(90, 120, 113, 32))
        self.web_button.setObjectName("web_button")
        self.docx_button = QtWidgets.QPushButton(self.centralwidget)
        self.docx_button.setGeometry(QtCore.QRect(260, 120, 113, 32))
        self.docx_button.setObjectName("docx_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 461, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "欢迎进入企业搜索系统"))
        self.web_button.setText(_translate("MainWindow", "网页内容检索"))
        self.docx_button.setText(_translate("MainWindow", "文档内容检索"))

