#-*- coding : utf-8-*-

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
# from plot_pyqt import PlotCanvas
import ann


class annWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            with open("./qss/style.qss") as f:
                style = f.read()
                self.setStyleSheet(style)
        except:
            print("open stylesheet error")
        self.title = "ann application"
        self.top = 300
        self.left = 600
        self.width = 400
        self.height = 400
        self.iconName = "./imgs/hustlogo.png"
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.setDefault()
        self.drawBrowser()
        self.drawSplit()
        self.drawHiddenNums()
        self.drawActivateFunc()
        self.drawOptimizerFunc()
        self.drawEpochs()
        self.drawBatch()

        self.trainButton = self.createButton("Train", self.trainANN, 330, 320, 60, 30)
        self.runButton = self.createButton("Run", self.runANN, 330, 360, 60, 30)

        self.show()

    def setDefault(self):
        # self.fileName = ""
        self.testSize = 20
        self.hiddenNums = 25
        self.activateFunc = 'relu'
        self.optimizerFunc = 'RMSprop'
        self.epochs = 10
        self.batch = 50

    def drawBrowser(self):
        self.centralwidget = QWidget(self)
        self.csv_label = QLabel(self.centralwidget)
        self.csv_label.setGeometry(QtCore.QRect(10, 10, 80, 30))
        self.csv_label.setText("csv file: ")

        self.csv_lineEdit = QLineEdit(self)
        self.csv_lineEdit.setGeometry(QtCore.QRect(90, 10, 300, 30))
        self.annButton = self.createButton("Browse", self.getFileName, 330, 50, 60, 30)

    def drawSplit(self):
        self.split_label = QLabel("test_data size(%): ", self)
        self.split_label.setGeometry(QtCore.QRect(40, 80, 110, 30))

        self.split_lineEdit = QLineEdit(self)
        self.split_lineEdit.setGeometry(QtCore.QRect(160, 80, 50, 30))
        self.split_lineEdit.setText(str(self.testSize))

    def drawHiddenNums(self):
        self.hidden_nums = QLabel("hidden nums: ", self)
        self.hidden_nums.setGeometry(QtCore.QRect(40, 120, 110, 30))

        self.hidden_lineEdit = QLineEdit(self)
        self.hidden_lineEdit.setGeometry(QtCore.QRect(160, 120, 50, 30))
        self.hidden_lineEdit.setText(str(self.hiddenNums))

    def drawActivateFunc(self):
        self.ActivateFunc_label = QLabel("activate function: ", self)
        self.ActivateFunc_label.setGeometry(QtCore.QRect(40, 160, 110, 30))

        self.activate_cb = QComboBox(self)
        self.activate_cb.setGeometry(QtCore.QRect(160, 160, 80, 30))
        self.activate_cb.addItems(["sigmoid", "tanh", "relu"])
        self.activate_cb.currentIndexChanged.connect(self.activateSelection)

    def drawOptimizerFunc(self):
        self.optimizer_label = QLabel("optimizer: ", self)
        self.optimizer_label.setGeometry(QtCore.QRect(40, 200, 110, 30))

        self.optimizer_cb = QComboBox(self)
        self.optimizer_cb.setGeometry(QtCore.QRect(160, 200, 80, 30))
        self.optimizer_cb.addItems(["SGD", "adam", "RMSprop", "Adagrad"])
        self.optimizer_cb.currentIndexChanged.connect(self.optimizerSelection)

    def drawEpochs(self):
        self.epochs_label = QLabel("epochs: ", self)
        self.epochs_label.setGeometry(QtCore.QRect(40, 240, 110, 30))

        self.epochs_lineEdit = QLineEdit(self)
        self.epochs_lineEdit.setGeometry(QtCore.QRect(160, 240, 50, 30))
        self.epochs_lineEdit.setText(str(self.epochs))

    def drawBatch(self):
        self.batch_label = QLabel("batch size: ", self)
        self.batch_label.setGeometry(QtCore.QRect(40, 280, 110, 30))

        self.batch_lineEdit = QLineEdit(self)
        self.batch_lineEdit.setGeometry(QtCore.QRect(160, 280, 50, 30))
        self.batch_lineEdit.setText(str(self.batch))

    def activateSelection(self):
        self.activateFunc = self.activate_cb.currentText()

    def optimizerSelection(self):
        self.optimizerFunc = self.optimizer_cb.currentText()

    def getFileName(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Single File', './data', '*.csv')
        self.csv_lineEdit.setText(fileName)
        self.fileName = self.csv_lineEdit.text()

    def trainANN(self):
        # print("--------TRAINING--------")
        if self.fileName != "":
            self.testSize = int(self.split_lineEdit.text())
            self.hiddenNums = int(self.hidden_lineEdit.text())
            self.activateFunc = self.activate_cb.currentText()
            self.optimizerFunc = self.optimizer_cb.currentText()
            self.epochs = int(self.epochs_lineEdit.text())
            self.batch = int(self.batch_lineEdit.text())
            if self.testSize <= 40:

                self.results = ann.train(self.fileName, self.testSize, self.hiddenNums, self.activateFunc,
                                         self.optimizerFunc, self.epochs, self.batch)
            else:
                pass
        else:
            pass

        QMessageBox.about(self, "Results:", self.results)

    def runANN(self):
        ann.run(self.fileName)
        # mfig.show()
        # mfig = PlotCanvas(self)
        # figWindow = SecondWindow()
        # figWindow.show()
        # figWindow.exec_()

    def createButton(self, text, fun, x, y, l, w):
        pushButton = QPushButton(text, self)
        pushButton.setGeometry(QtCore.QRect(x, y, l, w))
        pushButton.clicked.connect(fun)
        return pushButton


def Main():
    m = annWindow()
    m.show()
    return m


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mWin = annWindow()
    sys.exit(app.exec_())