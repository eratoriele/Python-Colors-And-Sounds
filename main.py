from re import S
from PyQt5 import QtGui
import PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QGridLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QIntValidator
from PyQt5.QtCore import Qt, QTimer, QDateTime
import sys
import random
import winsound
import time
from threading import Thread


windowWidth = 1500
windowHeight = 1000
rectangleWidth = 150
rectangleHeight = 100
vertRectCount = 10
horRectCount = 10
frameTime = 10
rectQueue = []
soundQueue = []


class DataEntryWindow(QDialog):
    def __init__(self, parent=None):
        super(DataEntryWindow, self).__init__(parent)

        self.setWindowTitle("Enter Size Details")
        self.resize(300, 120)
        layout = QGridLayout(self)

        self.onlyInt = QIntValidator()

        self.vertRectCountLabel = QLabel("<font size=\"4\"> Verticle rectangle count: </font>")
        self.vertRectCountLineEdit = QLineEdit(self)
        self.vertRectCountLineEdit.setValidator(self.onlyInt)
        layout.addWidget(self.vertRectCountLabel, 0, 0)
        layout.addWidget(self.vertRectCountLineEdit, 0, 1)

        self.horRectCountLabel = QLabel("<font size=\"4\"> Horizontal rectangle count: </font>")
        self.horRectCountLineEdit = QLineEdit(self)
        self.horRectCountLineEdit.setValidator(self.onlyInt)
        layout.addWidget(self.horRectCountLabel, 1, 0)
        layout.addWidget(self.horRectCountLineEdit, 1, 1)

        self.rectHeightLabel = QLabel("<font size=\"4\"> Rectangle height: </font>")
        self.rectHeightLineEdit = QLineEdit(self)
        self.rectHeightLineEdit.setValidator(self.onlyInt)
        layout.addWidget(self.rectHeightLabel, 2, 0)
        layout.addWidget(self.rectHeightLineEdit, 2, 1)

        self.rectWidthLabel = QLabel("<font size=\"4\"> Rectangle width: </font>")
        self.rectWidthLineEdit = QLineEdit(self)
        self.rectWidthLineEdit.setValidator(self.onlyInt)
        layout.addWidget(self.rectWidthLabel, 3, 0)
        layout.addWidget(self.rectWidthLineEdit, 3, 1)
                
        self.button = QPushButton("Ok", self)
        self.button.clicked.connect(self.handleData)

        layout.addWidget(self.button, 4, 0, 1, 2)

    def handleData(self):
        # Check if given data is not empty
        if self.vertRectCountLineEdit.text() != "" and self.horRectCountLineEdit.text() != "" and \
            self.rectHeightLineEdit.text() != "" and self.rectWidthLineEdit.text() != "":
            global windowWidth, windowHeight, rectangleWidth, rectangleHeight, horRectCount, vertRectCount
            rectangleWidth = int(self.rectWidthLineEdit.text())
            rectangleHeight = int(self.rectHeightLineEdit.text())
            horRectCount = int(self.horRectCountLineEdit.text())
            vertRectCount = int(self.vertRectCountLineEdit.text())
            windowWidth = rectangleWidth * vertRectCount
            windowHeight = rectangleHeight * horRectCount

            self.accept()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "PyQt5 Rectangles"
        self.top = 100
        self.left = 100
        self.width = windowWidth
        self.height = windowHeight

        self.moveRect = -1

        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def paintEvent(self, e):
        painter = QPainter(self)

        rowNumber = 0
        for column in range(len(rectQueue)):
            for color in rectQueue[column]:
                painter.setPen(QPen(color, 0, Qt.SolidLine))
                painter.setBrush(QBrush(color, Qt.SolidPattern))
                if column % 2 == 0:
                    painter.drawRect(column * rectangleWidth,
                                    rowNumber * rectangleHeight - self.moveRect,
                                    rectangleWidth, rectangleHeight)
                else:
                    painter.drawRect(column * rectangleWidth,
                                    (9 - rowNumber) * rectangleHeight + self.moveRect,
                                    rectangleWidth, rectangleHeight)
                rowNumber += 1
            rowNumber = 0

        self.moveRect += 1

        if self.moveRect >= rectangleHeight:
            for column in range(len(rectQueue)):
                rectQueue[column][:-1] = rectQueue[column][1:]
                # -1th rectangle will be deleted, so add it to the sound queue to make a beep out of it
                soundQueue.append(rectQueue[column][-1].red() + rectQueue[column][-1].green() + rectQueue[column][-1].blue())
                rectQueue[column][-1] = QColor(random.randint(0, 255),
                                           random.randint(0, 255), random.randint(0, 255))
                self.moveRect = 0


def SoundThread():
    #To always do some beeps, each beep should take 
    # (amount of time needed to move a rectangle one place up/down) / (amount of rectangles to be removed)  
    duration = int((rectangleHeight * frameTime) / 10)
    while True:
        if len(soundQueue) > 0:
            soundFreq = soundQueue.pop()
            winsound.Beep(soundFreq, duration)
    

if __name__ == "__main__":
    for i in range(vertRectCount):
        rectQueue.append([])
        for _ in range(horRectCount + 1):
            rectQueue[i].append(QColor(random.randint(0, 255),
                            random.randint(0, 255), random.randint(0, 255)))
                            
    App = QApplication(sys.argv)

    login = DataEntryWindow()

    if login.exec_() == QDialog.Accepted:
        window = Window()

        timer = QTimer()
        timer.timeout.connect(window.update)
        timer.start(frameTime)

        t1 = Thread(target=SoundThread)
        t1.daemon = True
        t1.start()

        sys.exit(App.exec())