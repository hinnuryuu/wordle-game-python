import linecache
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

import wordle

trialCount = 0


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(252, 308)
        MainWindow.setMinimumSize(QtCore.QSize(252, 308))
        MainWindow.setMaximumSize(QtCore.QSize(252, 308))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.restartButton = QtWidgets.QPushButton(self.centralwidget)
        self.restartButton.setGeometry(QtCore.QRect(150, 270, 101, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.restartButton.setFont(font)
        self.restartButton.setObjectName("restartButton")
        self.submitButton = QtWidgets.QPushButton(self.centralwidget)
        self.submitButton.setGeometry(QtCore.QRect(0, 270, 101, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.submitButton.setFont(font)
        self.submitButton.setObjectName("submitButton")
        self.submitButton.setEnabled(False)
        self.trialTable = QtWidgets.QTableWidget(self.centralwidget)
        self.trialTable.setEnabled(True)
        self.trialTable.setGeometry(QtCore.QRect(0, 0, 251, 211))
        self.trialTable.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.trialTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.trialTable.setObjectName("trialTable")
        self.trialTable.setColumnCount(2)
        self.trialTable.setRowCount(6)
        item = QtWidgets.QTableWidgetItem()
        self.trialTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.trialTable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.trialTable.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.trialTable.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.trialTable.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.trialTable.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.trialTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.trialTable.setHorizontalHeaderItem(1, item)
        self.wordleText = QtWidgets.QLineEdit(self.centralwidget)
        self.wordleText.setGeometry(QtCore.QRect(70, 229, 113, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.wordleText.setFont(font)
        self.wordleText.setText("")
        self.wordleText.setMaxLength(5)
        self.wordleText.setObjectName("wordleText")
        MainWindow.setCentralWidget(self.centralwidget)
        self.restart()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.submitButton.clicked.connect(self.submit)
        self.restartButton.clicked.connect(self.restart)
        self.wordleText.textChanged.connect(self.limit)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Wordle"))
        self.restartButton.setText(_translate("MainWindow", "重新开始"))
        self.submitButton.setText(_translate("MainWindow", "提交"))
        item = self.trialTable.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "第一试"))
        item = self.trialTable.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "第二试"))
        item = self.trialTable.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "第三试"))
        item = self.trialTable.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "第四试"))
        item = self.trialTable.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "第五试"))
        item = self.trialTable.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "第六试"))
        item = self.trialTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "输入单词"))
        item = self.trialTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "检查标志"))

    def submit(self):
        if self.checkValid():
            if trialCount <= 6:
                flag = self.checkRight()
                if flag:
                    self.submitButton.setText("已完成")
                    self.submitButton.setEnabled(False)
        else:
            self.wordleText.setText("无此单词")

    def restart(self):
        wordle.prepare()
        self.trialTable.clearContents()
        global trialCount
        trialCount = 0
        self.submitButton.setText("提交")
        if len(self.wordleText.text()) == 5:
            self.submitButton.setEnabled(True)
        self.wordleText.setEnabled(True)

    def limit(self):
        if len(self.wordleText.text()) < 5:
            self.submitButton.setEnabled(False)
        else:
            self.submitButton.setEnabled(True)

    def checkValid(self):
        for i in range(1, wordle.count + 1):
            word = linecache.getline('wordle_words.txt', i).strip()
            if word == self.wordleText.text():
                return True
        return False

    def checkRight(self):
        position = 0
        global trialCount
        judge = ""
        word = self.wordleText.text().lower()
        for ch in word:
            flag = wordle.word.find(ch)
            if flag == -1:
                judge += '×'
            elif flag != -1 and ch != wordle.word[position]:
                judge += '〇'
            else:
                judge += '√'
            position += 1
        self.trialTable.setItem(trialCount, 0, QTableWidgetItem(word))
        self.trialTable.setItem(trialCount, 1, QTableWidgetItem(judge))
        trialCount += 1
        if judge == "√√√√√":
            return True
        else:
            if trialCount == 6:
                self.submitButton.setText("答案已公布")
                self.wordleText.setText(wordle.word)
                self.wordleText.setEnabled(False)
                self.submitButton.setEnabled(False)
            return False


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
