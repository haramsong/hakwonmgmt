# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Schedule.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setWindowTitle("강좌 일정관리")
        Dialog.resize(540, 665)

        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(0, 30, 510, 20))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setText("강좌 일정 등록")

        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(50, 250, 440, 50))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 80, 441, 161))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")

        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setObjectName("gridLayout")

        title_arr = ["강      좌", "강      사", "시      즌", "시      간", "강  의  실"]
        for i in range(len(title_arr)):
            self.label = QtWidgets.QLabel(self.gridLayoutWidget)
            self.label.setText(title_arr[i])
            self.gridLayout.addWidget(self.label, i, 0, 1, 1)

        LE1_arr = [["self.lessonLE1", "x"], ["self.teacherLE1", "x"], ["self.seasonLE1", ""],
                   ["self.periodLE1", ""], ["self.roomLE1", ""]]
        for i in range(len(LE1_arr)):
            LE1_arr[i][0] = QtWidgets.QLineEdit(self.gridLayoutWidget)
            if LE1_arr[i][1] == "x":
               LE1_arr[i][0].setReadOnly(True)
               LE1_arr[i][0].setStyleSheet("background: lightgray")
            self.gridLayout.addWidget(LE1_arr[i][0], i, 1, 1, 1)

        LE2_arr = ["self.lessonLE2", "self.teacherLE2", "self.seasonLE2", "self.periodLE2", "self.roomLE2"]
        for i in range(len(LE2_arr)):
            LE2_arr[i] = QtWidgets.QLineEdit(self.gridLayoutWidget)
            LE2_arr[i].setReadOnly(True)
            LE2_arr[i].setStyleSheet("background: lightgray")
            self.gridLayout.addWidget(LE2_arr[i], i, 2, 1, 1)

        global days_arr
        days_arr = [["self.CB_1", "월"], ["self.CB_2", "화"], ["self.CB_3", "수"],
                    ["self.CB_4", "목"], ["self.CB_5", "금"], ["self.CB_6", "토"],
                    ["self.CB_7", "일"]]
        for i in range(len(days_arr)):
            days_arr[i][0] = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
            days_arr[i][0].setText(days_arr[i][1])
            self.horizontalLayout.addWidget(days_arr[i][0])

        tableWidget_hdr_arr = ["강의실", "시간", "월", "화", "수", "목", "금", "토", "일"]
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(10, 320, 511, 331))
        self.tableWidget.setColumnCount(len(tableWidget_hdr_arr))
        self.tableWidget.setRowCount(0)
        for i in range(len(tableWidget_hdr_arr)):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setHorizontalHeaderItem(i, item)
            item = self.tableWidget.horizontalHeaderItem(i)
            item.setText(tableWidget_hdr_arr[i])

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(420, 30, 93, 28))
        self.pushButton.setText("Add")
        self.pushButton.clicked.connect(self.go)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def go(self):
        print(days_arr[0][0].checkState(), days_arr[1][0].checkState(), days_arr[2][0].checkState(),
              days_arr[3][0].checkState(), days_arr[4][0].checkState(), days_arr[5][0].checkState(),
              days_arr[6][0].checkState())
        return

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate







if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

