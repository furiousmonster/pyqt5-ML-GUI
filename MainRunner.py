#-*- coding : utf-8-*-

import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
import numpy as np
import pandas as pd
import pyqtgraph as pg
import ANNRunner

pg.setConfigOptions(leftButtonPan=False)
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "冷水机组回水温度预测"
        self.top = 300
        self.left = 500
        self.width = 900
        self.height = 500
        self.iconName = "./imgs/hustlogo.png"

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar().showMessage('Ready')

        self.setDefault()
        self.init_menu()
        self.init_tool()
        self.drawBrowser()
        self.setDataTable()
        self.set_layout()

        self.show()

    def setDefault(self):
        self.filename = "./data/3_chiller_demo.csv"
        self.featurename = "室外环境湿球温度"
        self.figure = pg.PlotWidget(title=self.featurename)

    def init_menu(self):
        self.statusBar().showMessage("文本状态栏")

        menu = self.menuBar()

        file_menu = menu.addMenu("文件")
        file_menu.addSeparator()

        new_action = QAction('新的文件', self)
        new_action.setStatusTip('打开新的文件')
        file_menu.addAction(new_action)


        exit_action = QAction('退出',self)
        exit_action.setStatusTip("点击退出应用程序")
        exit_action.triggered.connect(self.close)
        exit_action.setShortcut('Ctrl+Q')
        file_menu.addAction(exit_action)

    def init_tool(self):
        h_toolbar = self.addToolBar('工具栏')
        h_toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        ann_act = QAction(QtGui.QIcon('./imgs/hustlogo.png'), 'ann', self)
        ann_act.setShortcut('Ctrl+1')
        ann_act.setStatusTip('ANN Model')
        ann_act.triggered.connect(self.callANNRunner)
        h_toolbar.addAction(ann_act)

        exit_act = QAction(QtGui.QIcon('./imgs/hustlogo.png'), 'exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('Quit PyQt5')
        exit_act.triggered.connect(qApp.quit)
        h_toolbar.addAction(exit_act)

    def contextMenuEvent(self, event):
        ri_menu = QMenu(self)

        new_action = ri_menu.addAction("New")
        opn_action = ri_menu.addAction("Open")
        exit_action = ri_menu.addAction("Quit")
        action = ri_menu.exec_(self.mapToGlobal(event.pos()))

        if action == exit_action:
            qApp.quit()

    def drawBrowser(self):
        self.csv_lineEdit = QLineEdit(self)
        self.csv_lineEdit.setGeometry(QtCore.QRect(480, 30, 300, 30))
        self.browseButton = self.createButton("Browse", self.getFileName, 800, 30, 60, 30)

    def getFileName(self):
        fileNametemp, _ = QFileDialog.getOpenFileName(self, 'Single File', './data', '*.csv')
        self.csv_lineEdit.setText(fileNametemp)
        self.filename = self.csv_lineEdit.text()
        self.setDataTable()

    def set_layout(self):
        widget = QWidget()
        self.createUnitBox()
        self.createDataBox()
        self.createVisualBox()
        self.createFeatureBox()
        mainLayout = QGridLayout(self)
        vboxLayout = QGridLayout(self)
        hboxLayout = QGridLayout(self)
        hboxLayout.addWidget(self.visualBox, 0, 0)
        hboxLayout.addWidget(self.featureBox, 0, 1)
        vboxLayout.addWidget(self.dataBox, 0, 0)
        vboxLayout.addLayout(hboxLayout, 1, 0)
        mainLayout.addWidget(self.UnitBox, 0, 0)
        mainLayout.addLayout(vboxLayout, 0, 1)
        mainLayout.setColumnMinimumWidth(1, 700)
        mainLayout.setColumnMinimumWidth(0, 160)
        vboxLayout.setRowMinimumHeight(0, 160)
        hboxLayout.setColumnMinimumWidth(0, 500)
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    def createButton(self, text, fun, x, y, l, w):
        pushButton = QPushButton(text, self)
        pushButton.setGeometry(QtCore.QRect(x, y, l, w))
        pushButton.clicked.connect(fun)
        return pushButton

    def createUnitBox(self):
        self.UnitBox = QGroupBox("冷水机组选择")
        vlayout = QGridLayout()

        self.btn1 = QRadioButton("1号冷水机组")
        self.btn1.setChecked(False)
        self.btn1.toggled.connect(lambda: self.btnstate(self.btn1))

        self.btn2 = QRadioButton("2号冷水机组")
        self.btn2.setChecked(False)
        self.btn2.toggled.connect(lambda: self.btnstate(self.btn2))

        self.btn3 = QRadioButton("3号冷水机组")
        self.btn3.setChecked(True)
        self.btn3.toggled.connect(lambda: self.btnstate(self.btn3))

        self.btn4 = QRadioButton("4号冷水机组")
        self.btn4.setChecked(False)
        self.btn4.toggled.connect(lambda: self.btnstate(self.btn4))

        titleLabel = QLabel(' ')

        vlayout.addWidget(self.btn1, 0, 0)
        vlayout.addWidget(self.btn2, 1, 0)
        vlayout.addWidget(self.btn3, 2, 0)
        vlayout.addWidget(self.btn4, 3, 0)
        vlayout.addWidget(titleLabel, 4, 0, 8, 0)

        self.UnitBox.setLayout(vlayout)

    def createDataBox(self):
        self.dataBox = QGroupBox("数据显示")
        layout = QHBoxLayout()
        layout.addWidget(self.dataTableView)
        self.dataBox.setLayout(layout)

    def setDataTable(self):
        input_table_ori = pd.read_csv(self.filename, encoding='utf-8')
        input_table = input_table_ori.iloc[-51:-1, 1:]
        input_table_rows = input_table.shape[0]
        input_table_colunms = input_table.shape[1]
        input_table_header = input_table.columns.values.tolist()

        self.dataTable = QtGui.QStandardItemModel(input_table_rows, input_table_colunms)
        self.dataTable.setHorizontalHeaderLabels(input_table_header)
        for row in range(input_table_rows):
            input_table_rows_values = input_table.iloc[[row]]
            input_table_rows_values_array = np.array(input_table_rows_values)
            input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
            for column in range(input_table_colunms):
                input_table_items_list = input_table_rows_values_list[column]
                input_table_items = str(input_table_items_list)
                i = QtGui.QStandardItem(input_table_items)
                self.dataTable.setItem(row, column, i)

        self.dataTableView = QTableView()
        self.dataTableView.setModel(self.dataTable)
        self.dataTableView.show()

    def createVisualBox(self):
        self.visualBox = QGroupBox("可视化区域")
        vlayout = QHBoxLayout()
        vlayout.addWidget(self.figure)
        self.visualBox.setLayout(vlayout)

    def createFeatureBox(self):
        self.featureBox = QGroupBox("变量选择")
        vlayout = QGridLayout()

        self.btnn1 = QRadioButton("室外环境湿球温度")
        self.btnn1.setChecked(False)
        self.btnn1.toggled.connect(lambda: self.btnnstate(self.btnn1))

        self.btnn2 = QRadioButton("冷却水供水温度")
        self.btnn2.setChecked(False)
        self.btnn2.toggled.connect(lambda: self.btnnstate(self.btnn2))

        self.btnn3 = QRadioButton("冷却水回水温度")
        self.btnn3.setChecked(False)
        self.btnn3.toggled.connect(lambda: self.btnnstate(self.btnn3))

        self.btnn4 = QRadioButton("机组流量")
        self.btnn4.setChecked(False)
        self.btnn4.toggled.connect(lambda: self.btnnstate(self.btnn4))

        self.featurename_lineEdit = QLineEdit(self)
        self.featurename_lineEdit.setPlaceholderText('请输入变量名')
        self.featurenameButton = QPushButton('确认', self)
        self.featurenameButton.clicked.connect(self.getFeaturename)

        vlayout.addWidget(self.btnn1, 2, 0, 2, 2)
        vlayout.addWidget(self.btnn2, 3, 0, 3, 2)
        vlayout.addWidget(self.btnn3, 4, 0, 4, 2)
        vlayout.addWidget(self.btnn4, 5, 0, 5, 2)

        vlayout.addWidget(self.featurename_lineEdit, 8, 0, 8, 2)
        vlayout.addWidget(self.featurenameButton, 8, 2, 8, 2)

        self.featureBox.setLayout(vlayout)

    def getFeaturename(self):
        # if self.featurename_lineEdit != :
        self.featurename = self.featurename_lineEdit.text()
        self.plot_slot()

    def callANNRunner(self):
        self.m = ANNRunner.Main()

    def btnstate(self, btn):
        if btn.text() == "1号冷水机组":
            if btn.isChecked():
                btn.setStatusTip('1号冷水机组')
                print(btn.text() + " is selected")

        if btn.text() == "2号冷水机组":
            if btn.isChecked():
                btn.setStatusTip('2号冷水机组')
                print(btn.text() + " is selected")

        if btn.text() == "3号冷水机组":
            if btn.isChecked():
                self.filename = './data/3_chiller_demo.csv'
                btn.setStatusTip('3号冷水机组')
                print(btn.text() + "is selected")

        if btn.text() == "4号冷水机组":
            if btn.isChecked():
                btn.setStatusTip('4号冷水机组')
                print(btn.text() + " is selected")

    def btnnstate(self, btnn):
        if btnn.text() == "室外环境湿球温度":
            if btnn.isChecked():
                btnn.setStatusTip('室外环境湿球温度')
                self.featurename = btnn.text()
                self.plot_slot()

        if btnn.text() == "冷却水供水温度":
            if btnn.isChecked():
                btnn.setStatusTip('冷却水供水温度')
                self.featurename = btnn.text()
                self.plot_slot()

        if btnn.text() == "冷却水回水温度":
            if btnn.isChecked():
                btnn.setStatusTip('冷却水回水温度')
                self.featurename = btnn.text()
                self.plot_slot()

        if btnn.text() == "机组流量":
            if btnn.isChecked():
                btnn.setStatusTip('机组流量')
                self.featurename = btnn.text()
                self.plot_slot()

    def plot_slot(self):
        input_tablex = pd.read_csv(self.filename, encoding='utf-8')
        y = input_tablex[self.featurename]
        self.figure.clear()
        # self.figure.getAxis('bottom').setLabel('x')
        self.figure.setTitle(self.featurename)
        self.figure.plot(y)


class logindialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('登录')
        self.resize(200, 200)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        self.frame = QFrame(self)
        self.frame.move(20, 20)
        self.verticalLayout = QVBoxLayout(self.frame)
        # self.verticalLayout = QVBoxLayout()
        self.verticalLayout.addStretch(1)

        self.lineEdit_account = QLineEdit()
        self.lineEdit_account.setPlaceholderText("请输入账号")
        self.verticalLayout.addWidget(self.lineEdit_account)

        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText("请输入密码")
        self.verticalLayout.addWidget(self.lineEdit_password)

        self.pushButton_enter = QPushButton()
        self.pushButton_enter.setText("确定")
        self.verticalLayout.addWidget(self.pushButton_enter)

        self.pushButton_quit = QPushButton()
        self.pushButton_quit.setText("取消")
        self.verticalLayout.addWidget(self.pushButton_quit)

        self.pushButton_enter.clicked.connect(self.on_pushButton_enter_clicked)
        self.pushButton_quit.clicked.connect(QtCore.QCoreApplication.instance().quit)

    def on_pushButton_enter_clicked(self):
        if self.lineEdit_account.text() != "ningbo":
            return

        if self.lineEdit_password.text() != "666":
            return

        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = logindialog()
    if dialog.exec_() == QDialog.Accepted:
        mWin = mainWindow()
        mWin.show()
        sys.exit(app.exec_())
        input('ss')