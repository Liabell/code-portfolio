from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *


class TransferTable(QtWidgets.QDialog):
    def __init__(self):
        super(TransferTable, self).__init__()
        self.setup_popup_Ui(self)

    def setup_popup_Ui(self, TransferTable):
        TransferTable.setWindowTitle("TransferTable")
        TransferTable.resize(448, 323)
        self.centralwidget = QtWidgets.QWidget(TransferTable)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 421, 271))
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
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 415, 265))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.action_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.action_label.setGeometry(QtCore.QRect(10, 10, 111, 41))
        self.action_label.setObjectName("action_label")
        self.line_1 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line_1.setGeometry(QtCore.QRect(10, 40, 391, 20))
        self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_1.setObjectName("line_1")
        self.from_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.from_label.setGeometry(QtCore.QRect(10, 60, 51, 31))
        self.from_label.setObjectName("from_label")
        self.to_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.to_label.setGeometry(QtCore.QRect(10, 110, 61, 21))
        self.to_label.setObjectName("to_label")
        self.amount_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.amount_label.setGeometry(QtCore.QRect(10, 150, 61, 21))
        self.amount_label.setObjectName("amount_label")
        self.line_2 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line_2.setGeometry(QtCore.QRect(10, 200, 391, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.submit_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.submit_button.setGeometry(QtCore.QRect(240, 230, 75, 23))
        self.submit_button.setObjectName("submit_button")
        self.cancel_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.cancel_button.setGeometry(QtCore.QRect(330, 230, 75, 23))
        self.cancel_button.setObjectName("pushButton_2")
        self.from_combo_box = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.from_combo_box.setGeometry(QtCore.QRect(50, 70, 221, 22))
        self.from_combo_box.setObjectName("from_combo_box")
        self.to_combo_box = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.to_combo_box.setGeometry(QtCore.QRect(50, 110, 221, 22))
        self.to_combo_box.setObjectName("to_combo_box")
        
        self.amount_input_box = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.amount_input_box.setGeometry(QtCore.QRect(50, 150, 221, 20))
        self.amount_input_box.setObjectName("amount_input_box")

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 1, 1, 1)
        self.popup_main_window.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.submit_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.retranslateUi(TransferTable)
        QtCore.QMetaObject.connectSlotsByName(TransferTable)

    def retranslateUi(self, TransferTable):
        _translate = QtCore.QCoreApplication.translate
        TransferTable.setWindowTitle(_translate("TransferTable", "TransferTable"))
        self.action_label.setText(_translate("TransferTable", "Transfer Money"))
        self.from_label.setText(_translate("TransferTable", "From"))
        self.to_label.setText(_translate("TransferTable", "To"))
        self.amount_label.setText(_translate("TransferTable", "Amount"))
        self.submit_button.setText(_translate("TransferTable", "Submit"))
        self.cancel_button.setText(_translate("TransferTable", "Cancel"))

    def get_transfer_input(self):
        ret_values = [self.from_combo_box.currentText(), self.to_combo_box.currentText(), self.amount_input_box.text()]
        return ret_values # returns relevant data