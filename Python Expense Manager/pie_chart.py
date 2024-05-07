import matplotlib.pyplot as plt
from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import QByteArray, QBuffer, QIODevice
import io


class PieChart(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pie Chart")
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.setSceneRect(0, 0, 800, 800)

    def generate_pie_chart(self, categories):
        _translate = QtCore.QCoreApplication.translate
        self.slices = []
        self.category_names = []
        self.rendering = False

        for i in range(len(categories)):
            self.slices.append(0)
            self.category_names.append('')

            current_wallet = categories[i]
            
            output_buffer = io.StringIO()
            print(current_wallet, file=output_buffer)
            output = output_buffer.getvalue()
            
            line_index = 0
            table_name = ''
            total = 0
            transactions = []

            for line in output.splitlines(): # separates transaction data
                if line_index == 0:
                    table_name = line.replace("*", "")

                elif line_index == len(output.splitlines()) - 1:
                    total = float(line[8:])
                else:
                    line = ",".join(line.split()).replace(" ", ",")
                    line = line.split(",")
                    if len(line) != 2:
                        new_line = [line[0], '']
                        for j in range(1, len(line)):
                            if j != len(line) - 1:
                                new_line[0] = new_line[0] + " " + line[j]
                        new_line[1] = line[len(line) - 1]
                        line = new_line
                    transactions.append(line)
                line_index += 1

            for transaction in transactions: # populates arrays with relevant transaction data
                if float(transaction[1]) < 1:
                    self.slices[i] += float(transaction[1]) * -1
                    self.category_names[i] = table_name
                
        for i in range(len(self.slices)): # determines if pie chart should be rendered and stored in memory
            if self.slices[i] != 0 and self.category_names[i] != '':
                self.rendering = True

        if self.rendering: # draws pie chart
            plt.figure(figsize=(2, 2)) # this determines the size of the pie chart
            plt.pie(self.slices,
                    labels=self.category_names,
                    startangle=-110,
                    shadow=False,
                    autopct="%1.2f%%",
                    labeldistance=1.05) # populates the pie chart objects with transaction data

            buf = QByteArray()
            buffer = QBuffer(buf)
            buffer.open(QIODevice.WriteOnly) # creates buffer

            plt.tight_layout() # scales image to fix text in window
            plt.savefig(buffer, format='png') # renders to ouput buffer
            qimage = QImage.fromData(buf) # QImage
            pixmap = QPixmap.fromImage(qimage) # QPixmap
            pixmap_item = QGraphicsPixmapItem(pixmap) # QGraphicsPixmapItem
            return pixmap_item # returns item containing pie chart render