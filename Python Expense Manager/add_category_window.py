from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *


class CategoryWindow(QtWidgets.QDialog):
    def __init__(self):
        super(CategoryWindow, self).__init__()
        self.setupUi(self)

    def setupUi(self, Add_Category):
        Add_Category.setObjectName("Add_Category")
        Add_Category.resize(442, 192)
        self.gridLayoutWidget = QtWidgets.QWidget(Add_Category)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 421, 171))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.popup_main_window = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.popup_main_window.setContentsMargins(0, 0, 0, 0)
        self.popup_main_window.setObjectName("popup_main_window")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.gridLayoutWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 415, 165))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.window_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.window_label.setGeometry(QtCore.QRect(10, 10, 111, 41))
        self.window_label.setObjectName("window_label")
        self.line_1 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line_1.setGeometry(QtCore.QRect(10, 40, 391, 20))
        self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_1.setObjectName("line_1")
        self.enter_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.enter_label.setGeometry(QtCore.QRect(10, 60, 161, 21))
        self.enter_label.setObjectName("enter_label")
        self.line_2 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line_2.setGeometry(QtCore.QRect(10, 110, 391, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.submit_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.submit_button.setGeometry(QtCore.QRect(240, 130, 75, 23))
        self.submit_button.setObjectName("submit_button")
        self.cancel_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.cancel_button.setGeometry(QtCore.QRect(330, 130, 75, 23))
        self.cancel_button.setObjectName("cancel_button")
        self.category_input_box = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.category_input_box.setGeometry(QtCore.QRect(10, 80, 221, 20))
        self.category_input_box.setObjectName("category_input_box")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.popup_main_window.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.submit_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.retranslateUi(Add_Category)
        QtCore.QMetaObject.connectSlotsByName(Add_Category)

    def retranslateUi(self, Add_Category):
        _translate = QtCore.QCoreApplication.translate
        Add_Category.setWindowTitle(_translate("Add_Category", "Add_Category"))
        self.window_label.setText(_translate("Add_Category", "Add Category"))
        self.enter_label.setText(_translate("Add_Category", "Enter The name of the Category"))
        self.submit_button.setText(_translate("Add_Category", "Submit"))
        self.cancel_button.setText(_translate("Add_Category", "Cancel"))

    def get_category_input(self):
        return self.category_input_box.text() # returns relevant data