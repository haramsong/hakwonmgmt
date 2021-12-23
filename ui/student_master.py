# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'student_master.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setWindowTitle("수강생 기준정보")
        Dialog.resize(490, 660)

        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(130, 600, 340, 30))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 20, 490, 40))
        font = QtGui.QFont()
        font.setFamily("에스코어 드림 6 Bold")
        font.setPointSize(24)
        # font.setBold(True)
        # font.setWeight(75)
        self.label.setFont(font)
        self.label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label.setLineWidth(1)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText("수강생 등록")

        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 70, 450, 320))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(10, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setObjectName("gridLayout")

        item_title = ["ID", "이름", "연락처", "성별", "직업", "직장/학교명", "생넌월일", "주소", "비고1","비고2"]
        for i in range(len(item_title)):
            self.label = QtWidgets.QLabel(self.gridLayoutWidget)
            self.label.setText(item_title[i])
            self.gridLayout.addWidget(self.label, i, 0, 1, 1)

        self.groupBox = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 30))
        self.idLabel = QtWidgets.QLabel(Dialog)
        self.idLabel.setText(" ")
        self.gridLayout.addWidget(self.idLabel, 0, 1, 1, 1)

        self.nameLE = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.nameLE, 1, 1, 1, 1)

        self.phoneLE = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.phoneLE, 2, 1, 1, 1)

        gender_arr = [["남", 20, 5, 50, 20], ["여", 100, 5, 50, 20]]
        self.groupBox = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 30))
        for i in range(len(gender_arr)):
            self.radioButton = QtWidgets.QRadioButton(self.groupBox)
            self.radioButton.setText(gender_arr[i][0])
            self.radioButton.setGeometry(QtCore.QRect(gender_arr[i][1],gender_arr[i][2],gender_arr[i][3],gender_arr[i][4]))
            if i == 0:
               self.radioButton.setChecked(True)
        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setText("활성")
        self.checkBox.setChecked(True)
        self.checkBox.setGeometry(QtCore.QRect(250, 5, 50, 20))
        self.gridLayout.addWidget(self.groupBox, 3, 1, 1, 1)

        comboBox_arr = ["학생", "직장인", "주부", "무직", "구직중"]
        self.comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        for i in range(len(comboBox_arr)):
            self.comboBox.addItem("")
            self.comboBox.setItemText(i, comboBox_arr[i])
        self.gridLayout.addWidget(self.comboBox, 4, 1, 1, 1)

        self.workPlcLE = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.workPlcLE, 5, 1, 1, 1)

        self.birthDayLE = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.birthDayLE, 6, 1, 1, 1)

        self.addressLE = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.addressLE, 7, 1, 1, 1)

        self.remark1LE = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.remark1LE, 8, 1, 1, 1)

        self.remark2LE = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.remark2LE, 9, 1, 1, 1)

        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(20, 430, 450, 150))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setRowCount(0)
        lesson_apply_hdr_arr = ["시즌 ID", "강좌 ID", "강좌명", "강사", "강의실", "시작일", "종료일", "등록일", "정지일"]
        for i in range(len(lesson_apply_hdr_arr)):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item)
            item = self.tableWidget.horizontalHeaderItem(i)
            item.setText(lesson_apply_hdr_arr[i])

        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(310, 410, 120, 20))
        self.checkBox.setText("활성 정보만 출력")

        self.toolButton = QtWidgets.QToolButton(Dialog)
        self.toolButton.setGeometry(QtCore.QRect(440, 400, 30, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/add-file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton.setIcon(icon)
        self.toolButton.setIconSize(QtCore.QSize(30, 30))


        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 410, 65, 15))
        font = QtGui.QFont()
        font.setFamily("에스코어 드림 6 Bold")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setText("강좌 등록")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

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

