from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *


class ExpenseWindow(QtWidgets.QDialog):
    def __init__(self):
        super(ExpenseWindow, self).__init__()
        self.setupUi(self)

    def setupUi(self, ExpenseWindow):
        ExpenseWindow.setObjectName("ExpenseWindow")
        ExpenseWindow.resize(442, 282)
        self.centralwidget = QtWidgets.QWidget(ExpenseWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 421, 261))
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
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 415, 255))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.window_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.window_label.setGeometry(QtCore.QRect(10, 10, 111, 41))
        self.window_label.setObjectName("window_label")
        self.line_1 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line_1.setGeometry(QtCore.QRect(10, 40, 391, 20))
        self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_1.setObjectName("line_1")
        self.to_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.to_label.setGeometry(QtCore.QRect(10, 80, 41, 21))
        self.to_label.setObjectName("to_label")
        self.amount_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.amount_label.setGeometry(QtCore.QRect(10, 160, 41, 21))
        self.amount_label.setObjectName("amount_label")
        self.line_2 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line_2.setGeometry(QtCore.QRect(10, 200, 391, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.submit_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.submit_button.setGeometry(QtCore.QRect(240, 220, 75, 23))
        self.submit_button.setObjectName("submit_button")
        self.cancel_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.cancel_button.setGeometry(QtCore.QRect(330, 220, 75, 23))
        self.cancel_button.setObjectName("cancel_button")
        self.to_combo_box = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.to_combo_box.setGeometry(QtCore.QRect(60, 80, 221, 22))
        self.to_combo_box.setObjectName("to_combo_box")
        self.amount_input_box = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.amount_input_box.setGeometry(QtCore.QRect(60, 160, 221, 20))
        self.amount_input_box.setObjectName("amount_input_box")
        self.name_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.name_label.setGeometry(QtCore.QRect(10, 120, 51, 16))
        self.name_label.setObjectName("name_label")
        self.name_input_box = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.name_input_box.setGeometry(QtCore.QRect(60, 120, 221, 20))
        self.name_input_box.setObjectName("name_input_box")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.popup_main_window.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.submit_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.retranslateUi(ExpenseWindow)
        QtCore.QMetaObject.connectSlotsByName(ExpenseWindow)

    def retranslateUi(self, ExpenseWindow):
        _translate = QtCore.QCoreApplication.translate
        ExpenseWindow.setWindowTitle(_translate("ExpenseWindow", "ExpenseWindow"))
        self.window_label.setText(_translate("ExpenseWindow", "Add Expense"))
        self.to_label.setText(_translate("ExpenseWindow", "To"))
        self.amount_label.setText(_translate("ExpenseWindow", "Amount"))
        self.submit_button.setText(_translate("ExpenseWindow", "Submit"))
        self.cancel_button.setText(_translate("ExpenseWindow", "Cancel"))
        self.name_label.setText(_translate("ExpenseWindow", "Name"))

    def get_expense_input(self):
        ret_values = [self.to_combo_box.currentText(), self.name_input_box.text(), self.amount_input_box.text()]
        return ret_values # returns relevant data
