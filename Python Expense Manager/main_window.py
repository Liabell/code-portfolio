import io
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QMessageBox, QDialog, QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from expense_report import Category
from transfer_money_table import TransferTable
from add_category_window import CategoryWindow
from add_revenue_window import RevenueWindow
from add_expense_window import ExpenseWindow
from pie_chart import PieChart

class PopupWindow(QDialog): # if all else fails use this method for popup windows
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Popup Window')
        self.label = QLabel('Enter some text:')
        self.text_edit = QLineEdit()
        self.ok_button = QPushButton('OK')
        self.ok_button.clicked.connect(self.accept)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.categories = []
        self.table_counter = 0
        self.setupUi(self)
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(636, 573)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 611, 511))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.main_window = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.main_window.setContentsMargins(0, 0, 0, 0)
        self.main_window.setObjectName("main_window")
        self.grid_1 = QtWidgets.QGridLayout()
        self.grid_1.setObjectName("grid_1")
        self.grid_1_vertical_layout = QtWidgets.QVBoxLayout()
        self.grid_1_vertical_layout.setObjectName("grid_1_vertical_layout")
        self.scrollArea = QtWidgets.QScrollArea(self.gridLayoutWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 603, 470))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.transaction_table = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.transaction_table.setGeometry(QtCore.QRect(10, 120, 261, 111))
        self.transaction_table.setObjectName("transaction_table")
        self.transaction_table.setColumnCount(2)
        self.transaction_table.setRowCount(0) # this value determines the number of rows in the table, probably need to kill the table and open it again while also changing this value to the size of the array that contains the transactions

        item = QtWidgets.QTableWidgetItem()
        self.transaction_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.transaction_table.setHorizontalHeaderItem(1, item)

        self.Total_label_group_box = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.Total_label_group_box.setGeometry(QtCore.QRect(10, 250, 91, 41))
        self.Total_label_group_box.setTitle("")
        self.Total_label_group_box.setObjectName("Total_label_group_box")
        self.total_label = QtWidgets.QLabel(self.Total_label_group_box)
        self.total_label.setGeometry(QtCore.QRect(10, 10, 71, 21))
        self.total_label.setObjectName("total_label")
        self.Total_value_group_box = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.Total_value_group_box.setGeometry(QtCore.QRect(170, 250, 101, 41))
        self.Total_value_group_box.setTitle("")
        self.Total_value_group_box.setObjectName("Total_value_group_box")
        self.total_value_label = QtWidgets.QLineEdit(self.Total_value_group_box)
        self.total_value_label.setGeometry(QtCore.QRect(10, 12, 81, 21))
        self.total_value_label.setObjectName("total_value_label")
        self.category_selector = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.category_selector.setGeometry(QtCore.QRect(10, 90, 261, 21))
        self.category_selector.setObjectName("category_selector")

        self.category_selector.currentIndexChanged.connect(self.update_transaction_table)

        self.line = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line.setGeometry(QtCore.QRect(10, 380, 561, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.exit_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)

        self.exit_button.clicked.connect(self.close_application)

        self.exit_button.setGeometry(QtCore.QRect(490, 400, 75, 23))
        self.exit_button.setObjectName("exit_button")
        self.piechart_graphic = QtWidgets.QGraphicsView(self.scrollAreaWidgetContents)
        self.piechart_graphic.setGeometry(QtCore.QRect(310, 90, 251, 231))
        self.piechart_graphic.setObjectName("piechart_graphic")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.grid_1_vertical_layout.addWidget(self.scrollArea)
        self.grid_1.addLayout(self.grid_1_vertical_layout, 1, 0, 1, 1)
        self.main_window.addLayout(self.grid_1, 1, 0, 1, 1)
        self.grid4 = QtWidgets.QGridLayout()
        self.grid4.setObjectName("grid4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_category_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.add_category_button.setObjectName("add_category_button")
        self.horizontalLayout.addWidget(self.add_category_button)

        self.add_category_button.clicked.connect(self.open_add_category)

        self.add_revenue_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.add_revenue_button.setObjectName("add_revenue_button")
        self.horizontalLayout.addWidget(self.add_revenue_button)

        self.add_revenue_button.clicked.connect(self.open_add_revenue)

        self.add_expense_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.add_expense_button.setObjectName("add_expense_button")
        self.horizontalLayout.addWidget(self.add_expense_button)

        self.add_expense_button.clicked.connect(self.open_add_expense)

        self.transfer_money_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.transfer_money_button.setObjectName("transfer_money_button")
        self.horizontalLayout.addWidget(self.transfer_money_button)

        self.transfer_money_button.clicked.connect(self.open_transfer_money)

        self.grid4.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.main_window.addLayout(self.grid4, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 636, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Expense Manager"))

        item = self.transaction_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Item"))
        item = self.transaction_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Price"))
        __sortingEnabled = self.transaction_table.isSortingEnabled()
        self.transaction_table.setSortingEnabled(False)

        self.transaction_table.setSortingEnabled(__sortingEnabled)
        self.total_label.setText(_translate("MainWindow", "Total"))
        self.total_value_label.setText(_translate("MainWindow", ""))

        self.exit_button.setText(_translate("MainWindow", "Exit"))
        self.add_category_button.setText(_translate("MainWindow", "Add Category"))
        self.add_revenue_button.setText(_translate("MainWindow", "Add Revenue"))
        self.add_expense_button.setText(_translate("MainWindow", "Add Expense"))
        self.transfer_money_button.setText(_translate("MainWindow", "Transfer Money"))
    
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def open_add_category(self):
        self.popup = CategoryWindow() # type of popup winow

        if self.popup.exec_() == QtWidgets.QDialog.Accepted: # submit was pressed
            _translate = QtCore.QCoreApplication.translate
            
            new_category = self.popup.get_category_input()

            self.categories.append(Category(str(new_category))) # array of user entered categories

            self.category_selector.addItem("")
            self.category_selector.setItemText(int(self.table_counter), _translate("MainWindow", self.categories[len(self.categories) - 1]._category))
            self.table_counter += 1
            self.open_category_success_window(str(new_category))

        if self.category_selector.currentText() != '':
            self.update_transaction_table()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def update_transaction_table(self):
        if len(self.categories) != 0:
            self.transaction_table.clearContents()
            _translate = QtCore.QCoreApplication.translate
            selected_category = self.category_selector.currentText()

            category_index = 0
            current_wallet = []
            for i in range (len(self.categories)): # determines which category to modify
                if self.categories[i]._category == selected_category:
                    category_index = i
            
            current_wallet = self.categories[category_index]

            output_buffer = io.StringIO()
            print(current_wallet, file=output_buffer)
            output = output_buffer.getvalue()
            
            line_index = 0
            table_name = ''
            total = 0
            transactions = []
            for line in output.splitlines():
                if line_index == 0:
                    table_name = line.replace("*", "")

                elif line_index == len(output.splitlines()) - 1:
                    total = float(line[8:])
                else:
                    line = ",".join(line.split()).replace(" ", ",")
                    line = line.split(",")
                    if len(line) != 2:
                        new_line = [line[0], '']
                        for i in range(1, len(line)):
                            if i != len(line) - 1:
                                new_line[0] = new_line[0] + " " + line[i]
                        new_line[1] = line[len(line) - 1]
                        line = new_line
                    transactions.append(line)
                line_index += 1

            step = 0
            self.transaction_table.setRowCount(len(transactions))
            for pair in transactions:
                item = QtWidgets.QTableWidgetItem()
                self.transaction_table.setItem(step, 0, item)
                item = QtWidgets.QTableWidgetItem()
                self.transaction_table.setItem(step, 1, item)

                item = self.transaction_table.item(step, 0)
                item.setText(_translate("MainWindow", pair[0]))
                item = self.transaction_table.item(step, 1)
                item.setText(_translate("MainWindow", pair[1]))
                step += 1
            
            total = round(total, 2) # forcing 2dp
            self.total_value_label.setText(str(total))
            self.draw_pie_chart()
            return 0
        else:
            return 0

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def draw_pie_chart(self):
        self.piechart = PieChart()
        self.piechart_item = self.piechart.generate_pie_chart(self.categories)
        if self.piechart_item is not None: # only draws pie chart if there is one stored in memory
            self.piechart.scene.addItem(self.piechart_item)
            self.piechart_graphic.setScene(self.piechart.scene)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def open_add_revenue(self):
        _translate = QtCore.QCoreApplication.translate
        self.popup = RevenueWindow() # type of popup winow
        
        for i in range(len(self.categories)):
            self.popup.to_combo_box.addItem("")
            self.popup.to_combo_box.setItemText(i, _translate("MainWindow", self.categories[i]._category))
        
        if self.popup.exec_() == QtWidgets.QDialog.Accepted: # submit was pressed
            new_revenue = self.popup.get_revenue_input()

            category_index = -1
            for i in range (len(self.categories)): # determines which category to modify
                if self.categories[i]._category == new_revenue[0]:
                    category_index = i

            if category_index != -1 and new_revenue[2].replace(".", "").isnumeric(): # rejects if it has an invalid symbol, including '-'
                self.categories[category_index].add_revenue(float(new_revenue[2]), new_revenue[1])
                self.open_revenue_success_window(new_revenue[0], new_revenue[1], new_revenue[2])
                    
            else:
                self.open_revenue_fail_window(new_revenue[0])

        if self.category_selector.currentText() != '':
            self.update_transaction_table()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def open_add_expense(self):
        _translate = QtCore.QCoreApplication.translate
        self.popup = ExpenseWindow()

        for i in range(len(self.categories)):
            self.popup.to_combo_box.addItem("")
            self.popup.to_combo_box.setItemText(i, _translate("MainWindow", self.categories[i]._category))

        if self.popup.exec_() == QtWidgets.QDialog.Accepted:
            new_expense = self.popup.get_expense_input()

            category_index = -1
            for i in range (len(self.categories)): # determines which category to modify
                if self.categories[i]._category == new_expense[0]:
                    category_index = i

            if category_index != -1 and new_expense[2].replace(".", "").isnumeric() and self.categories[category_index].check_category_balance(float(new_expense[2])): # rejects if it has an invalid symbol, including '-'
                self.categories[category_index].add_expense(float(new_expense[2]), new_expense[1])
                self.open_expense_success_window(new_expense[0], new_expense[1], new_expense[2])
            else:
                self.open_expense_fail_window(new_expense[0])

        if self.category_selector.currentText() != '':
            self.update_transaction_table()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def open_transfer_money(self):
        _translate = QtCore.QCoreApplication.translate
        self.popup = TransferTable()
        
        for i in range(len(self.categories)):
            self.popup.from_combo_box.addItem("")
            self.popup.from_combo_box.setItemText(i, _translate("MainWindow", self.categories[i]._category))
            self.popup.to_combo_box.addItem("")
            self.popup.to_combo_box.setItemText(i, _translate("MainWindow", self.categories[i]._category))

        if self.popup.exec_() == QtWidgets.QDialog.Accepted:
            new_transfer = self.popup.get_transfer_input()
            
            category_index_1 = -1
            for i in range (len(self.categories)): # determines which category to take money from
                if self.categories[i]._category == new_transfer[0]:
                    category_index_1 = i

            category_index_2 = -1
            for i in range (len(self.categories)): # determines which category to recieve money
                if self.categories[i]._category == new_transfer[1]:
                    category_index_2 = i

            if category_index_1 != -1 and new_transfer[0] != new_transfer[1] and new_transfer[2].replace(".", "").isnumeric():
                self.categories[category_index_1].transfer_money(float(new_transfer[2]), self.categories[category_index_2])
                self.open_money_transfer_success_window(new_transfer)
            else:
                self.open_transfer_fail_window(self.categories[category_index_1]._category, self.categories[category_index_2]._category)

        if self.category_selector.currentText() != '':
            self.update_transaction_table()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def open_money_transfer_success_window(self, transfer):
        show_msg = QMessageBox(QMessageBox.Information,
            'Money Transferred Successfully',
            "Thank you! $"+ transfer[2] +" was successfully transferred from '"+ transfer[0] +"' to '"+ transfer[1] +"'",
            QMessageBox.Ok)
        show_msg.exec_()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def open_category_success_window(self, name):
        show_msg = QMessageBox(QMessageBox.Information,
            'Category Successfully Added',
            "Category name: \""+ name +"\" has successfully been added as a category",
            QMessageBox.Ok)
        show_msg.exec_()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def open_revenue_success_window(self, name, revenue_name, amount):
        show_msg = QMessageBox(QMessageBox.Information,
            'Revenue Successfully Added',
            "Category name: \""+ name +"\" has successfully been updated with a revenue named "+ revenue_name +" of: $"+ amount +"",
            QMessageBox.Ok)
        show_msg.exec_()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def open_revenue_fail_window(self, name):
        show_msg = QMessageBox(QMessageBox.Critical,
            'Revenue Blocked',
            "Category name: \""+ name +"\" has failed to add the revenue specified, please try again",
            QMessageBox.Ok)
        show_msg.exec_()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def open_expense_success_window(self, name, expense_name, amount):
        show_msg = QMessageBox(QMessageBox.Information,
            'Expense Successfully Added',
            "Category name: \""+ name +"\" has successfully been updated with a revenue named "+ expense_name +" of: $"+ amount +"",
            QMessageBox.Ok)
        show_msg.exec_()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def open_expense_fail_window(self, name):
        show_msg = QMessageBox(QMessageBox.Critical,
            'Expense Blocked',
            "Category name: \""+ name +"\" has failed to add the expense specified, please try again. Note that you are not supposed to include \'-\' symbols in the input field and amount cannot exceed the current total",
            QMessageBox.Ok)
        show_msg.exec_()
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def open_transfer_fail_window(self, name1, name2):
        show_msg = QMessageBox(QMessageBox.Critical,
            'Transfer Blocked',
            "Transfer from "+ name1 +" to "+ name2 +" has Terminated or Failed, Please try again. Note that money cannot be sent between the same categories and the amount must be positive",
            QMessageBox.Ok)
        show_msg.exec_()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def close_application(self):
        # show a confirmation message-box
        confirmation = QMessageBox.question(self, "Confirm Close",
            "Are you sure you want to close this window",
            QMessageBox.Yes | QMessageBox.No |
            QMessageBox.Cancel, QMessageBox.Cancel)
        if confirmation == QMessageBox.Yes:
            sys.exit()
        if confirmation == QMessageBox.No:
            pass
        if confirmation == QMessageBox.Cancel:
            pass

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def open_main_window():
    app = QtWidgets.QApplication(sys.argv)
    launch_gui = Ui_MainWindow()
    launch_gui.show()
    app.exec()