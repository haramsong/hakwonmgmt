import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pandas as pd
import numpy as np
from datetime import *
import copy

class Ui_Season_Period(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("시즌 시간 관리")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setFixedSize(540, 665)

        self.label = QLabel(self)
        self.label.setGeometry(QRect(0, 15, 510, 40))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("시즌 시간 등록")
        global_funtion().fontSetting(self.label, '6B', 24, " ")  # "에스코어 드림 6 Bold", PointSize(24)

        self.gridLayoutWidget = QWidget(self)
        self.gridLayoutWidget.setGeometry(QRect(50, 80, 440, 120))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")

        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setObjectName("gridLayout")

        title_arr = ["시       즌", "시간 ID/내용", "시간 간격" ]
        for i in range(len(title_arr)):
            self.label = QLabel(self.gridLayoutWidget)
            self.label.setText(title_arr[i])
            self.gridLayout.addWidget(self.label, i, 0, 1, 1)

        self.seasonLE1 = QLineEdit(self.gridLayoutWidget)
        self.seasonLE1.setText(master_ID)
        self.seasonLE1.setReadOnly(True)
        self.seasonLE1.setStyleSheet("background: lightgray")
        self.gridLayout.addWidget(self.seasonLE1, 0, 1, 1, 1)

        comboBox_arr = []
        for i in range(1, 25):
            comboBox_arr.append(str(i) + " (교시)")

        self.comboBox = QComboBox(self.gridLayoutWidget)
        for i in range(len(comboBox_arr)):
            self.comboBox.addItem(str(i))
            self.comboBox.setItemText(i, comboBox_arr[i])
        self.gridLayout.addWidget(self.comboBox, 1, 1, 1, 1)

        self.timeEdit1 = QTimeEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.timeEdit1, 2, 1, 1, 1)

        self.seasonLE2 = QLineEdit(self.gridLayoutWidget)
        self.seasonLE2.setReadOnly(True)
        self.seasonLE2.setStyleSheet("background: lightgray")
        self.seasonLE2.setText(selected_info[1])
        self.gridLayout.addWidget(self.seasonLE2, 0, 2, 1, 1)

        self.timeLE2 = QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.timeLE2, 1, 2, 1, 1)

        self.timeEdit2 = QTimeEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.timeEdit2, 2, 2, 1, 1)

        tool_button_arr = [["시간 추가", 440, 220, 30, 30, "img/add-file.png", 30, 30, self.addInfo],
                           ["시간 삭제", 480, 220, 30, 30, "img/delete.png", 30, 30, self.delInfo]]

        for i in range(len(tool_button_arr)):
            self.toolButton = QToolButton(self)
            global_funtion().tool_button_setting(self.toolButton, tool_button_arr[i])

        # TableWidget Layout & Header Title setting
        tableWidget_hdr_arr = ["시간 ID", "내용", "시작시간", "종료시간"]
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QRect(10, 250, 510, 330))
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 전체 cell read-only
        self.tableWidget.verticalHeader().setVisible(False)  # index 안보이는 기능
        self.tableWidget.setColumnCount(len(tableWidget_hdr_arr))
        self.tableWidget.setRowCount(0)
        self.tableWidget.cellClicked.connect(self.handleCellClicked)

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStyleSheet("::section {""background-color: lightgray;""}")  # TableWidget내 헤더 Title의 배경색은 일반적으로 달리 이렇게 지정함
        for i in range(len(tableWidget_hdr_arr)):
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setHorizontalHeaderItem(i, item)
            item = self.tableWidget.horizontalHeaderItem(i)
            item.setText(tableWidget_hdr_arr[i])

        self.buttonBox = QDialogButtonBox(self)
        global_funtion().final_decision_button_box(self.buttonBox, 150, 600, 340, 30, "저장", "취소", self.accept, self.reject)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QCoreApplication.translate

        self.tableWidget.clearContents()
        for i in range(len(tabWidget_time_info_arr)):
            self.tableWidget.removeRow(i)
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            for j in range(len(tabWidget_time_info_arr[i])):
                if j == 5: break
                if j == 0: continue
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(i, j-1, item)
                item = self.tableWidget.item(i, j-1)
                if j == 1:
                    item.setBackground(QColor("lightgreen"))
                    item.setText(str(tabWidget_time_info_arr[i][j]) + " (교시)")
                else:
                    item.setText(tabWidget_time_info_arr[i][j])

    def handleCellClicked(self, row):
        global time_info
        clicked_cell = self.tableWidget.item(row, 0).text()

        # tablewidget에서 Clicked row의 시간 ID를 가지고 'tabWidget_time_info_arr'의 특정 Record를 읽어옴
        for i in range(len(tabWidget_time_info_arr)):
            if tabWidget_time_info_arr[i][1] == int(clicked_cell.split()[0]): #item.text는 str 속성이기 때문에 int type으로 변환해야 함
               time_info = tabWidget_time_info_arr[i]
               break

    def addInfo(self):
        add_target_arr = [self.seasonLE1.text(), int(self.comboBox.currentText().split()[0]), self.timeLE2.text(),
                          self.timeEdit1.text(), self.timeEdit2.text(), "x", "", "", ""]


        error_no = 0
        if add_target_arr[2].replace(" ","") == "":               #입력 필드내의 모든 공백 값 제거
            error_no = 1
        elif self.timeEdit1.time() >= self.timeEdit2.time():
            error_no = 2
        else:
            for i in range(len(tabWidget_time_info_arr)):
                if tabWidget_time_info_arr[i][1] == add_target_arr[1]:
                    error_no = 3
                elif tabWidget_time_info_arr[i][3] <= add_target_arr[3] and tabWidget_time_info_arr[i][4] >= add_target_arr[3]:
                    error_no = 4
                elif tabWidget_time_info_arr[i][3] <= add_target_arr[4] and tabWidget_time_info_arr[i][4] >= add_target_arr[4]:
                    error_no = 5
                if error_no != 0:
                    break

        if error_no != 0:
            MsgTxt = { 1: "시간 ID에 대한 내용 누락", 2: "종료시간이 시작시간 보다 같거나 빠를 수 없음",
                       3: "이미 등록된 시간 ID가 존재", 4: "시작시간이 겹치는 시간대가 존재", 5:"종료시간이 겹치는 시간대가 존재" }
            global_funtion().message_box_1(QMessageBox.Critical, "오류", MsgTxt[error_no], "확인")
            return

        tabWidget_time_info_arr.append(add_target_arr)
        list.sort(tabWidget_time_info_arr, key=lambda k: (k[0], k[1]))

        self.retranslateUi()

    def delInfo(self):
        try:
            time_info
        except NameError:
            global_funtion().message_box_1(QMessageBox.Warning, "경고", "삭제할 행을 선택하시오", "확인")
            pass
        else:
            if time_info[1]  in range(1, 24):
                for i in range(len(tabWidget_time_info_arr)):
                    if tabWidget_time_info_arr[i][1] == time_info[1]:
                        tabWidget_time_info_arr.__delitem__(i)
                        self.tableWidget.removeRow(i)
                        break

            self.retranslateUi()

    def accept(self):
        global_funtion().message_box_2(QMessageBox.Question, "확인", "작성내용을 저장하시겠습니까?", "예", "아니오")
        if MsgBoxRtnSignal == 'Y':
            target_updated_record = 0                   #TableWidget내 생성/변경 정보가 있는 지 점검하기 위한 인자
            for i in range(len(tabWidget_time_info_arr)):
                if tabWidget_time_info_arr[i][5] == "x":      #생성일
                   tabWidget_time_info_arr[i][5] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                   tabWidget_time_info_arr[i][6] = "admin"   #생성인
                   target_updated_record += 1
                else:
                   if tabWidget_time_info_arr[i][7] == "x":      #변경일
                      tabWidget_time_info_arr[i][7] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                      tabWidget_time_info_arr[i][8] = "admin"   #변경인
                      target_updated_record += 1

            if target_updated_record == 0 and length_of_df_list == len(tabWidget_time_info_arr):
               global_funtion().message_box_1(QMessageBox.Warning, "경고", "변경된 정보가 없습니다", "확인")
               return

            # 최초 excel file에서 추출한 list를 다시 excel file로 저장하기 위해 현재 화면에 출력된 기존/생성/수정/변경된 정보를
            # 갱신하기 위해 화면에 출력된 기존 list 정보값을 모두 지우고 다시 화면 리스트 정보를 Append하여 excel file에 저장한 대상을 정비함
            del_idx_arr = []                       # numpy array 기능을 이용하기 위해 지울 대상의 Index를 수집할 목적
            for i in range(len(df_time_period_list)):
               if df_time_period_list[i][0] == master_ID:
                  del_idx_arr.append(i)

            np_type_arr = np.array(df_time_period_list)   # 일반 배열을 numpy array 유형으로 전환하면 각 요소를 구분하는 Comma(,)가 제거된 상태가 됨
            np_type_arr = np.delete(np_type_arr, del_idx_arr, axis = 0)     # axis = 0 (Row), 1(Column)
            normal_arr = np_type_arr.tolist()

            df_time_period_list.clear()
            for i in range(len(normal_arr)):
                normal_arr[i][1] = int(normal_arr[i][1])
                df_time_period_list.append(normal_arr[i])

            for i in range(len(tabWidget_time_info_arr)):
                df_time_period_list.append(tabWidget_time_info_arr[i])

            list.sort(df_time_period_list, key=lambda k: (k[0], k[1]))

            df = pd.DataFrame(df_time_period_list, columns=df_time_col)
            df.to_excel('table/AA_time_period.xlsx', index=False)
            global_funtion().message_box_1(QMessageBox.Information, "정보", "저장되었습니다", "확인")

            self.close()
            # Ui_Master_Mgmt().exec_()
        else: pass

class Ui_Lesson_Schedule(QDialog):
    def __init__(self):
        super().__init__()
        self.get_Init_data()
        self.setupUi()

    def get_Init_data(self):
        global selected_ID, selected_name

        selected_ID = selected_info[0]
        selected_name = selected_info[1]

        global length_of_df_list
        length_of_df_list = len(tabWidget_less_schl_arr)

    def setupUi(self):
        self.setWindowTitle("강좌 일정관리")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setFixedSize(540, 665)

        self.label = QLabel(self)
        self.label.setGeometry(QRect(0, 15, 510, 40))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("강좌 일정 등록")
        global_funtion().fontSetting(self.label, '6B', 24, " ")  # "에스코어 드림 6 Bold", PointSize(24)

        self.gridLayoutWidget = QWidget(self)
        self.gridLayoutWidget.setGeometry(QRect(50, 80, 440, 160))

        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(20)

        title_arr = ["강      좌", "시간 유형", "강  의  실", "시      간" ]
        for i in range(len(title_arr)):
            self.label = QLabel(self.gridLayoutWidget)
            self.label.setText(title_arr[i])
            self.gridLayout.addWidget(self.label, i, 0, 1, 1)

        global fld1_arr, fld2_arr
        fld1_arr = [["self.lessonLE1", selected_ID]]
        for i in range(len(fld1_arr)):
            fld1_arr[i][0] = QLineEdit(self.gridLayoutWidget)
            fld1_arr[i][0].setText(fld1_arr[i][1])
            fld1_arr[i][0].setReadOnly(True)
            fld1_arr[i][0].setStyleSheet("background: lightgray")
            self.gridLayout.addWidget(fld1_arr[i][0], i, 1, 1, 1)

        self.groupBox = QGroupBox(self.gridLayoutWidget)
        self.groupBox.setMaximumSize(QSize(16777215, 30))
        global type_arr
        type_arr = [["self.button","개별", 20, 0, 50, 20], ["self.groupbutton","그룹", 100, 0, 50, 20]]

        for i in range(len(type_arr)):
            type_arr[i][0] = QRadioButton(self.groupBox)
            type_arr[i][0].setText(type_arr[i][1])
            type_arr[i][0].setGeometry(QRect(type_arr[i][2],type_arr[i][3], type_arr[i][4], type_arr[i][5]))
            if i == 0:  type_arr[i][0].setChecked(True)
            type_arr[i][0].clicked.connect(self.rb_check)
        self.gridLayout.addWidget(self.groupBox, 1, 1, 1, 1)

        fld2_arr = [["self.roomCB1", "BB"], ["self.periodCB1", "AA"]]
        for i in range(len(fld2_arr)):
            fld2_arr[i][0] = QComboBox(self.gridLayoutWidget)
            if fld2_arr[i][1] == "BB":
               for j in range(len(BB_master_list)):
                   fld2_arr[i][0].addItem("BB" + str(BB_master_list[j][1]))
                   fld2_arr[i][0].setItemText(j, "BB" + str(BB_master_list[j][1]) + ": " + BB_master_list[j][2])
            elif fld2_arr[i][1] == "AA":
                for j in range(len(time_period_arr)):
                    fld2_arr[i][0].addItem(str(time_period_arr[j][1]))
                    fld2_arr[i][0].setItemText(j, str(time_period_arr[j][1]) + " (교시): " + time_period_arr[j][2])
            self.gridLayout.addWidget(fld2_arr[i][0], i+2, 1, 1, 1)

        LE2_arr = [["self.lessonLE2", selected_name]]
        for i in range(len(LE2_arr)):
            LE2_arr[i][0] = QLineEdit(self.gridLayoutWidget)
            LE2_arr[i][0].setReadOnly(True)
            LE2_arr[i][0].setStyleSheet("background: lightgray")
            LE2_arr[i][0].setText(LE2_arr[i][1])
            self.gridLayout.addWidget(LE2_arr[i][0], i, 2, 1, 1)

        # global LE_type
        self.LE_type = QLineEdit(self.gridLayoutWidget)
        self.LE_type.setReadOnly(True)
        self.LE_type.setStyleSheet("background: lightgray")
        self.LE_type.setText(" ")
        self.gridLayout.addWidget(self.LE_type, 1, 2, 1, 1)

        self.horizontalLayoutWidget = QWidget(self)
        self.horizontalLayoutWidget.setGeometry(QRect(50, 245, 440, 50))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        global days_arr
        days_arr = [["self.CB_1", "월"], ["self.CB_2", "화"], ["self.CB_3", "수"],
                    ["self.CB_4", "목"], ["self.CB_5", "금"], ["self.CB_6", "토"],
                    ["self.CB_7", "일"]]
        for i in range(len(days_arr)):
            days_arr[i][0] = QCheckBox(self.horizontalLayoutWidget)
            days_arr[i][0].setText(days_arr[i][1])
            self.horizontalLayout.addWidget(days_arr[i][0])

        tool_button_arr = [["강좌 추가", 400, 290, 30, 30, "img/add-file.png", 30, 30, self.addInfo],
                           ["강좌 변경", 440, 290, 30, 30, "img/update.png", 30, 30, self.updateInfo],
                           ["강좌 삭제", 480, 290, 30, 30, "img/delete.png", 30, 30, self.delInfo]]
        for i in range(len(tool_button_arr)):
            self.toolButton = QToolButton(self)
            global_funtion().tool_button_setting(self.toolButton, tool_button_arr[i])

        tableWidget_hdr_arr = ["그룹", "강의실", "시간", "월", "화", "수", "목", "금", "토", "일"]
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QRect(10, 320, 510, 255))
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 전체 cell read-only
        self.tableWidget.verticalHeader().setVisible(False)  # index 안보이는 기능
        self.tableWidget.setColumnCount(len(tableWidget_hdr_arr))
        self.tableWidget.setRowCount(0)
        self.tableWidget.cellClicked.connect(self.handleCellClicked)
        self.tableWidget.cellDoubleClicked.connect(self.handleCellDoubleClicked)

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStyleSheet("::section {""background-color: lightgray;""}")  # TableWidget내 헤더 Title의 배경색은 일반적으로 달리 이렇게 지정함
        for i in range(len(tableWidget_hdr_arr)):
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setHorizontalHeaderItem(i, item)
            item = self.tableWidget.horizontalHeaderItem(i)
            item.setText(tableWidget_hdr_arr[i])

        self.buttonBox = QDialogButtonBox(self)
        global_funtion().final_decision_button_box(self.buttonBox, 150, 600, 340, 30, "저장", "취소",
                                                   self.accept, self.reject)
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QCoreApplication.translate

        old_group_key = ""
        x = 0
        self.tableWidget.clearContents()
        for i in range(len(tabWidget_less_schl_arr)):
            self.tableWidget.removeRow(i)
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            if tabWidget_less_schl_arr[i][0] != " ":
               if old_group_key != "" and  old_group_key != tabWidget_less_schl_arr[i][0]:
                  x += 1
            for j in range(len(tabWidget_less_schl_arr[i])):
                k = j
                if j == 3: continue
                if j == 11: break
                if j > 3 : k = j - 1
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(i, k, item)
                item = self.tableWidget.item(i, k)
                if k < 3 and tabWidget_less_schl_arr[i][0] != " ":
                   item.setBackground(QColor(bg_color_arr[x%5]))
                item.setText(tabWidget_less_schl_arr[i][j])

            old_group_key = tabWidget_less_schl_arr[i][0]

    def cleanContents(self):
        fld1_arr[0][0].setText(fld1_arr[0][1])
        type_arr[0][0].click()
        fld2_arr[0][0].setCurrentIndex(0)
        fld2_arr[1][0].setCurrentIndex(0)
        for i in range(len(days_arr)):
            days_arr[i][0].setChecked(False)


    def handleCellClicked(self, row):
        global less_schl_info
        less_schl_info = tabWidget_less_schl_arr[row]

    def handleCellDoubleClicked(self, row):
        less_schl_info = tabWidget_less_schl_arr[row]
        if less_schl_info[0] != " " and type_arr[1][0].isChecked() == True:  #그룹 키 존재, 라디오버튼 "그룹"지정
            self.LE_type.setText(less_schl_info[0])

    def rb_check(self):
        # option_arr = [[False, "background: white"], [True, "background: lightgray"]]
        # if self.radioButton.isChecked() == True: i = 0
        # else: i = 1
        #
        # LE_type.setReadOnly(option_arr[i][0])
        # LE_type.setStyleSheet(option_arr[i][1])
        # LE_type.setText("")
        if type_arr[1][0].isChecked() != True:
           self.LE_type.setText(" ")

    def addInfo(self):
        if type_arr[1][0].isChecked() == True:
           if self.LE_type.text() == " ":
               global_funtion().message_box_2(QMessageBox.Question, "확인", "신규그룹을 생성하시겠습니까?", "예", "아니오")
               if MsgBoxRtnSignal == 'Y':
                   text, ok = QInputDialog.getText(self, 'Input Dialog', '그룹 키:')
                   if ok:
                       for i in range(len(tabWidget_less_schl_arr)):
                           if tabWidget_less_schl_arr[i][0] == text:
                               global_funtion().message_box_1(QMessageBox.Information, "정보",
                                                              "동일한 그룹키가 존재합니다. 다시 지정해 주세요", "확인")
                               return
                       self.LE_type.setText(str(text))
                   else:
                       return
               else:
                   global_funtion().message_box_1(QMessageBox.Information, "정보", "아래 리스트에서 그룹키를 더블클릭하여 지정하시오!", "확인")
                   return
           else:
               if self.LE_type.text().encode().isalnum() == False:
                   global_funtion().message_box_1(QMessageBox.Critical, "오류", "공백이 없는 영숫자조합의 그룹키를 입력하시오", "확인")
                   return

        monday = " "
        if days_arr[0][0].checkState() != 0: monday = "X"
        tuesday = " "
        if days_arr[1][0].checkState() != 0: tuesday = "X"
        wednesday = " "
        if days_arr[2][0].checkState() != 0: wednesday = "X"
        thursday = " "
        if days_arr[3][0].checkState() != 0: thursday = "X"
        friday = " "
        if days_arr[4][0].checkState() != 0: friday = "X"
        saturday = " "
        if days_arr[5][0].checkState() != 0: saturday = "X"
        sunday = " "
        if days_arr[6][0].checkState() != 0: sunday = "X"

        day_ID = ""
        if   day_ID == "" and monday    == "X": day_ID = "A"
        elif day_ID == "" and tuesday   == "X": day_ID = "B"
        elif day_ID == "" and wednesday == "X": day_ID = "C"
        elif day_ID == "" and thursday  == "X": day_ID = "D"
        elif day_ID == "" and friday    == "X": day_ID = "E"
        elif day_ID == "" and saturday  == "X": day_ID = "F"
        elif day_ID == "" and sunday    == "X": day_ID = "G"

        add_target_arr = [self.LE_type.text(), fld2_arr[0][0].currentText(), fld2_arr[1][0].currentText(), day_ID,
                          monday, tuesday, wednesday, thursday, friday, saturday, sunday,"", "x", "", "", ""] #강의실,시간,요일,생성/변경이력

        if monday == " " and tuesday == " " and wednesday == " " and thursday == " " and friday == " " and \
           saturday == " " and sunday == " ":
           global_funtion().message_box_1(QMessageBox.Critical, "오류", "요일 미지정", "확인")
           return

        error_exist = ""
        for i in range(len(tabWidget_less_schl_arr)):
            if tabWidget_less_schl_arr[i][1] == add_target_arr[1] and tabWidget_less_schl_arr[i][2] == add_target_arr[2]:
                for j in range(4, 11):
                    if add_target_arr[j] == "X" and add_target_arr[j] == tabWidget_less_schl_arr[i][j]:
                        error_exist = "x"
                        break
                if error_exist == "x": break
        if error_exist != "":
            global_funtion().message_box_1(QMessageBox.Critical, "오류", "이미 등록된 강좌/시간 정보가 존재", "확인")
            return

        for i in range(len(df_lesson_schedule_list)):
            if df_lesson_schedule_list[i][0] == Selected_season_ID and \
               df_lesson_schedule_list[i][5] == add_target_arr[1].split(":")[0] and \
               df_lesson_schedule_list[i][6] == int(add_target_arr[2].split(" ")[0]):      #시즌, 강의실, 시간
               for j in range(4,11):
                  if add_target_arr[j] == "X" and add_target_arr[j] == df_lesson_schedule_list[i][j+3]:
                     error_exist = "x"
                     break
               if error_exist == "x": break

        if error_exist != "":
            global_funtion().message_box_1(QMessageBox.Critical, "오류", "이미 등록된 다른 강좌/시간 정보가 존재", "확인")
            return

        tabWidget_less_schl_arr.append(add_target_arr)
        list.sort(tabWidget_less_schl_arr, key=lambda k: (k[0], k[1], k[2], k[3]))

        self.cleanContents()
        self.retranslateUi()

    def updateInfo(self):
        try:
            less_schl_info
        except NameError:
            global_funtion().message_box_1(QMessageBox.Warning, "경고", "변경할 행을 선택하시오", "확인")
            pass
        else:
            print("해당 버젼에 제공하지 않음.")
            # self.close()
            # Ui_Lesson_Schedule_Update().exec_()

    def delInfo(self):
        try:
            less_schl_info
        except NameError:
            global_funtion().message_box_1(QMessageBox.Warning, "경고", "삭제할 행을 선택하시오", "확인")
            pass
        else:
            exist_err = "N"
            for i in range(len(df_teacher_lesson_list)):
                if df_teacher_lesson_list[i][0] != Selected_season_ID: continue  # 시즌 ID
                if df_teacher_lesson_list[i][3] != selected_ID: continue         # 강좌 ID
                if df_teacher_lesson_list[i][4] != less_schl_info[0]: continue   # 그룹 키
                if df_teacher_lesson_list[i][5] != less_schl_info[1].split(": ")[0]: continue  # 강의실 ID
                if df_teacher_lesson_list[i][6] != int(less_schl_info[2].split(" (")[0]): continue  # 시간 ID
                if df_teacher_lesson_list[i][7] != less_schl_info[3]: continue  # 요일 ID
                exist_err = "Y"
                break

            if exist_err == "Y":
                global_funtion().message_box_1(QMessageBox.Warning, "경고", "강사에 이미 등록되어 있어 삭제불가함", "확인")
                return

            for i in range(len(tabWidget_less_schl_arr)):
                if tabWidget_less_schl_arr[i][0] == less_schl_info[0] and \
                   tabWidget_less_schl_arr[i][1] == less_schl_info[1] and \
                   tabWidget_less_schl_arr[i][2] == less_schl_info[2] and \
                   tabWidget_less_schl_arr[i][3] == less_schl_info[3]:                  #강의실/시간/요일
                   tabWidget_less_schl_arr.__delitem__(i)
                   self.tableWidget.removeRow(i)
                   break
            self.retranslateUi()

    def accept(self):
        global_funtion().message_box_2(QMessageBox.Question, "확인", "작성내용을 저장하시겠습니까?", "예", "아니오")
        if MsgBoxRtnSignal == 'Y':
            target_updated_record = 0                   #TableWidget내 생성/변경 정보가 있는 지 점검하기 위한 인자
            temp_less_schl_list = []
            sub_key = 1
            for i in range(len(tabWidget_less_schl_arr)):
                temp_less_schl_arr = []
                temp_less_schl_arr.append(Selected_season_ID)                                #시즌 ID
                if tabWidget_less_schl_arr[i][0] == "" or tabWidget_less_schl_arr[i][0] == " ":
                    groupkey_text = "#"
                    lesson_key = fld1_arr[0][0].text() + groupkey_text + \
                                 tabWidget_less_schl_arr[i][1].split(":")[0] + tabWidget_less_schl_arr[i][2].split(" ")[
                                     0] + \
                                 tabWidget_less_schl_arr[i][3]
                    sub_key = 1
                else:
                    groupkey_text = str(tabWidget_less_schl_arr[i][0])
                    lesson_key = fld1_arr[0][0].text() + groupkey_text + tabWidget_less_schl_arr[i][1].split(":")[0]
                    if i != 0 and str(tabWidget_less_schl_arr[i][0]) == str(tabWidget_less_schl_arr[i-1][0]):
                        sub_key = sub_key + 1
                    elif i == 0 and groupkey_text != "#":
                        sub_key = 1

                temp_less_schl_arr.append(lesson_key)
                temp_less_schl_arr.append(str(sub_key))
                temp_less_schl_arr.append(fld1_arr[0][0].text())                             #강좌 ID
                temp_less_schl_arr.append(tabWidget_less_schl_arr[i][0])                     #그룹 Key
                temp_less_schl_arr.append(tabWidget_less_schl_arr[i][1].split(":")[0])       #강의실 ID
                temp_less_schl_arr.append(int(tabWidget_less_schl_arr[i][2].split(" ")[0]))  #시간 ID
                if tabWidget_less_schl_arr[i][12] == "x":      #생성일
                   tabWidget_less_schl_arr[i][12] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                   tabWidget_less_schl_arr[i][13] = "admin"   #생성인
                   target_updated_record += 1
                else:
                   if tabWidget_less_schl_arr[i][14] == "x":      #변경일
                      tabWidget_less_schl_arr[i][14] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                      tabWidget_less_schl_arr[i][15] = "admin"   #변경인
                      target_updated_record += 1
                for j in range(len(tabWidget_less_schl_arr[i])):
                    if j < 3: continue
                    temp_less_schl_arr.append(tabWidget_less_schl_arr[i][j])

                temp_less_schl_list.append(temp_less_schl_arr)
            if target_updated_record == 0 and length_of_df_list == len(tabWidget_less_schl_arr):
               global_funtion().message_box_1(QMessageBox.Warning, "경고", "변경된 정보가 없습니다", "확인")
               return

            # 최초 excel file에서 추출한 list를 다시 excel file로 저장하기 위해 현재 화면에 출력된 기존/생성/수정/변경된 정보를
            # 갱신하기 위해 화면에 출력된 기존 list 정보값을 모두 지우고 다시 화면 리스트 정보를 Append하여 excel file에 저장한 대상을 정비함
            del_idx_arr = []                       # numpy array 기능을 이용하기 위해 지울 대상의 Index를 수집할 목적
            for i in range(len(df_lesson_schedule_list)):
               if df_lesson_schedule_list[i][0] == Selected_season_ID and df_lesson_schedule_list[i][3] == selected_ID:
                  del_idx_arr.append(i)

            np_type_arr = np.array(df_lesson_schedule_list)   #일반 배열을 numpy array 유형으로 전환하면 각 요소를 구분하는 Comma(,)가 제거된 상태가 됨
            np_type_arr = np.delete(np_type_arr, del_idx_arr, axis = 0)     # axis = 0 (Row), 1(Column)
            normal_arr = np_type_arr.tolist()

            df_lesson_schedule_list.clear()

            for i in range(len(normal_arr)):
                normal_arr[i][6] = int(normal_arr[i][6])      #numpy array 상태의 각 요소들은 변수 Type이 동일하게 적용되므로 특정 원소들은 원래 Type으로 변환필요
                df_lesson_schedule_list.append(normal_arr[i])

            for i in range(len(temp_less_schl_list)):
                df_lesson_schedule_list.append(temp_less_schl_list[i])

            list.sort(df_lesson_schedule_list, key=lambda k: (k[0], k[3], k[4], k[5], k[6], k[7]))
            df = pd.DataFrame(df_lesson_schedule_list, columns=df_lesson_schedule_col)
            df.to_excel('table/CC_lesson_schedule.xlsx', index=False)
            global_funtion().message_box_1(QMessageBox.Information, "정보", "저장되었습니다", "확인")

            # Ui_Lesson_Master_Mgmt().close()
            self.close()
            # Ui_Lesson_Master_Mgmt().exec_()
            # Ui_Master_Mgmt().exec_()
        else: pass

class Ui_Lesson_Schedule_Update(QDialog):
    def __init__(self):
        super().__init__()
        self.get_Init_data()
        self.setupUi()

    def get_Init_data(self):
        global selected_ID, selected_name, less_arr

        selected_ID = selected_info[0]
        selected_name = selected_info[1]

        less_arr = []
        less_arr.append(less_schl_info)

        global length_of_df_list
        length_of_df_list = len(tabWidget_less_schl_arr)

    def setupUi(self):
        self.setWindowTitle("강좌 일정 변경")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setFixedSize(540, 665)

        self.label = QLabel(self)
        self.label.setGeometry(QRect(0, 15, 510, 40))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("강좌 일정 변경")
        global_funtion().fontSetting(self.label, '6B', 24, " ")  # "에스코어 드림 6 Bold", PointSize(24)

        self.gridLayoutWidget = QWidget(self)
        self.gridLayoutWidget.setGeometry(QRect(50, 80, 440, 160))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")

        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setObjectName("gridLayout")

        title_arr = ["강      좌", "시간 유형", "강  의  실", "시      간" ]
        for i in range(len(title_arr)):
            self.label = QLabel(self.gridLayoutWidget)
            self.label.setText(title_arr[i])
            self.gridLayout.addWidget(self.label, i, 0, 1, 1)

        global fld1_arr, fld2_arr
        fld1_arr = [["self.lessonLE1", selected_ID]]
        for i in range(len(fld1_arr)):
            fld1_arr[i][0] = QLineEdit(self.gridLayoutWidget)
            fld1_arr[i][0].setText(fld1_arr[i][1])
            fld1_arr[i][0].setReadOnly(True)
            fld1_arr[i][0].setStyleSheet("background: lightgray")
            self.gridLayout.addWidget(fld1_arr[i][0], i, 1, 1, 1)

        self.groupBox = QGroupBox(self.gridLayoutWidget)
        self.groupBox.setMaximumSize(QSize(16777215, 30))

        global type_arr
        type_arr = [["self.button", "개별", 20, 0, 50, 20], ["self.groupbutton", "그룹", 100, 0, 50, 20]]

        for i in range(len(type_arr)):
            type_arr[i][0] = QRadioButton(self.groupBox)
            type_arr[i][0].setText(type_arr[i][1])
            type_arr[i][0].setGeometry(QRect(type_arr[i][2], type_arr[i][3], type_arr[i][4], type_arr[i][5]))
            type_arr[i][0].setEnabled(False)
        self.gridLayout.addWidget(self.groupBox, 1, 1, 1, 1)

        fld2_arr = [["self.roomCB1", "BB"], ["self.periodCB1", "AA"]]
        for i in range(len(fld2_arr)):
            fld2_arr[i][0] = QComboBox(self.gridLayoutWidget)
            if fld2_arr[i][1] == "BB":
               for j in range(len(BB_master_list)):
                   fld2_arr[i][0].addItem("BB" + str(BB_master_list[j][1]))
                   fld2_arr[i][0].setItemText(j, "BB" + str(BB_master_list[j][1]) + ": " + BB_master_list[j][2])
            elif fld2_arr[i][1] == "AA":
                for j in range(len(time_period_arr)):
                    fld2_arr[i][0].addItem(str(time_period_arr[j][1]))
                    fld2_arr[i][0].setItemText(j, str(time_period_arr[j][1]) + " (교시): " + time_period_arr[j][2])
            self.gridLayout.addWidget(fld2_arr[i][0], i+2, 1, 1, 1)

        LE2_arr = [["self.lessonLE2", selected_name]]
        for i in range(len(LE2_arr)):
            LE2_arr[i][0] = QLineEdit(self.gridLayoutWidget)
            LE2_arr[i][0].setReadOnly(True)
            LE2_arr[i][0].setStyleSheet("background: lightgray")
            LE2_arr[i][0].setText(LE2_arr[i][1])
            self.gridLayout.addWidget(LE2_arr[i][0], i, 2, 1, 1)

        # global LE_type
        self.LE_type = QLineEdit(self.gridLayoutWidget)
        self.LE_type.setReadOnly(True)
        self.LE_type.setStyleSheet("background: lightgray")
        self.LE_type.setText(" ")
        self.gridLayout.addWidget(self.LE_type, 1, 2, 1, 1)

        if less_schl_info[0] == " ":
            type_arr[0][0].setChecked(True)
        else:
            type_arr[1][0].setChecked(True)
            self.LE_type.setText(less_schl_info[0])
        class_index = fld2_arr[0][0].findText(less_schl_info[1])
        fld2_arr[0][0].setCurrentIndex(class_index)
        time_index = fld2_arr[1][0].findText(less_schl_info[2])
        fld2_arr[1][0].setCurrentIndex(time_index)

        self.horizontalLayoutWidget = QWidget(self)
        self.horizontalLayoutWidget.setGeometry(QRect(50, 245, 440, 50))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        global days_arr
        days_arr = [["self.CB_1", "월"], ["self.CB_2", "화"], ["self.CB_3", "수"],
                    ["self.CB_4", "목"], ["self.CB_5", "금"], ["self.CB_6", "토"],
                    ["self.CB_7", "일"]]
        for i in range(len(days_arr)):
            days_arr[i][0] = QCheckBox(self.horizontalLayoutWidget)
            days_arr[i][0].setText(days_arr[i][1])
            self.horizontalLayout.addWidget(days_arr[i][0])
            if less_schl_info[i+4] == "X":
                days_arr[i][0].setChecked(True)

        tool_button_arr = [["강좌 추가", 400, 290, 30, 30, "img/add-file.png", 30, 30, self.addInfo],
                           ["강좌 삭제", 480, 290, 30, 30, "img/delete.png", 30, 30, self.delInfo]]
        for i in range(len(tool_button_arr)):
            self.toolButton = QToolButton(self)
            global_funtion().tool_button_setting(self.toolButton, tool_button_arr[i])

        tableWidget_hdr_arr = ["그룹", "강의실", "시간", "월", "화", "수", "목", "금", "토", "일"]
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QRect(10, 320, 510, 255))
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 전체 cell read-only
        self.tableWidget.verticalHeader().setVisible(False)  # index 안보이는 기능
        self.tableWidget.setColumnCount(len(tableWidget_hdr_arr))
        self.tableWidget.setRowCount(0)
        self.tableWidget.cellClicked.connect(self.handleCellClicked)

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStyleSheet("::section {""background-color: lightgray;""}")  # TableWidget내 헤더 Title의 배경색은 일반적으로 달리 이렇게 지정함
        for i in range(len(tableWidget_hdr_arr)):
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setHorizontalHeaderItem(i, item)
            item = self.tableWidget.horizontalHeaderItem(i)
            item.setText(tableWidget_hdr_arr[i])

        self.buttonBox = QDialogButtonBox(self)
        global_funtion().final_decision_button_box(self.buttonBox, 150, 600, 340, 30, "저장", "취소",
                                                   self.accept, self.reject)
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QCoreApplication.translate

        old_group_key = ""
        x = 0
        self.tableWidget.clearContents()
        for i in range(len(less_arr)):
            self.tableWidget.removeRow(i)
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)

            if less_arr[i][0] != " ":
               if old_group_key != "" and  old_group_key != less_schl_info[i][0]:
                  x += 1
            for j in range(len(less_arr[i])):
                k = j
                if j == 3: continue
                if j == 11: break
                if j > 3 : k = j - 1
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(i, k, item)
                item = self.tableWidget.item(i, k)
                if k < 3 and i != 0 and len(less_arr) == 2:
                   item.setBackground(QColor(bg_color_arr[x%5]))
                item.setText(less_arr[i][j])

            old_group_key = less_arr[i][0]

    def handleCellClicked(self, row):
        global less_schl_info_row
        less_schl_info_row = less_schl_info[row]

    def addInfo(self):
        if len(less_arr) >= 2:
            global_funtion().message_box_1(QMessageBox.Critical, "오류", "변경한 내용을 삭제하시고 다시 변경을 진행해주세요.", "확인")
            return
        if type_arr[1][0].isChecked() == True:
           if self.LE_type.text() == " ":
               global_funtion().message_box_2(QMessageBox.Question, "확인", "신규그룹을 생성하시겠습니까?", "예", "아니오")
               if MsgBoxRtnSignal == 'Y':
                   text, ok = QInputDialog.getText(self, 'Input Dialog', '그룹 키:')
                   if ok:
                       self.LE_type.setText(str(text))
                   else:
                       return
               else:
                   global_funtion().message_box_1(QMessageBox.Information, "정보", "아래 리스트에서 그룹키를 더블클릭하여 지정하시오!", "확인")
                   return
           else:
               if self.LE_type.text().encode().isalnum() == False:
                   global_funtion().message_box_1(QMessageBox.Critical, "오류", "공백이 없는 영숫자조합의 그룹키를 입력하시오", "확인")
                   return

        monday = " "
        if days_arr[0][0].checkState() != 0: monday = "X"
        tuesday = " "
        if days_arr[1][0].checkState() != 0: tuesday = "X"
        wednesday = " "
        if days_arr[2][0].checkState() != 0: wednesday = "X"
        thursday = " "
        if days_arr[3][0].checkState() != 0: thursday = "X"
        friday = " "
        if days_arr[4][0].checkState() != 0: friday = "X"
        saturday = " "
        if days_arr[5][0].checkState() != 0: saturday = "X"
        sunday = " "
        if days_arr[6][0].checkState() != 0: sunday = "X"

        day_ID = ""
        if   day_ID == "" and monday    == "X": day_ID = "A"
        elif day_ID == "" and tuesday   == "X": day_ID = "B"
        elif day_ID == "" and wednesday == "X": day_ID = "C"
        elif day_ID == "" and thursday  == "X": day_ID = "D"
        elif day_ID == "" and friday    == "X": day_ID = "E"
        elif day_ID == "" and saturday  == "X": day_ID = "F"
        elif day_ID == "" and sunday    == "X": day_ID = "G"

        add_target_arr = [self.LE_type.text(), fld2_arr[0][0].currentText(), fld2_arr[1][0].currentText(), day_ID,
                          monday, tuesday, wednesday, thursday, friday, saturday, sunday,"", "x", "", "", ""] #강의실,시간,요일,변경key,생성/변경이력

        if monday == " " and tuesday == " " and wednesday == " " and thursday == " " and friday == " " and \
           saturday == " " and sunday == " ":
           global_funtion().message_box_1(QMessageBox.Critical, "오류", "요일 미지정", "확인")
           return

        error_exist = ""
        for i in range(len(tabWidget_less_schl_arr)):
            if tabWidget_less_schl_arr[i][1] == add_target_arr[1] and tabWidget_less_schl_arr[i][2] == add_target_arr[2]:
                for j in range(4, 11):
                    if add_target_arr[j] == "X" and add_target_arr[j] == tabWidget_less_schl_arr[i][j]:
                        error_exist = "x"
                        break
                if error_exist == "x": break
        if error_exist != "":
            global_funtion().message_box_1(QMessageBox.Critical, "오류", "이미 등록된 강좌/시간 정보가 존재", "확인")
            return

        for i in range(len(df_lesson_schedule_list)):
            if df_lesson_schedule_list[i][0] == Selected_season_ID and \
               df_lesson_schedule_list[i][5] == add_target_arr[1].split(":")[0] and \
               df_lesson_schedule_list[i][6] == int(add_target_arr[2].split(" ")[0]):      #시즌, 강의실, 시간
               for j in range(4,11):
                  if add_target_arr[j] == "X" and add_target_arr[j] == df_lesson_schedule_list[i][j+3]:
                     error_exist = "x"
                     break
               if error_exist == "x": break

        if error_exist != "":
            global_funtion().message_box_1(QMessageBox.Critical, "오류", "이미 등록된 다른 강좌/시간 정보가 존재", "확인")
            return

        less_arr.append(add_target_arr)

        self.retranslateUi()

    def delInfo(self):
        try:
            less_schl_info_row
        except NameError:
            global_funtion().message_box_1(QMessageBox.Warning, "경고", "삭제할 행을 선택하시오", "확인")
            pass
        else:
            exist_err = "N"
            for i in range(len(df_teacher_lesson_list)):
                if df_teacher_lesson_list[i][0] != Selected_season_ID: continue  # 시즌 ID
                if df_teacher_lesson_list[i][3] != selected_ID: continue         # 강좌 ID
                if df_teacher_lesson_list[i][4] != less_schl_info_row[0]: continue   # 그룹 키
                if df_teacher_lesson_list[i][5] != less_schl_info_row[1].split(": ")[0]: continue  # 강의실 ID
                if df_teacher_lesson_list[i][6] != int(less_schl_info_row[2].split(" (")[0]): continue  # 시간 ID
                if df_teacher_lesson_list[i][7] != less_schl_info_row[3]: continue  # 요일 ID
                exist_err = "Y"
                break

            if exist_err == "Y":
                global_funtion().message_box_1(QMessageBox.Warning, "경고", "강사에 이미 등록되어 있어 삭제불가함", "확인")
                return

            for i in range(len(less_schl_info)):
                if less_arr[i][0] == less_schl_info_row[0] and \
                   less_arr[i][1] == less_schl_info_row[1] and \
                   less_arr[i][2] == less_schl_info_row[2] and \
                   less_arr[i][3] == less_schl_info_row[3]:                  #강의실/시간/요일
                   less_arr.__delitem__(i)
                   self.tableWidget.removeRow(i)
                   break
            self.retranslateUi()

    def accept(self):
        global_funtion().message_box_2(QMessageBox.Question, "확인", "변경하시겠습니까?", "예", "아니오")
        if MsgBoxRtnSignal == 'Y':
            target_updated_record = 0                   #TableWidget내 생성/변경 정보가 있는 지 점검하기 위한 인자
            temp_less_schl_list = []
            sub_key = 1
            for i in range(len(less_arr)):
                temp_less_schl_arr = []
                temp_less_schl_arr.append(Selected_season_ID)                                #시즌 ID
                if less_arr[i][0] == "" or less_arr[i][0] == " ":
                    groupkey_text = "#"
                    lesson_key = fld1_arr[0][0].text() + groupkey_text + \
                                 less_arr[i][1].split(":")[0] + less_arr[i][2].split(" ")[
                                     0] + \
                                 less_arr[i][3]
                    sub_key = 1
                else:
                    groupkey_text = str(less_arr[i][0])
                    lesson_key = fld1_arr[0][0].text() + groupkey_text + less_arr[i][1].split(":")[0]
                    if i != 0 and str(less_arr[i][0]) == str(less_arr[i-1][0]):
                        sub_key = sub_key + 1
                    elif i == 0 and groupkey_text != "#":
                        sub_key = 1

                temp_less_schl_arr.append(lesson_key)
                temp_less_schl_arr.append(str(sub_key))
                temp_less_schl_arr.append(fld1_arr[0][0].text())                             #강좌 ID
                temp_less_schl_arr.append(less_arr[i][0])                     #그룹 Key
                temp_less_schl_arr.append(less_arr[i][1].split(":")[0])       #강의실 ID
                temp_less_schl_arr.append(int(less_arr[i][2].split(" ")[0]))  #시간 ID
                if tabWidget_less_schl_arr[i][12] == "x":      #생성일
                   less_arr[i][12] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                   less_arr[i][13] = "admin"   #생성인
                   target_updated_record += 1
                else:
                   if less_arr[i][14] == "x":      #변경일
                      less_arr[i][14] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                      less_arr[i][15] = "admin"   #변경인
                      target_updated_record += 1
                for j in range(len(tabWidget_less_schl_arr[i])):
                    if j < 3: continue
                    temp_less_schl_arr.append(tabWidget_less_schl_arr[i][j])

                temp_less_schl_list.append(temp_less_schl_arr)
            if target_updated_record == 0 and length_of_df_list == len(tabWidget_less_schl_arr):
               global_funtion().message_box_1(QMessageBox.Warning, "경고", "변경된 정보가 없습니다", "확인")
               return

            # 최초 excel file에서 추출한 list를 다시 excel file로 저장하기 위해 현재 화면에 출력된 기존/생성/수정/변경된 정보를
            # 갱신하기 위해 화면에 출력된 기존 list 정보값을 모두 지우고 다시 화면 리스트 정보를 Append하여 excel file에 저장한 대상을 정비함
            del_idx_arr = []                       # numpy array 기능을 이용하기 위해 지울 대상의 Index를 수집할 목적
            for i in range(len(df_lesson_schedule_list)):
               if df_lesson_schedule_list[i][0] == Selected_season_ID and df_lesson_schedule_list[i][3] == selected_ID:
                  del_idx_arr.append(i)

            np_type_arr = np.array(df_lesson_schedule_list)   #일반 배열을 numpy array 유형으로 전환하면 각 요소를 구분하는 Comma(,)가 제거된 상태가 됨
            np_type_arr = np.delete(np_type_arr, del_idx_arr, axis = 0)     # axis = 0 (Row), 1(Column)
            normal_arr = np_type_arr.tolist()

            df_lesson_schedule_list.clear()

            for i in range(len(normal_arr)):
                normal_arr[i][6] = int(normal_arr[i][6])      #numpy array 상태의 각 요소들은 변수 Type이 동일하게 적용되므로 특정 원소들은 원래 Type으로 변환필요
                df_lesson_schedule_list.append(normal_arr[i])

            for i in range(len(temp_less_schl_list)):
                df_lesson_schedule_list.append(temp_less_schl_list[i])

            list.sort(df_lesson_schedule_list, key=lambda k: (k[0], k[3], k[4], k[5], k[6], k[7]))
            df = pd.DataFrame(df_lesson_schedule_list, columns=df_lesson_schedule_col)
            df.to_excel('table/CC_lesson_schedule.xlsx', index=False)
            global_funtion().message_box_1(QMessageBox.Information, "정보", "저장되었습니다", "확인")

            self.close()
            Ui_Lesson_Schedule().exec_()
        else: pass

class Ui_Teacher_Lesson_Assign(QDialog):
    def __init__(self):
        super().__init__()
        self.get_Init_data()
        self.setupUi()

    def get_Init_data(self):
        global days_arr, selected_ID, selected_name, lesson_arr

        selected_ID = selected_info[0]
        selected_name = selected_info[1]
        lesson_arr = []
        for i in range(len(CC_master_list)):
            if CC_master_list[i][11] != "x": continue
            lesson_arr.append(CC_master_list[i][0] + str(CC_master_list[i][1]) + ": " + CC_master_list[i][2])

        self.detail_list_by_lesson(9999)

        global length_of_tabWidget
        length_of_tabWidget = len(tabWidget_teach_less_arr)

    def setupUi(self):
        self.setWindowTitle("강사/강좌 관리")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setFixedSize(540, 665)

        self.label = QLabel(self)
        self.label.setGeometry(QRect(0, 15, 510, 40))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("강사/강좌 등록")
        global_funtion().fontSetting(self.label, '6B', 24, " ")  # "에스코어 드림 6 Bold", PointSize(24)

        self.gridLayoutWidget = QWidget(self)
        self.gridLayoutWidget.setGeometry(QRect(50, 80, 440, 100))

        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(20)

        title_arr = ["강      사", "기      간" ]
        for i in range(len(title_arr)):
            self.label = QLabel(self.gridLayoutWidget)
            self.label.setText(title_arr[i])
            self.gridLayout.addWidget(self.label, i, 0, 1, 1)

        global fld1_arr, fld2_arr, fld3_arr
        fld1_arr = [["self.teacherLE1", selected_ID], ["self.prdStrQDt", ""]]
        for i in range(len(fld1_arr)):
            if i != 1:
                fld1_arr[i][0] = QLineEdit(self.gridLayoutWidget)
                fld1_arr[i][0].setText(fld1_arr[i][1])
                fld1_arr[i][0].setReadOnly(True)
                fld1_arr[i][0].setStyleSheet("background: lightgray")
            else:
                fld1_arr[i][0] = QDateEdit(self.gridLayoutWidget)
                fld1_arr[i][0].setDate(QDate.fromString(CC_master_list[0][5], 'yyyy-MM-dd'))
                fld1_arr[i][0].setCalendarPopup(True)
            self.gridLayout.addWidget(fld1_arr[i][0], i, 1, 1, 1)

        fld2_arr = [["self.teacherLE2", selected_name], ["self.prdEndQDt", ""]]
        for i in range(len(fld2_arr)):
            if i != 1:
                fld2_arr[i][0] = QLineEdit(self.gridLayoutWidget)
                fld2_arr[i][0].setReadOnly(True)
                if fld2_arr[i][1] != "":
                   fld2_arr[i][0].setText(fld2_arr[i][1])
                fld2_arr[i][0].setStyleSheet("background: lightgray")
            else:
                fld2_arr[i][0] = QDateEdit(self.gridLayoutWidget)
                fld2_arr[i][0].setDate(QDate.fromString(CC_master_list[0][6], 'yyyy-MM-dd'))
                fld2_arr[i][0].setCalendarPopup(True)
            self.gridLayout.addWidget(fld2_arr[i][0], i, 2, 1, 1)

        self.formLayoutWidget = QWidget(self)
        self.formLayoutWidget.setGeometry(QRect(50, 190, 440, 140))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setHorizontalSpacing(20)
        self.formLayout.setVerticalSpacing(20)

        fld3_arr = [["강      좌", "self.comboBox_lesson", lesson_arr],
                    ["상      세", "self.comboBox_detail", detail_combo_arr]]
        for i in range(len(fld3_arr)):
            self.label = QLabel(self.formLayoutWidget)
            self.label.setText(fld3_arr[i][0])
            self.formLayout.setWidget(i, QFormLayout.LabelRole, self.label)

            fld3_arr[i][1] = QComboBox(self.formLayoutWidget)
            fld3_arr[i][1].addItems(fld3_arr[i][2])
            if i == 0:
               fld3_arr[i][1].currentIndexChanged[int].connect(self.detail_list_by_lesson)
            self.formLayout.setWidget(i, QFormLayout.FieldRole, fld3_arr[i][1])

        tool_button_arr = [["강좌 추가", 440, 290, 30, 30, "img/add-file.png", 30, 30, self.addInfo],
                           ["강좌 삭제", 480, 290, 30, 30, "img/delete.png", 30, 30, self.delInfo]]
        for i in range(len(tool_button_arr)):
            self.toolButton = QToolButton(self)
            global_funtion().tool_button_setting(self.toolButton, tool_button_arr[i])

        tableWidget_hdr_arr = ["강좌", "강의실", "시간", "요일", "시작일", "종료일"]
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QRect(10, 320, 510, 255))
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 전체 cell read-only
        self.tableWidget.verticalHeader().setVisible(False)  # index 안보이는 기능
        self.tableWidget.setColumnCount(len(tableWidget_hdr_arr))
        self.tableWidget.setRowCount(0)
        self.tableWidget.cellClicked.connect(self.handleCellClicked)

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStyleSheet("::section {""background-color: lightgray;""}")  # TableWidget내 헤더 Title의 배경색은 일반적으로 달리 이렇게 지정함
        for i in range(len(tableWidget_hdr_arr)):
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setHorizontalHeaderItem(i, item)
            item = self.tableWidget.horizontalHeaderItem(i)
            item.setText(tableWidget_hdr_arr[i])

        self.buttonBox = QDialogButtonBox(self)
        global_funtion().final_decision_button_box(self.buttonBox, 150, 600, 340, 30, "저장", "취소",
                                                   self.accept, self.reject)
        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate

        old_group_key = ""
        x = 0
        self.tableWidget.clearContents()
        for i in range(len(tabWidget_teach_less_arr)):
            self.tableWidget.removeRow(i)
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            if tabWidget_teach_less_arr[i][11] != " ":
                if old_group_key != "" and old_group_key != tabWidget_teach_less_arr[i][11]: x += 1
            for j in range(len(tabWidget_teach_less_arr[i])):
                k = j
                if j >= 4: k = j - 1
                if j == 3: continue
                if j == 7: break
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(i, k, item)
                item = self.tableWidget.item(i, k)
                if j <= 4 and tabWidget_teach_less_arr[i][11] != " ":
                    item.setBackground(QColor(bg_color_arr[x%5]))
                if j == 0:
                    item.setText(tabWidget_teach_less_arr[i][j].split(": ")[1])
                else:
                    item.setText(tabWidget_teach_less_arr[i][j])
            old_group_key = tabWidget_teach_less_arr[i][11]

    def handleCellClicked(self, row):
        global teach_less_info, selected_row_idx
        selected_row_idx = row
        teach_less_info = tabWidget_teach_less_arr[selected_row_idx]
        # clicked_cell_0 = self.tableWidget.item(row, 0).text()    #강좌
        # clicked_cell_1 = self.tableWidget.item(row, 1).text()    #강의실
        # clicked_cell_2 = self.tableWidget.item(row, 2).text()    #시간
        #
        # # tablewidget에서 Clicked row의 강좌 정보를 가지고 'tabWidget_teach_less_arr'의 특정 Record를 읽어옴
        # for i in range(len(tabWidget_teach_less_arr)):
        #     if tabWidget_teach_less_arr[i][0].split(": ")[1] != clicked_cell_0: continue
        #     if tabWidget_teach_less_arr[i][1].split(": ")[1] != clicked_cell_1: continue
        #     if tabWidget_teach_less_arr[i][2]                != clicked_cell_2: continue
        #     teach_less_info = tabWidget_teach_less_arr[i]
        #     break

    def detail_list_by_lesson(self, idx):
        if idx == 9999:                         #화면 초기화
            selected_lesson_ID = lesson_arr[0].split(":")[0]
        else:
            selected_lesson_ID = lesson_arr[idx].split(":")[0]

        global detail_arr
        detail_arr = []
        for i in range(len(days_text_info_arr)):  # 요일ID, 요일 Text
            if days_text_info_arr[i][0] != selected_lesson_ID: continue   # 강좌
            exist_info = ""


            for j in range(len(df_teacher_lesson_list)):
                if df_teacher_lesson_list[j][0] != Selected_season_ID: continue        #시즌 ID
                if df_teacher_lesson_list[j][2] != days_text_info_arr[i][6]: continue  #레슨 Key
                exist_info = "x"
                break
            if exist_info == "x": continue

            detail_item = ""
            for j in range(len(BB_master_list)):                 #강의실 마스타
                if BB_master_list[j][11] != "x": continue
                if BB_master_list[j][1] != int(days_text_info_arr[i][2][2:]): continue
                detail_item = days_text_info_arr[i][2] + ": " + BB_master_list[j][2]
                break
            detail_item = detail_item + "| " + str(days_text_info_arr[i][3]) + " (교시)"
            detail_item = detail_item + "| (" + days_text_info_arr[i][4] + "): " + days_text_info_arr[i][5]
            if df_lesson_schedule_list[i][4] != " ":
               detail_item = detail_item + "| 그룹키: " + days_text_info_arr[i][1]
            else:
               detail_item = detail_item + "| 단일키"

            detail_arr.append(detail_item)

        global detail_combo_arr
        detail_combo_arr = []
        for i in range(len(detail_arr)):
            detail_combo_arr.append(detail_arr[i].split("| ")[0].split(": ")[1] + "| " + detail_arr[i].split("| ")[1] \
                                    + "| " + detail_arr[i].split("| ")[2] + "| " + detail_arr[i].split("| ")[3])

        if idx != 9999:
            fld3_arr[1][1].clear()
            fld3_arr[1][1].addItems(detail_combo_arr)

    def addInfo(self):
        groupKey = fld3_arr[1][1].currentText().split("| ")[3]
        if groupKey.split(": ")[0] =="그룹키": groupKey = groupKey.split(": ")[1]
        else: groupKey = " "

        add_target_arr = []
        less_info = fld3_arr[0][1].currentText()
        for i in range(len(detail_arr)):
            room_info = detail_arr[i].split("| ")[0]  # 강의실
            for j in range(len(time_period_arr)):
                if time_period_arr[j][1] == int(detail_arr[i].split("| ")[1][:2]):  # 시간
                    time_info = detail_arr[i].split("| ")[1] + ": " + time_period_arr[j][2]
                    break
            days_info = detail_arr[i].split("| ")[2]
            day_ID = days_info.split("): ")[0][1:]
            days_text = days_info.split(": ")[1]
            if groupKey != " ":
                if detail_arr[i].split("| ")[3] == "단일키": continue
                if detail_arr[i].split("| ")[3].split(": ")[1] != groupKey : continue

            else:
                if detail_arr[i].split("| ")[3] != "단일키": continue                 #그룹키
                if fld3_arr[1][1].currentText().split("| ")[0] != detail_arr[i].split("| ")[0].split(": ")[1] or \
                   fld3_arr[1][1].currentText().split("| ")[1] != detail_arr[i].split("| ")[1] or \
                   fld3_arr[1][1].currentText().split("| ")[2] != detail_arr[i].split("| ")[2]: continue   #강의실 명, 시간, 요일

            if groupKey == " ":
               lesson_key = less_info.split(":")[0] + "#" + room_info.split(":")[0] + \
                             str(detail_arr[i].split("| ")[1].split(" (")[0]) + \
                             detail_arr[i].split("| ")[2].split(")")[0].split("(")[1]
            else:
                lesson_key = less_info.split(":")[0] + groupKey + room_info.split(":")[0]

            target_arr = [less_info, room_info, time_info, day_ID, days_text, fld1_arr[1][0].text(),
                          fld2_arr[1][0].text(), "x", "", "", "", groupKey, lesson_key]  # 강좌, 강의실, 시간, 요일ID, 요일, 시작일, 종료일, 생성일/인, 변경일/인, 그룹키
            add_target_arr.append(target_arr)
            if detail_arr[i].split("| ")[3] == "단일키": break

        error_exist = ""
        for i in range(len(add_target_arr)):
            for j in range(len(tabWidget_teach_less_arr)):
                if tabWidget_teach_less_arr[j][0] != add_target_arr[i][0]: continue  #강좌
                if tabWidget_teach_less_arr[j][1] != add_target_arr[i][1]: continue  #강의실
                if tabWidget_teach_less_arr[j][2] != add_target_arr[i][2]: continue  #시간
                if tabWidget_teach_less_arr[j][3] != add_target_arr[i][3]: continue  #요일 ID
                error_exist = "x"
                break
            if error_exist != "": break
        if error_exist != "":
           global_funtion().message_box_1(QMessageBox.Critical, "오류", "이미 등록된 강좌 정보가 존재", "확인")
           return

        for i in range(len(add_target_arr)):
            tabWidget_teach_less_arr.append(add_target_arr[i])
        list.sort(tabWidget_teach_less_arr, key=lambda k: (k[0], k[11], k[1], k[2]))

        self.retranslateUi()

    def delInfo(self):
        try:
            teach_less_info
        except NameError:
            global_funtion().message_box_1(QMessageBox.Warning, "경고", "삭제할 행을 선택하시오", "확인")
            pass
        else:
            exist_err = "N"
            for i in range(len(df_student_lesson_list)):
                if teach_less_info[11] == " ":
                    if df_student_lesson_list[i][0] != Selected_season_ID: continue                        #시즌 ID
                    if df_student_lesson_list[i][2] != teach_less_info[0].split(": ")[0]: continue         #강좌 ID
                    if df_student_lesson_list[i][4] != teach_less_info[1].split(": ")[0]: continue         #강의실 ID
                    if df_student_lesson_list[i][5] != int(teach_less_info[2].split(" (")[0]): continue    #시간 ID
                    if df_student_lesson_list[i][6] != teach_less_info[3]: continue                        #요일 ID
                    exist_err = "Y"
                else:
                    if df_student_lesson_list[i][3] != teach_less_info[11]: continue                       #그룹 키
                    exist_err = "Y"
                break

            if exist_err == "Y":
               global_funtion().message_box_1(QMessageBox.Warning, "경고", "수강생이 등록되어 있어 삭제불가함", "확인")
               return

            del_idx_arr = []                                   #지울 대상의 Index를 수집할 목적
            for i in range(len(tabWidget_teach_less_arr)):
                if teach_less_info[11] == " ":
                    if i == selected_row_idx:
                       tabWidget_teach_less_arr.__delitem__(i)
                       self.tableWidget.removeRow(i)
                       break
                else:
                    if tabWidget_teach_less_arr[i][11] == teach_less_info[11]:
                        del_idx_arr.append(i)

            if len(del_idx_arr) != 0:
                del_idx_arr.sort(reverse=True)
                for i in range(len(del_idx_arr)):
                    tabWidget_teach_less_arr.__delitem__(del_idx_arr[i])
                    self.tableWidget.removeRow(del_idx_arr[i])

            self.retranslateUi()

    def accept(self):
        global_funtion().message_box_2(QMessageBox.Question, "확인", "작성내용을 저장하시겠습니까?", "예", "아니오")
        if MsgBoxRtnSignal == 'Y':
            target_updated_record = 0                   #TableWidget내 생성/변경 정보가 있는 지 점검하기 위한 인자
            temp_teach_less_list = []
            for i in range(len(tabWidget_teach_less_arr)):
                if i != 0 and tabWidget_teach_less_arr[i][11] != " " and tabWidget_teach_less_arr[i][11] == tabWidget_teach_less_arr[i-1][11]:
                    continue
                temp_teach_less_arr = []
                temp_teach_less_arr.append(Selected_season_ID)                                  #시즌 ID
                temp_teach_less_arr.append(selected_ID)                                         #강사 ID
                temp_teach_less_arr.append(tabWidget_teach_less_arr[i][12])                     #레슨키
                temp_teach_less_arr.append(tabWidget_teach_less_arr[i][5])                      #시작일
                temp_teach_less_arr.append(tabWidget_teach_less_arr[i][6])                      #종료일
                if tabWidget_teach_less_arr[i][7] == "x":      #생성일
                   tabWidget_teach_less_arr[i][7] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                   tabWidget_teach_less_arr[i][8] = "admin"   #생성인
                   target_updated_record += 1
                else:
                   if tabWidget_teach_less_arr[i][9] == "x":      #변경일
                      tabWidget_teach_less_arr[i][9] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                      tabWidget_teach_less_arr[i][10] = "admin"   #변경인
                      target_updated_record += 1
                temp_teach_less_arr.append(tabWidget_teach_less_arr[i][7])                     #생성일
                temp_teach_less_arr.append(tabWidget_teach_less_arr[i][8])                     #생성인
                temp_teach_less_arr.append(tabWidget_teach_less_arr[i][9])                     #변경일
                temp_teach_less_arr.append(tabWidget_teach_less_arr[i][10])                    #변경인
                temp_teach_less_list.append(temp_teach_less_arr)

            if target_updated_record == 0 and length_of_tabWidget == len(tabWidget_teach_less_arr):
               global_funtion().message_box_1(QMessageBox.Warning, "경고", "변경된 정보가 없습니다", "확인")
               return

            # 최초 excel file에서 추출한 list를 다시 excel file로 저장하기 위해 현재 화면에 출력된 기존/생성/수정/변경된 정보를
            # 갱신하기 위해 화면에 출력된 기존 list 정보값을 모두 지우고 다시 화면 리스트 정보를 Append하여 excel file에 저장한 대상을 정비함
            del_idx_arr = []                       # numpy array 기능을 이용하기 위해 지울 대상의 Index를 수집할 목적
            for i in range(len(df_teacher_lesson_list)):
               if df_teacher_lesson_list[i][0] == Selected_season_ID and df_teacher_lesson_list[i][1] == selected_ID:
                  del_idx_arr.append(i)

            np_type_arr = np.array(df_teacher_lesson_list)   #일반 배열을 numpy array 유형으로 전환하면 각 요소를 구분하는 Comma(,)가 제거된 상태가 됨
            np_type_arr = np.delete(np_type_arr, del_idx_arr, axis = 0)     # axis = 0 (Row), 1(Column)
            normal_arr = np_type_arr.tolist()

            df_teacher_lesson_list.clear()
            for i in range(len(normal_arr)):
                df_teacher_lesson_list.append(normal_arr[i])

            for i in range(len(temp_teach_less_list)):
                df_teacher_lesson_list.append(temp_teach_less_list[i])

            list.sort(df_teacher_lesson_list, key=lambda k: (k[0], k[1], k[2]))
            df = pd.DataFrame(df_teacher_lesson_list, columns=df_teacher_lesson_col)
            df.to_excel('table/DD_teacher_lesson.xlsx', index=False)
            global_funtion().message_box_1(QMessageBox.Information, "정보", "저장되었습니다", "확인")

            # Ui_Lesson_Master_Mgmt().close()
            self.close()
            # Ui_Lesson_Master_Mgmt().exec_()
            # Ui_Master_Mgmt().exec_()
        else: pass

class Ui_Student_Lesson_Assign(QDialog):
    def __init__(self):
        super().__init__()
        self.get_Init_data()
        self.setupUi()

    def get_Init_data(self):
        global days_arr, selected_ID, selected_name, lesson_arr

        selected_ID = selected_info[0]
        selected_name = selected_info[1]

        lesson_arr = []
        for i in range(len(CC_master_list)):
            if CC_master_list[i][11] != "x": continue
            lesson_arr.append(CC_master_list[i][0] + str(CC_master_list[i][1]) + ": " + CC_master_list[i][2])

        self.detail_list_by_lesson(9999)

        global length_of_tabWidget
        length_of_tabWidget = len(tabWidget_stud_less_arr)

    def setupUi(self):
        self.setWindowTitle("수강생/강좌 관리")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setFixedSize(540, 665)

        self.label = QLabel(self)
        self.label.setGeometry(QRect(0, 15, 510, 40))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("수강생/강좌 등록")
        global_funtion().fontSetting(self.label, '6B', 24, " ")  # "에스코어 드림 6 Bold", PointSize(24)

        self.gridLayoutWidget = QWidget(self)
        self.gridLayoutWidget.setGeometry(QRect(50, 80, 440, 100))

        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(20)

        title_arr = ["수  강  생", "기      간" ]
        for i in range(len(title_arr)):
            self.label = QLabel(self.gridLayoutWidget)
            self.label.setText(title_arr[i])
            self.gridLayout.addWidget(self.label, i, 0, 1, 1)

        global fld1_arr, fld2_arr, fld3_arr
        fld1_arr = [["self.studentLE1", selected_ID], ["self.prdStrQDt", ""]]
        for i in range(len(fld1_arr)):
            if i != 1:
                fld1_arr[i][0] = QLineEdit(self.gridLayoutWidget)
                fld1_arr[i][0].setText(fld1_arr[i][1])
                fld1_arr[i][0].setReadOnly(True)
                fld1_arr[i][0].setStyleSheet("background: lightgray")
            else:
                fld1_arr[i][0] = QDateEdit(self.gridLayoutWidget)
                fld1_arr[i][0].setDate(QDate.fromString(CC_master_list[0][5], 'yyyy-MM-dd'))
                fld1_arr[i][0].setCalendarPopup(True)
            self.gridLayout.addWidget(fld1_arr[i][0], i, 1, 1, 1)

        fld2_arr = [["self.studentLE2", selected_name], ["self.prdEndQDt", ""]]
        for i in range(len(fld2_arr)):
            if i != 1:
                fld2_arr[i][0] = QLineEdit(self.gridLayoutWidget)
                fld2_arr[i][0].setReadOnly(True)
                if fld2_arr[i][1] != "":
                   fld2_arr[i][0].setText(fld2_arr[i][1])
                fld2_arr[i][0].setStyleSheet("background: lightgray")
            else:
                fld2_arr[i][0] = QDateEdit(self.gridLayoutWidget)
                fld2_arr[i][0].setDate(QDate.fromString(CC_master_list[0][6], 'yyyy-MM-dd'))
                fld2_arr[i][0].setCalendarPopup(True)
            self.gridLayout.addWidget(fld2_arr[i][0], i, 2, 1, 1)

        self.formLayoutWidget = QWidget(self)
        self.formLayoutWidget.setGeometry(QRect(50, 190, 440, 140))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setHorizontalSpacing(20)
        self.formLayout.setVerticalSpacing(20)

        fld3_arr = [["강      좌", "self.comboBox_lesson", lesson_arr, self.detail_list_by_lesson],
                    ["강      사", "self.comboBox_teacher", teacher_combo_arr, self.detail_list_by_teacher],
                    ["상      세", "self.comboBox_detail", detail_combo_arr]]
        for i in range(len(fld3_arr)):
            self.label = QLabel(self.formLayoutWidget)
            self.label.setText(fld3_arr[i][0])
            self.formLayout.setWidget(i, QFormLayout.LabelRole, self.label)

            fld3_arr[i][1] = QComboBox(self.formLayoutWidget)
            fld3_arr[i][1].addItems(fld3_arr[i][2])
            if i in (0, 1):
               fld3_arr[i][1].currentIndexChanged[int].connect(fld3_arr[i][3])
            self.formLayout.setWidget(i, QFormLayout.FieldRole, fld3_arr[i][1])

        tool_button_arr = [["강좌 추가", 440, 300, 30, 30, "img/add-file.png", 30, 30, self.addInfo],
                           ["강좌 삭제", 480, 300, 30, 30, "img/delete.png", 30, 30, self.delInfo]]
        for i in range(len(tool_button_arr)):
            self.toolButton = QToolButton(self)
            global_funtion().tool_button_setting(self.toolButton, tool_button_arr[i])

        tableWidget_hdr_arr = ["강좌", "강사", "강의실", "시간", "요일", "시작일", "종료일"]
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QRect(10, 330, 510, 255))
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 전체 cell read-only
        self.tableWidget.verticalHeader().setVisible(False)  # index 안보이는 기능
        self.tableWidget.setColumnCount(len(tableWidget_hdr_arr))
        self.tableWidget.setRowCount(0)
        self.tableWidget.cellClicked.connect(self.handleCellClicked)

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStyleSheet("::section {""background-color: lightgray;""}")  # TableWidget내 헤더 Title의 배경색은 일반적으로 달리 이렇게 지정함
        for i in range(len(tableWidget_hdr_arr)):
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setHorizontalHeaderItem(i, item)
            item = self.tableWidget.horizontalHeaderItem(i)
            item.setText(tableWidget_hdr_arr[i])

        self.buttonBox = QDialogButtonBox(self)
        global_funtion().final_decision_button_box(self.buttonBox, 150, 600, 340, 30, "저장", "취소",
                                                   self.accept, self.reject)
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        old_group_key = ""
        x = 0
        self.tableWidget.clearContents()
        for i in range(len(tabWidget_stud_less_arr)):
            self.tableWidget.removeRow(i)
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            if tabWidget_stud_less_arr[i][12] != " ":
                 if old_group_key != "" and old_group_key != tabWidget_stud_less_arr[i][12]: x += 1
            for j in range(len(tabWidget_stud_less_arr[i])):
                k = j
                if j >= 5: k = j - 1
                if j == 4: continue
                if j == 8: break
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(i, k, item)
                item = self.tableWidget.item(i, k)
                if j <= 5 and tabWidget_stud_less_arr[i][12] != " ":
                   item.setBackground(QColor(bg_color_arr[x%5]))
                if j in (0, 1, 2):
                   item.setText(tabWidget_stud_less_arr[i][j].split(": ")[1])
                else:
                   item.setText(tabWidget_stud_less_arr[i][j])
            old_group_key = tabWidget_stud_less_arr[i][12]

    def handleCellClicked(self, row):
        global stud_less_info, selected_row_idx
        selected_row_idx = row
        stud_less_info = tabWidget_stud_less_arr[selected_row_idx]

    def detail_list_by_lesson(self, idx):
        if idx == 9999:                         #화면 초기화
            selected_lesson_ID = lesson_arr[0].split(":")[0]
        else:
            selected_lesson_ID = lesson_arr[idx].split(":")[0]

        global detail_arr, teacher_arr
        detail_arr = []
        teacher_arr = []
        for i in range(len(days_text_info_arr)):  # 요일ID, 요일 Text
            if days_text_info_arr[i][0] != selected_lesson_ID: continue  # 강좌
            exist_info = ""
            for j in range(len(df_student_lesson_list)):
                if df_student_lesson_list[j][0] != Selected_season_ID: continue  # 시즌 ID
                if df_student_lesson_list[j][1] != selected_ID: continue         # 수강생 ID
                if df_student_lesson_list[j][2] != days_text_info_arr[i][7]: continue  # 강좌 ID
                break
            if exist_info == "x": continue

            exist_info = ""
            detail_item = ""
            for j in range(len(df_teacher_lesson_list)):
                if df_teacher_lesson_list[j][0] != Selected_season_ID: continue              # 시즌 ID
                if df_teacher_lesson_list[j][2] != days_text_info_arr[i][7]: continue        # 레슨 Key

                teacher_arr.append(df_teacher_lesson_list[j][1])  # 강사 ID
                detail_item = df_teacher_lesson_list[j][1] + "| "
                exist_info = "x"
                break
            if exist_info == "": continue

            for j in range(len(BB_master_list)):  # 강의실 마스타
                if BB_master_list[j][11] != "x": continue
                if BB_master_list[j][1] != int(days_text_info_arr[i][2][2:]): continue
                detail_item = detail_item + days_text_info_arr[i][2] + ": " + BB_master_list[j][2]
                break
            detail_item = detail_item + "| " + str(days_text_info_arr[i][3]) + " (교시)"

            detail_item = detail_item + "| (" + days_text_info_arr[i][4] + "): " + days_text_info_arr[i][5]

            if df_lesson_schedule_list[i][4] != " ":
                detail_item = detail_item + "| 그룹키: " + days_text_info_arr[i][1]
            else:
                detail_item = detail_item + "| 단일키"

            detail_arr.append(detail_item)

        global teacher_combo_arr
        teacher_arr = list(set(teacher_arr))                      #배열 원소들의 중복제거를 위해 set함수로 단일화한 다음 다시 list함수를 통해 배열형태로 변환
        teacher_arr.sort()
        teacher_combo_arr = []
        for i in range(len(teacher_arr)):
            for j in range(len(DD_master_list)):
                if DD_master_list[j][1] == int(teacher_arr[i][2:]):
                    teacher_combo_arr.append(teacher_arr[i] + ": " + DD_master_list[j][2])
                    break

        if len(teacher_combo_arr) != 0:
           teacher_combo_selected = teacher_combo_arr[0].split(":")[0]

        global detail_combo_arr
        detail_combo_arr = []
        for i in range(len(detail_arr)):
            if detail_arr[i].split("| ")[0] != teacher_combo_selected: continue
            detail_combo_arr.append(detail_arr[i].split("| ")[1].split(": ")[1] + "| " + detail_arr[i].split("| ")[2] \
                                    + "| " + detail_arr[i].split("| ")[3] + "| " + detail_arr[i].split("| ")[4])

        if idx != 9999:
            fld3_arr[1][1].clear()
            fld3_arr[1][1].addItems(teacher_combo_arr)
            fld3_arr[2][1].clear()
            fld3_arr[2][1].addItems(detail_combo_arr)

    def detail_list_by_teacher(self, idx):
        if len(teacher_combo_arr) == 0: return
        selected_teacher_ID = teacher_combo_arr[idx].split(":")[0]

        detail_combo_arr = []
        for i in range(len(detail_arr)):
            if detail_arr[i].split("| ")[0] != selected_teacher_ID: continue
            detail_combo_arr.append(detail_arr[i].split("| ")[1].split(": ")[1] + "| " + detail_arr[i].split("| ")[2] \
                                    + "| " + detail_arr[i].split("| ")[3] + "| " + detail_arr[i].split("| ")[4])

        fld3_arr[2][1].clear()
        fld3_arr[2][1].addItems(detail_combo_arr)

    def addInfo(self):
        if fld3_arr[1][1].currentText() == "" or fld3_arr[2][1].currentText() == "":       #강사, 상세정보
           global_funtion().message_box_1(QMessageBox.Critical, "오류", "강사 혹은 상세정보가 누락되었습니다", "확인")
           return

        groupKey = fld3_arr[2][1].currentText().split("| ")[3]
        if groupKey.split(": ")[0] =="그룹키": groupKey = groupKey.split(": ")[1]
        else: groupKey = " "

        add_target_arr = []
        less_info = fld3_arr[0][1].currentText()
        for i in range(len(detail_arr)):
            teacher_info = fld3_arr[1][1].currentText()
            room_info = detail_arr[i].split("| ")[1]  # 강의실
            for j in range(len(time_period_arr)):
                if time_period_arr[j][1] == int(detail_arr[i].split("| ")[2][:2]):  # 시간
                    time_info = detail_arr[i].split("| ")[2] + ": " + time_period_arr[j][2]
                    break
            days_info = detail_arr[i].split("| ")[3]
            day_ID = days_info.split("): ")[0][1:]
            days_text = days_info.split(": ")[1]
            if groupKey != " ":
                if detail_arr[i].split("| ")[4] == "단일키": continue
                if detail_arr[i].split("| ")[4].split(": ")[1] != groupKey : continue
                lesson_key = less_info.split(":")[0] + groupKey + room_info.split(":")[0]
            else:
                if detail_arr[i].split("| ")[4] != "단일키": continue                 #그룹키
                if fld3_arr[2][1].currentText().split("| ")[0] != detail_arr[i].split("| ")[1].split(": ")[1] or \
                   fld3_arr[2][1].currentText().split("| ")[1] != detail_arr[i].split("| ")[2] or \
                   fld3_arr[2][1].currentText().split("| ")[2] != detail_arr[i].split("| ")[3]: continue   #강의실 명, 시간, 요일
                lesson_key = less_info.split(":")[0] + "#" + room_info.split(":")[0] + \
                            str(int(detail_arr[i].split("| ")[2][:2])) + day_ID
            target_arr = [less_info, teacher_info, room_info, time_info, day_ID, days_text, fld1_arr[1][0].text(),
                          fld2_arr[1][0].text(), "x", "", "", "", groupKey, lesson_key]  # 강좌, 강사, 강의실, 시간, 요일, 시작일, 종료일, 생성일/인, 변경일/인, 그룹키
            add_target_arr.append(target_arr)
            if detail_arr[i].split("| ")[4] == "단일키": break

        error_exist = ""
        for i in range(len(add_target_arr)):
            for j in range(len(tabWidget_stud_less_arr)):
                if tabWidget_stud_less_arr[j][0] != add_target_arr[i][0]: continue  #강좌
                if tabWidget_stud_less_arr[j][1] != add_target_arr[i][1]: continue  #강의실
                if tabWidget_stud_less_arr[j][2] != add_target_arr[i][2]: continue  #시간
                if tabWidget_stud_less_arr[j][3] != add_target_arr[i][3]: continue  #요일 ID
                error_exist = "x"
                break
            if error_exist != "": break
        if error_exist != "":
           global_funtion().message_box_1(QMessageBox.Critical, "오류", "이미 등록된 강좌 정보가 존재", "확인")
           return

        for i in range(len(add_target_arr)):
            tabWidget_stud_less_arr.append(add_target_arr[i])
        list.sort(tabWidget_stud_less_arr, key=lambda k: (k[0], k[12], k[1], k[2]))

        self.retranslateUi()

    def delInfo(self):
        try:
            stud_less_info
        except NameError:
            global_funtion().message_box_1(QMessageBox.Warning, "경고", "삭제할 행을 선택하시오", "확인")
            pass
        else:
            del_idx_arr = []                  #지울 대상의 Index를 수집할 목적
            for i in range(len(tabWidget_stud_less_arr)):
                if stud_less_info[12] == " ":
                    if i == selected_row_idx:
                       tabWidget_stud_less_arr.__delitem__(i)
                       self.tableWidget.removeRow(i)
                       break
                else:
                    if tabWidget_stud_less_arr[i][12] == stud_less_info[12]:
                       del_idx_arr.append(i)

            if len(del_idx_arr) != 0:
                del_idx_arr.sort(reverse=True)
                for i in range(len(del_idx_arr)):
                    tabWidget_stud_less_arr.__delitem__(del_idx_arr[i])
                    self.tableWidget.removeRow(del_idx_arr[i])

            self.retranslateUi()

    def accept(self):
        global_funtion().message_box_2(QMessageBox.Question, "확인", "작성내용을 저장하시겠습니까?", "예", "아니오")
        if MsgBoxRtnSignal == 'Y':
            target_updated_record = 0                   #TableWidget내 생성/변경 정보가 있는 지 점검하기 위한 인자
            temp_stud_less_list = []
            for i in range(len(tabWidget_stud_less_arr)):
                if i != 0 and tabWidget_stud_less_arr[i][12] != " " and tabWidget_stud_less_arr[i][12] == tabWidget_stud_less_arr[i-1][12]:
                    continue
                temp_stud_less_arr = []
                temp_stud_less_arr.append(Selected_season_ID)                                 # 시즌 ID
                temp_stud_less_arr.append(selected_ID)                                        # 수강생 ID
                temp_stud_less_arr.append(tabWidget_stud_less_arr[i][13])                     # 레슨 Key
                temp_stud_less_arr.append(tabWidget_stud_less_arr[i][6])                      # 시작일
                temp_stud_less_arr.append(tabWidget_stud_less_arr[i][7])                      # 종료일
                if tabWidget_stud_less_arr[i][8] == "x":      # 생성일
                   tabWidget_stud_less_arr[i][8] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                   tabWidget_stud_less_arr[i][9] = "admin"    # 생성인
                   target_updated_record += 1
                else:
                   if tabWidget_stud_less_arr[i][10] == "x":      # 변경일
                      tabWidget_stud_less_arr[i][10] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                      tabWidget_stud_less_arr[i][11] = "admin"    # 변경인
                      target_updated_record += 1
                temp_stud_less_arr.append(tabWidget_stud_less_arr[i][8])                     # 생성일
                temp_stud_less_arr.append(tabWidget_stud_less_arr[i][9])                     # 생성인
                temp_stud_less_arr.append(tabWidget_stud_less_arr[i][10])                    # 변경일
                temp_stud_less_arr.append(tabWidget_stud_less_arr[i][11])                    # 변경인
                temp_stud_less_list.append(temp_stud_less_arr)

            if target_updated_record == 0 and length_of_tabWidget == len(tabWidget_stud_less_arr):
               global_funtion().message_box_1(QMessageBox.Warning, "경고", "변경된 정보가 없습니다", "확인")
               return

            # 최초 excel file에서 추출한 list를 다시 excel file로 저장하기 위해 현재 화면에 출력된 기존/생성/수정/변경된 정보를
            # 갱신하기 위해 화면에 출력된 기존 list 정보값을 모두 지우고 다시 화면 리스트 정보를 Append하여 excel file에 저장한 대상을 정비함
            del_idx_arr = []                       # numpy array 기능을 이용하기 위해 지울 대상의 Index를 수집할 목적
            for i in range(len(df_student_lesson_list)):
               if df_student_lesson_list[i][0] == Selected_season_ID and df_student_lesson_list[i][1] == selected_ID:
                  del_idx_arr.append(i)

            np_type_arr = np.array(df_student_lesson_list)   #일반 배열을 numpy array 유형으로 전환하면 각 요소를 구분하는 Comma(,)가 제거된 상태가 됨
            np_type_arr = np.delete(np_type_arr, del_idx_arr, axis = 0)     # axis = 0 (Row), 1(Column)
            normal_arr = np_type_arr.tolist()

            df_student_lesson_list.clear()
            for i in range(len(normal_arr)):
                df_student_lesson_list.append(normal_arr[i])

            for i in range(len(temp_stud_less_list)):
                df_student_lesson_list.append(temp_stud_less_list[i])

            list.sort(df_student_lesson_list, key=lambda k: (k[0], k[1], k[2]))
            df = pd.DataFrame(df_student_lesson_list, columns=df_student_lesson_col)
            df.to_excel('table/EE_student_lesson.xlsx', index=False)
            global_funtion().message_box_1(QMessageBox.Information, "정보", "저장되었습니다", "확인")

            # Ui_Lesson_Master_Mgmt().close()
            self.close()
            # Ui_Lesson_Master_Mgmt().exec_()
            # Ui_Master_Mgmt().exec_()
        else: pass

class Ui_Season_Master_Mgmt(QDialog):
    def __init__(self):
        super().__init__()
        self.get_Init_data()
        self.setupUi()

    def get_Init_data(self):
        global scr_control_event, win_header_title, master_type, master_ID, tabWidget_time_info_arr

        master_type = clickedRcdInfo[0]

        master_ID = clickedRcdInfo[0] + str(clickedRcdInfo[1])

        scr_control_event = "CRT"           # 생성
        win_header_title = "강의시즌 등록"
        if str(clickedRcdInfo[1]) != "":
            scr_control_event = "CHG"       # 수정
            win_header_title = "강의시즌 정보수정"

        tabWidget_time_info_arr = []
        for i in range(len(df_time_period_list)):
            if df_time_period_list[i][0] != master_ID: continue
            tabWidget_time_info_arr.append(df_time_period_list[i])

    def setupUi(self):
        self.setWindowTitle("기준정보")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        self.buttonBox = QDialogButtonBox(self)
        if scr_control_event == "CRT":
            self.setFixedSize(490, 460)
            global_funtion().final_decision_button_box(self.buttonBox, 130, 410, 340, 30, "저장", "나가기",
                                                       self.accept, self.reject)
        else:
            self.setFixedSize(490, 660)
            global_funtion().final_decision_button_box(self.buttonBox, 130, 605, 340, 30, "저장", "나가기",
                                                   self.accept, self.reject)

        self.label = QLabel(self)
        self.label.setGeometry(QRect(0, 20, 490, 40))
        self.label.setFrameShadow(QFrame.Sunken)
        self.label.setLineWidth(1)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText(win_header_title)
        global_funtion().fontSetting(self.label, '6B', 24, " ")  # "에스코어 드림 6 Bold", PointSize(24)

        self.gridLayoutWidget = QWidget(self)
        self.gridLayoutWidget.setGeometry(QRect(20, 70, 450, 320))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(10, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setObjectName("gridLayout")

        # item_title = ["ID", "시즌명(필수)", "년/학기(필수)", " ", "시작일 ", "종료일", "비고1", "비고2", "비고3"]
        for i in range(0, 9):
            self.label = QLabel(self.gridLayoutWidget)
            item_title = AA_master_list_col[i + 1]
            if i == 1 or i == 2:
                item_title += "(필수)"
            elif i == 3:
                item_title = " "
            elif i > 3:
                item_title = AA_master_list_col[i]
            self.label.setText(item_title)
            global_funtion().fontSetting(self.label, '6B', 10, " ")
            self.gridLayout.addWidget(self.label, i, 0, 1, 1)

        self.groupBox = QGroupBox(self.gridLayoutWidget)
        self.groupBox.setMaximumSize(QSize(16777215, 25))
        self.groupBox.setStyleSheet("border : 0")
        self.idLabel = QLabel(self.groupBox)
        self.idLabel.setGeometry(QRect(0, 5, 80, 15))
        if scr_control_event == "CRT":
            self.idLabel.setText("")
        else:
            self.idLabel.setText(master_ID)     # ID
        if scr_control_event == "CRT":
            tool_button_arr = ["ID 생성(필수정보 입력필)", 280, 0, 25, 25, "img/add_person.png", 25, 25, self.addMember]

        else:
            tool_button_arr = ["최신정보 갱신", 280, 0, 25, 25, "img/refresh.png", 25, 25, self.refreshInfo]
        self.toolButton = QToolButton(self.groupBox)
        global_funtion().tool_button_setting(self.toolButton, tool_button_arr)
        self.gridLayout.addWidget(self.groupBox, 0, 1, 1, 1)

        self.nameLE = QLineEdit(self.gridLayoutWidget)    #시즌명
        self.nameLE.setText(str(clickedRcdInfo[2]))
        self.gridLayout.addWidget(self.nameLE, 1, 1, 1, 1)

        comboBox_arr = ["정규", "특강", "기타"]
        self.fld1_LE = QComboBox(self.gridLayoutWidget)
        self.fld1_LE.addItems(comboBox_arr)
        self.fld1_LE.setCurrentText(clickedRcdInfo[3])
        self.gridLayout.addWidget(self.fld1_LE, 2, 1, 1, 1)

        self.groupBox = QGroupBox(self.gridLayoutWidget)
        self.groupBox.setMaximumSize(QSize(16777215, 30))

        self.line = QFrame(self.groupBox)
        self.line.setGeometry(QRect(160, 0, 20, 30))
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.checkBox = QCheckBox(self.groupBox)
        self.checkBox.setText("활성")
        if scr_control_event == "CHG":                   # scr_control_event이 Blank이면 생성화면을 의미, 아니면 수정화면
            if clickedRcdInfo[11] == "x":
                self.checkBox.setChecked(True)
            else:
                self.checkBox.setChecked(False)
        else:
            self.checkBox.setChecked(True)
            self.checkBox.setEnabled(False)
        self.checkBox.setGeometry(QRect(220, 5, 60, 20))
        self.gridLayout.addWidget(self.groupBox, 3, 1, 1, 1)

        self.fld2_DE = QDateEdit(self.gridLayoutWidget)

        global start_date, end_date
        if scr_control_event == "CHG":
            start_date = QDate.fromString(clickedRcdInfo[4], 'yyyy-MM-dd')
        else:
            start_date = AA_master_list[-1][5]
            print(start_date)
            start_date = QDate.fromString(start_date, 'yyyy-MM-dd').addDays(1)
            # new_start_date = new_start_date.addDays(1)
        self.fld2_DE.setDate(start_date)  # 시작일
        self.fld2_DE.setCalendarPopup(True)
        self.gridLayout.addWidget(self.fld2_DE, 4, 1, 1, 1)

        self.fld3_DE = QDateEdit(self.gridLayoutWidget)
        if scr_control_event == "CHG":
            end_date = QDate.fromString(clickedRcdInfo[5], 'yyyy-MM-dd')
        else:
            end_date = start_date.addMonths(3).addDays(-1)
        self.fld3_DE.setDate(end_date)  #종료일
        self.fld3_DE.setCalendarPopup(True)
        self.gridLayout.addWidget(self.fld3_DE, 5, 1, 1, 1)

        self.fld4_LE = QLineEdit(self.gridLayoutWidget)
        self.fld4_LE.setText(clickedRcdInfo[6])         #비고1
        self.gridLayout.addWidget(self.fld4_LE, 6, 1, 1, 1)

        self.remark1LE = QLineEdit(self.gridLayoutWidget)
        self.remark1LE.setText(clickedRcdInfo[7])       #비고2
        self.gridLayout.addWidget(self.remark1LE, 7, 1, 1, 1)

        self.remark2LE = QLineEdit(self.gridLayoutWidget)
        self.remark2LE.setText(clickedRcdInfo[8])       #비고3
        self.gridLayout.addWidget(self.remark2LE, 8, 1, 1, 1)

        if scr_control_event == "CHG":  # 수정
            lesson_apply_hdr_arr = ["시간", "시간명", "시작시간", "종료시간"]
            self.tableWidget = QTableWidget(self)
            self.tableWidget.setGeometry(QRect(20, 390, 450, 190))
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 전체 cell read-only
            self.tableWidget.verticalHeader().setVisible(False)  # index 안보이는 기능

            if tabWidget_time_info_arr != []:
                self.tableWidget.setColumnCount(len(lesson_apply_hdr_arr))
                self.tableWidget.setRowCount(0)

                header = self.tableWidget.horizontalHeader()
                # header.setSectionResizeMode(QHeaderView.ResizeToContents)
                header.setSectionResizeMode(QHeaderView.Stretch)
                header.setStyleSheet("::section {""background-color: lightgray;""}")  # TableWidget내 헤더 Title의 배경색은 일반적으로 달리 이렇게 지정함
                for i in range(len(lesson_apply_hdr_arr)):
                    item = QTableWidgetItem()
                    self.tableWidget.setHorizontalHeaderItem(i, item)
                    item = self.tableWidget.horizontalHeaderItem(i)
                    item.setText(lesson_apply_hdr_arr[i])

            tool_button_arr = ["시간관리", 20, 600, 30, 30, "img/edit.png", 30, 30, self.addInfo]
            self.toolButton = QToolButton(self)
            global_funtion().tool_button_setting(self.toolButton, tool_button_arr)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate

        if scr_control_event != "CHG":  return   # 수정
        if tabWidget_time_info_arr == []: return

        self.tableWidget.clearContents()
        for i in range(len(tabWidget_time_info_arr)):
            self.tableWidget.removeRow(i)
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            for j in range(len(tabWidget_time_info_arr[i])):
                if j == 5: break
                if j == 0: continue
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(i, j - 1, item)
                item = self.tableWidget.item(i, j - 1)
                if j == 1:
                    item.setBackground(QColor("lightgreen"))
                    item.setText(str(tabWidget_time_info_arr[i][j]) + " (교시)")
                else:
                    item.setText(tabWidget_time_info_arr[i][j])

    def addMember(self):
        if self.nameLE.text() != "":
            self.idLabel.setText(clickedRcdInfo[0] + str(df_super_list[0][11]))
        else:
            global_funtion().message_box_1(QMessageBox.Warning, "경고", "필수 정보를 입력해주세요.", "확인")


    def addInfo(self):
        global selected_info
        selected_info = [self.idLabel.text(), self.nameLE.text(), " ",  " "]
        win = Ui_Season_Period()
        win.exec_()

    def refreshInfo(self):
        self.close()
        self.__init__()
        self.exec_()

    def accept(self):
        if self.nameLE.text() == "" or self.fld1_LE.currentText() == "":
            global_funtion().message_box_1(QMessageBox.Warning, "경고", "필수 정보를 입력해주세요.", "확인")
            return
        if self.idLabel.text() == "":
            global_funtion().message_box_1(QMessageBox.Warning, "경고", "ID를 생성해주세요.", "확인")
            return
        if QDate.fromString(self.fld2_DE.text(), "yyyy-MM-dd") >= QDate.fromString(self.fld3_DE.text(), "yyyy-MM-dd"):
            global_funtion().message_box_1(QMessageBox.Warning, "경고", "시작일자가 종료일자보다 느릴 수 없습니다.", "확인")
            return

        AA_create_arr = [clickedRcdInfo[0], int(self.idLabel.text()[2:7]), self.nameLE.text(), self.fld1_LE.currentText(),
                         self.fld2_DE.text(),
                         self.fld3_DE.text(), self.fld4_LE.text(), self.remark1LE.text(), self.remark2LE.text(), "", "", "",
                         "", "", "", ""]
        if self.checkBox.isChecked() == True:
            AA_create_arr[11] = "x"
        if scr_control_event == "CRT":
            if QDate.fromString(self.fld2_DE.text(), "yyyy-MM-dd") <=  QDate.fromString(AA_master_list[-1][5], "yyyy-MM-dd"):
                global_funtion().message_box_1(QMessageBox.Warning, "경고", "과거 시즌 시간이 겹칩니다. 확인해주세요.", "확인")
                return
            AA_create_arr[12] = datetime.today()
            AA_create_arr[13] = "admin"
            df_super_list[0][11] = df_super_list[0][11] + 1
            df = pd.DataFrame(df_super_list, columns=df_super_col)
            df.to_excel('table/super_master.xlsx', index=False)
        else:
            for i in range(len(AA_master_list)):
                if AA_master_list[i][1] == int(self.idLabel.text()[2:7]):
                    AA_create_arr[1] = AA_master_list[i][1]
                    AA_create_arr[12] = AA_master_list[i][12]
                    AA_create_arr[13] = AA_master_list[i][13]
                    if i != 0 and QDate.fromString(self.fld2_DE.text(), "yyyy-MM-dd") <= QDate.fromString(AA_master_list[i-1][5],"yyyy-MM-dd"):
                        global_funtion().message_box_1(QMessageBox.Warning, "경고", "과거 시즌 시간이 겹칩니다. 확인해주세요.", "확인")
                        return
                    if i != len(AA_master_list)-1 and QDate.fromString(self.fld3_DE.text(), "yyyy-MM-dd") >= QDate.fromString(AA_master_list[i+1][4],"yyyy-MM-dd"):
                        global_funtion().message_box_1(QMessageBox.Warning, "경고", "과거 시즌 시간이 겹칩니다. 확인해주세요.", "확인")
                        return
                    AA_master_list.__delitem__(i)
                    AA_create_arr[14] = datetime.today()
                    AA_create_arr[15] = "admin"

                    break
        AA_master_list.append(AA_create_arr)
        list.sort(AA_master_list, key=lambda k: k[1])
        df = pd.DataFrame(AA_master_list, columns=AA_master_list_col)
        df.to_excel('table/AA_season_master.xlsx', index=False)
        global_funtion().message_box_1(QMessageBox.Information, "정보", "저장되었습니다", "확인")

        self.close()

class Ui_Room_Master_Mgmt(QDialog):
    def __init__(self):
        super().__init__()
        self.get_Init_data()
        self.setupUi()

    def get_Init_data(self):
        global scr_control_event, win_header_title, master_type, master_ID, tabWidget_time_info_arr
        global comboBox_season_arr, season_active_idx

        master_type = clickedRcdInfo[0]
        master_ID = clickedRcdInfo[0] + str(clickedRcdInfo[1])

        scr_control_event = "CRT"           # 생성
        win_header_title = "강의실 등록"
        if str(clickedRcdInfo[1]) != "":
            scr_control_event = "CHG"       # 수정
            win_header_title = "강의실 정보수정"

        self.get_tabWidget_data()

    def get_tabWidget_data(self):
        global tabWidget_room_schl_arr
        tabWidget_room_schl_arr = []
        # room_apply_hdr_arr = ["시간", "요일", "강사", "강좌", "시작일", "종료일"]
        for i in range(len(df_teacher_lesson_list)):
            room_teach_lesson_arr = []
            if df_teacher_lesson_list[i][0] != Selected_season_ID: continue
            if df_teacher_lesson_list[i][4] != master_ID: continue
            # teach_lesson_arr.append(str(df_teacher_lesson_list[i][5]) + " (교시)")                      #시간
            for j in range(len(days_text_info_arr)):                                                   #요일ID, 요일 Text
                # if days_text_info_arr[j][0] != df_teacher_lesson_list[i][2]: continue    #강좌
                if days_text_info_arr[j][7] != df_teacher_lesson_list[i][2]: continue    #그룹 키
                # if days_text_info_arr[j][2] != df_teacher_lesson_list[i][4]: continue    #강의실 ID
                # if days_text_info_arr[j][3] != df_teacher_lesson_list[i][5]: continue    #시간 ID
                # if days_text_info_arr[j][4] != df_teacher_lesson_list[i][6]: continue    #요일 ID
                room_teach_lesson_arr.append(str(df_teacher_lesson_list[i][5]) + " (교시): " + days_text_info_arr[j][6])
                # room_teach_lesson_arr.append(days_text_info_arr[j][4])                        #요일 ID
                room_teach_lesson_arr.append(days_text_info_arr[j][5])                        #요일 Text
                break
            for j in range(len(DD_master_list)):
                if DD_master_list[j][1] != int(df_teacher_lesson_list[i][1][2:]): continue
                room_teach_lesson_arr.append(df_teacher_lesson_list[i][1] + ": " + DD_master_list[j][2])    #강사
                break
            for j in range(len(CC_master_list)):
                if CC_master_list[j][1] != int(df_teacher_lesson_list[i][2][2:]): continue
                room_teach_lesson_arr.append(df_teacher_lesson_list[i][2] + ": " + CC_master_list[j][2])    #강좌
                break

            for k in range(7, 9):                                #시작일, 종료일
                room_teach_lesson_arr.append(df_teacher_lesson_list[i][k])
            # room_teach_lesson_arr.append(df_teacher_lesson_list[i][3])  # 그룹 키
            tabWidget_room_schl_arr.append(room_teach_lesson_arr)

    def setupUi(self):
        self.setWindowTitle("기준정보")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        self.buttonBox = QDialogButtonBox(self)
        if scr_control_event == "CRT":
            self.setFixedSize(490, 460)
            global_funtion().final_decision_button_box(self.buttonBox, 130, 410, 340, 30, "저장", "나가기",
                                                       self.accept, self.reject)
        else:
            self.setFixedSize(490, 660)
            global_funtion().final_decision_button_box(self.buttonBox, 130, 605, 340, 30, "저장", "나가기",
                                                       self.accept, self.reject)

        self.label = QLabel(self)
        self.label.setGeometry(QRect(0, 20, 490, 40))
        self.label.setFrameShadow(QFrame.Sunken)
        self.label.setLineWidth(1)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText(win_header_title)
        global_funtion().fontSetting(self.label, '6B', 24, " ")  # "에스코어 드림 6 Bold", PointSize(24)

        self.gridLayoutWidget = QWidget(self)
        self.gridLayoutWidget.setGeometry(QRect(20, 70, 450, 320))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(10, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setObjectName("gridLayout")

        item_title = ["ID", "강의실명1(필수)", "강의실명2(필수)", " ", "수용인원", "특이사항", "비고1", "비고2", "비고3"]

        for i in range(0, 9):
            self.label = QLabel(self.gridLayoutWidget)
            item_title = BB_master_list_col[i + 1]
            if i == 1 or i == 2:
                item_title += "(필수)"
            elif i == 3:
                item_title = " "
            elif i > 3:
                item_title = BB_master_list_col[i]
            self.label.setText(item_title)
            global_funtion().fontSetting(self.label, '6B', 10, " ")
            self.gridLayout.addWidget(self.label, i, 0, 1, 1)

        self.groupBox = QGroupBox(self.gridLayoutWidget)
        self.groupBox.setMaximumSize(QSize(16777215, 25))
        self.groupBox.setStyleSheet("border : 0")
        self.idLabel = QLabel(self.groupBox)
        self.idLabel.setGeometry(QRect(0, 5, 80, 15))
        if scr_control_event == "CRT":
            self.idLabel.setText("")
        else:
            self.idLabel.setText(master_ID)     # ID
        if scr_control_event == "CRT":
            tool_button_arr = ["ID 생성(필수정보 입력필)", 280, 0, 25, 25, "img/add_person.png", 25, 25, self.addMember]
            for i in range(len(tool_button_arr)):
                self.toolButton = QToolButton(self.groupBox)
                global_funtion().tool_button_setting(self.toolButton, tool_button_arr)
        self.gridLayout.addWidget(self.groupBox, 0, 1, 1, 1)

        self.nameLE = QLineEdit(self.gridLayoutWidget)    # "EE": 이름, "DD": 이름, "CC": 강좌명1, "BB": 강의실명1, "AA":시즌명
        self.nameLE.setText(str(clickedRcdInfo[2]))
        self.gridLayout.addWidget(self.nameLE, 1, 1, 1, 1)

        self.fld1_LE = QLineEdit(self.gridLayoutWidget)  # "EE": 연락처, "DD": 연락처, "CC": 강좌명2, "BB": 강의실명2, "AA":내용
        self.fld1_LE.setText(str(clickedRcdInfo[3]))
        self.gridLayout.addWidget(self.fld1_LE, 2, 1, 1, 1)

        self.groupBox = QGroupBox(self.gridLayoutWidget)
        self.groupBox.setMaximumSize(QSize(16777215, 30))

        self.line = QFrame(self.groupBox)
        self.line.setGeometry(QRect(160, 0, 20, 30))
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.checkBox = QCheckBox(self.groupBox)
        self.checkBox.setText("활성")
        if scr_control_event == "CRT":                   # scr_control_event이 Blank이면 생성화면을 의미, 아니면 수정화면
            self.checkBox.setChecked(True)
            self.checkBox.setEnabled(False)
        else:
            if clickedRcdInfo[11] == "x":
                self.checkBox.setChecked(True)
            else:
                self.checkBox.setChecked(False)
        self.checkBox.setGeometry(QRect(220, 5, 60, 20))
        self.gridLayout.addWidget(self.groupBox, 3, 1, 1, 1)

        comboBox_arr = []                  #강의실
        for i in range(1, 101):
           comboBox_arr.append(str(i) + " (명)")

        self.comboBox1 = QComboBox(self.gridLayoutWidget)
        self.comboBox1.addItems(comboBox_arr)
        if scr_control_event == "CHG":
            self.comboBox1.setCurrentIndex(clickedRcdInfo[4]- 1)
        self.gridLayout.addWidget(self.comboBox1, 4, 1, 1, 1)

        self.fld2_LE = QLineEdit(self.gridLayoutWidget)   #특이사항
        self.fld2_LE.setText(clickedRcdInfo[5])
        self.gridLayout.addWidget(self.fld2_LE, 5, 1, 1, 1)

        self.fld3_LE = QLineEdit(self.gridLayoutWidget)   #비고1
        self.fld3_LE.setText(clickedRcdInfo[6])
        self.gridLayout.addWidget(self.fld3_LE, 6, 1, 1, 1)

        self.fld4_LE = QLineEdit(self.gridLayoutWidget)   #비고2
        self.fld4_LE.setText(clickedRcdInfo[7])
        self.gridLayout.addWidget(self.fld4_LE, 7, 1, 1, 1)

        self.remark1LE = QLineEdit(self.gridLayoutWidget)  #비고3
        self.remark1LE.setText(clickedRcdInfo[8])
        self.gridLayout.addWidget(self.remark1LE, 8, 1, 1, 1)


        if scr_control_event == "CHG":       # 수정
            room_apply_hdr_arr = ["시간", "요일", "강사", "강좌", "시작일", "종료일"]
            self.tableWidget = QTableWidget(self)
            self.tableWidget.setGeometry(QRect(20, 430, 450, 170))
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 전체 cell read-only
            self.tableWidget.verticalHeader().setVisible(False)  # index 안보이는 기능

            if tabWidget_room_schl_arr != []:
                self.tableWidget.setColumnCount(len(room_apply_hdr_arr))
                self.tableWidget.setRowCount(0)

                header = self.tableWidget.horizontalHeader()
                header.setSectionResizeMode(QHeaderView.ResizeToContents)
                # header.setSectionResizeMode(QHeaderView.Stretch)
                header.setStyleSheet("::section {""background-color: lightgray;""}")  # TableWidget내 헤더 Title의 배경색은 일반적으로 달리 이렇게 지정함
                for i in range(len(room_apply_hdr_arr)):
                    item = QTableWidgetItem()
                    self.tableWidget.setHorizontalHeaderItem(i, item)
                    item = self.tableWidget.horizontalHeaderItem(i)
                    item.setText(room_apply_hdr_arr[i])

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QCoreApplication.translate

        if scr_control_event != "CHG": return # 수정
        if tabWidget_room_schl_arr == []: return

        self.tableWidget.clearContents()
        for i in range(len(tabWidget_room_schl_arr)):
            self.tableWidget.removeRow(i)
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            days_info = ""
            for j in range(len(tabWidget_room_schl_arr[i])):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(i, j, item)
                item = self.tableWidget.item(i, j)
                if j in (2, 3):
                   item.setText(tabWidget_room_schl_arr[i][j].split(": ")[1])
                   continue
                item.setText(tabWidget_room_schl_arr[i][j])

    def addMember(self):
        if self.nameLE.text() != " " and self.fld1_LE.text() != "":
            self.idLabel.setText(clickedRcdInfo[0] + str(df_super_list[1][11]))

    def refreshInfo(self):
        self.close()
        self.__init__()
        self.exec_()

    def accept(self):
        if self.nameLE.text() == " " or self.fld1_LE.text() == "":
            global_funtion().message_box_1(QMessageBox.Warning, "경고", "필수 정보를 입력해주세요.", "확인")
            return
        if self.idLabel.text() == " ":
            global_funtion().message_box_1(QMessageBox.Warning, "경고", "ID를 생성해주세요.", "확인")
            return

        BB_create_arr = [clickedRcdInfo[0], int(self.idLabel.text()[2:7]), self.nameLE.text(), self.fld1_LE.text(), self.comboBox1.currentIndex() + 1,
                         self.fld2_LE.text(), self.fld3_LE.text(), self.fld4_LE.text(), self.remark1LE.text(), "", "", "", "", "", "", ""
                         ]

        if self.checkBox.isChecked() == True:
            BB_create_arr[11] = "x"
        if scr_control_event == "CRT":
            BB_create_arr[12] = datetime.today()
            BB_create_arr[13] = "admin"
            df_super_list[1][11] = df_super_list[1][11] + 1
            df = pd.DataFrame(df_super_list, columns=df_super_col)
            df.to_excel('table/super_master.xlsx', index=False)
        else:
            for i in range(len(BB_master_list)):
                if BB_master_list[i][1] == int(self.idLabel.text()[2:7]):
                    BB_create_arr[1] = BB_master_list[i][1]
                    BB_create_arr[12] = BB_master_list[i][12]
                    BB_create_arr[13] = BB_master_list[i][13]
                    BB_master_list.__delitem__(i)
                    BB_create_arr[14] = datetime.today()
                    BB_create_arr[15] = "admin"

                    continue
        BB_master_list.append(BB_create_arr)
        list.sort(BB_master_list, key=lambda k: k[1])
        df = pd.DataFrame(BB_master_list, columns=BB_master_list_col)
        df.to_excel('table/BB_room_master_data.xlsx', index=False)
        global_funtion().message_box_1(QMessageBox.Information, "정보", "저장되었습니다", "확인")

        self.close()

class Ui_Lesson_Master_Mgmt(QDialog):
    def __init__(self):
        super().__init__()
        self.get_Init_data()
        self.setupUi()

    def get_Init_data(self):
        global scr_control_event, win_header_title, master_type, master_ID

        master_type = clickedRcdInfo[0]
        master_ID = clickedRcdInfo[0] + str(clickedRcdInfo[1])

        scr_control_event = "CRT"           # 생성
        win_header_title = "강좌 등록"
        if str(clickedRcdInfo[1]) != "":
            scr_control_event = "CHG"       # 수정
            win_header_title = "강좌 정보수정"

        self.get_tabWidget_data()

    def get_tabWidget_data(self):
        global tabWidget_less_schl_arr
        tabWidget_less_schl_arr = []
        for i in range(len(df_lesson_schedule_list)):
            lesson_schedule_arr = []
            if df_lesson_schedule_list[i][0] != Selected_season_ID: continue
            if df_lesson_schedule_list[i][3] != master_ID: continue
            lesson_schedule_arr.append(df_lesson_schedule_list[i][4])                #그룹 키
            for j in range(len(BB_master_list)):         #강의실
                if BB_master_list[j][1] != int(df_lesson_schedule_list[i][5][2:]): continue
                lesson_schedule_arr.append(df_lesson_schedule_list[i][5] + ": " + BB_master_list[j][2])
                break
            for j in range(len(time_period_arr)):           #시즌별 시간
                if time_period_arr[j][1] != df_lesson_schedule_list[i][6]: continue  #시간 ID
                lesson_schedule_arr.append(str(time_period_arr[j][1]) + " (교시): " + time_period_arr[j][2])
                break
            for k in range(0,13):
                lesson_schedule_arr.append(df_lesson_schedule_list[i][k+7])        #df_lesson_schedule_list[i][5] : 요일 ID
            tabWidget_less_schl_arr.append(lesson_schedule_arr)


    def setupUi(self):
        self.setWindowTitle("기준정보")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        self.buttonBox = QDialogButtonBox(self)
        if scr_control_event == "CRT":
            self.setFixedSize(490, 460)
            global_funtion().final_decision_button_box(self.buttonBox, 130, 410, 340, 30, "저장", "나가기",
                                                       self.accept, self.reject)
            # self.buttonBox.accepted.connect(Ui_MainWindow().refreshInfo())
        else:
            self.setFixedSize(490, 660)
            global_funtion().final_decision_button_box(self.buttonBox, 130, 605, 340, 30, "저장", "나가기",
                                                       self.accept, self.reject)

        self.label = QLabel(self)
        self.label.setGeometry(QRect(0, 20, 490, 40))
        self.label.setFrameShadow(QFrame.Sunken)
        self.label.setLineWidth(1)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText(win_header_title)
        global_funtion().fontSetting(self.label, '6B', 24, " ")  # "에스코어 드림 6 Bold", PointSize(24)

        self.gridLayoutWidget = QWidget(self)
        self.gridLayoutWidget.setGeometry(QRect(20, 70, 450, 320))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(10, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setObjectName("gridLayout")

        for i in range(0, 10):
            self.label = QLabel(self.gridLayoutWidget)
            item_title = CC_master_list_col[i + 1]
            if i == 1 or i == 2:
                item_title += "(필수)"
            elif i == 3:
                item_title = " "
            elif i > 3:
                item_title = CC_master_list_col[i]
            self.label.setText(item_title)
            global_funtion().fontSetting(self.label, '6B', 10, " ")
            self.gridLayout.addWidget(self.label, i, 0, 1, 1)

        self.groupBox = QGroupBox(self.gridLayoutWidget)
        self.groupBox.setMaximumSize(QSize(16777215, 25))
        self.groupBox.setStyleSheet("border : 0")
        self.idLabel = QLabel(self.groupBox)
        self.idLabel.setGeometry(QRect(0, 5, 65, 15))
        if scr_control_event == "CRT":
            self.idLabel.setText(str(clickedRcdInfo[1]))
        else:
            self.idLabel.setText(master_ID)     # ID
        if scr_control_event == "CRT":
            tool_button_arr = ["ID 생성(필수정보 입력필)", 280, 0, 25, 25, "img/add_person.png", 25, 25, self.addMember]

        else:
            tool_button_arr = ["최신정보 갱신", 280, 0, 25, 25, "img/refresh.png", 25, 25, self.refreshInfo]
        self.toolButton = QToolButton(self.groupBox)
        global_funtion().tool_button_setting(self.toolButton, tool_button_arr)
        self.gridLayout.addWidget(self.groupBox, 0, 1, 1, 1)

        self.nameLE = QLineEdit(self.gridLayoutWidget)    #강좌명1
        self.nameLE.setText(str(clickedRcdInfo[2]))
        self.gridLayout.addWidget(self.nameLE, 1, 1, 1, 1)

        self.fld1_LE = QLineEdit(self.gridLayoutWidget)  #최대인원
        self.fld1_LE.setText(str(clickedRcdInfo[3]))
        self.fld1_LE.setValidator(QRegExpValidator(QRegExp("[0-9]{3}")))
        self.fld1_LE.setPlaceholderText("3자리 이하")  # 입력 가이드 (ddd)
        self.gridLayout.addWidget(self.fld1_LE, 2, 1, 1, 1)

        self.groupBox = QGroupBox(self.gridLayoutWidget)
        self.groupBox.setMaximumSize(QSize(16777215, 30))

        self.line = QFrame(self.groupBox)
        self.line.setGeometry(QRect(160, 0, 20, 30))
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.checkBox = QCheckBox(self.groupBox)
        self.checkBox.setText("활성")
        if scr_control_event == "CRT":                   # scr_control_event이 Blank이면 생성화면을 의미, 아니면 수정화면
            self.checkBox.setChecked(True)
            self.checkBox.setEnabled(False)
        else:
            if clickedRcdInfo[11] == "x":
                self.checkBox.setChecked(True)
            else:
                self.checkBox.setChecked(False)
        self.checkBox.setGeometry(QRect(220, 5, 60, 20))
        self.gridLayout.addWidget(self.groupBox, 3, 1, 1, 1)

        comboBox_arr = ["영어", "수학", "국어", "과학", "기타"]
        self.comboBox1 = QComboBox(self.gridLayoutWidget)
        self.comboBox1.addItems(comboBox_arr)
        self.gridLayout.addWidget(self.comboBox1, 4, 1, 1, 1)

        self.fld2_DE = QDateEdit(self.gridLayoutWidget)  #시작일
        self.fld2_DE.setDate(Selected_season_SDate)
        self.fld2_DE.setCalendarPopup(True)
        self.gridLayout.addWidget(self.fld2_DE, 5, 1, 1, 1)

        self.fld3_DE = QDateEdit(self.gridLayoutWidget) #종료일
        self.fld3_DE.setDate(Selected_season_EDate)
        self.fld3_DE.setCalendarPopup(True)
        self.gridLayout.addWidget(self.fld3_DE, 6, 1, 1, 1)

        self.fld4_LE = QLineEdit(self.gridLayoutWidget) #비고2
        self.fld4_LE.setText(clickedRcdInfo[7])
        self.gridLayout.addWidget(self.fld4_LE, 7, 1, 1, 1)

        self.remark1LE = QLineEdit(self.gridLayoutWidget) #비고3
        self.remark1LE.setText(clickedRcdInfo[8])
        self.gridLayout.addWidget(self.remark1LE, 8, 1, 1, 1)

        self.remark2LE = QLineEdit(self.gridLayoutWidget) #비고4
        self.remark2LE.setText(clickedRcdInfo[10])
        self.gridLayout.addWidget(self.remark2LE, 9, 1, 1, 1)

        if scr_control_event == "CHG":       # 수정
            lesson_apply_hdr_arr = ["강의실", "시간", "요일"]
            self.tableWidget = QTableWidget(self)
            self.tableWidget.setGeometry(QRect(20, 430, 450, 150))
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 전체 cell read-only
            self.tableWidget.verticalHeader().setVisible(False)  # index 안보이는 기능

            if tabWidget_less_schl_arr != []:
                self.tableWidget.setColumnCount(len(lesson_apply_hdr_arr))
                self.tableWidget.setRowCount(0)

                header = self.tableWidget.horizontalHeader()
                header.setSectionResizeMode(QHeaderView.ResizeToContents)
                # header.setSectionResizeMode(QHeaderView.Stretch)
                header.setStyleSheet("::section {""background-color: lightgray;""}")  # TableWidget내 헤더 Title의 배경색은 일반적으로 달리 이렇게 지정함
                for i in range(len(lesson_apply_hdr_arr)):
                    item = QTableWidgetItem()
                    self.tableWidget.setHorizontalHeaderItem(i, item)
                    item = self.tableWidget.horizontalHeaderItem(i)
                    item.setText(lesson_apply_hdr_arr[i])

            table_title = "강좌/강의실 등록"
            self.label = QLabel(self)
            self.label.setGeometry(QRect(20, 400, 180, 20))
            self.label.setText(table_title)
            global_funtion().fontSetting(self.label, '6B', 11, " ")   # "에스코어 드림 6 Bold", PointSize(11)

            tool_button_arr = ["강의실/시간관리", 20, 600, 30, 30, "img/edit.png", 30, 30, self.addInfo]
            self.toolButton = QToolButton(self)
            global_funtion().tool_button_setting(self.toolButton, tool_button_arr)


        self.retranslateUi()

    def retranslateUi(self):
        _translate = QCoreApplication.translate

        if scr_control_event == "CRT": return #강좌등록
        if tabWidget_less_schl_arr == []: return

        old_group_key = ""
        x = 0
        self.tableWidget.clearContents()
        print(tabWidget_less_schl_arr)
        for i in range(len(tabWidget_less_schl_arr)):
            self.tableWidget.removeRow(i)
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            if tabWidget_less_schl_arr[i][0] != " ":
               if old_group_key != "" and  old_group_key != tabWidget_less_schl_arr[i][0]: x += 1
            week_str = []
            for j in range(len(tabWidget_less_schl_arr[i])):
                if j in (0, 3): continue            #그룹 Key, 요일 ID
                if j == 11: break              #생성일자
                if j < 3:
                    item = QTableWidgetItem()
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget.setItem(i, j-1, item)
                    item = self.tableWidget.item(i, j-1)
                    if tabWidget_less_schl_arr[i][0] != " ":
                        item.setBackground(QColor(bg_color_arr[x%5]))
                    item.setText(tabWidget_less_schl_arr[i][j])
                    continue
                if j >= 4:
                    week_arr = ['월', '화', '수', '목', '금', '토', '일']

                    if tabWidget_less_schl_arr[i][j] == "X":
                        week_str.append(week_arr[j-4])
                    if j < 10:
                        continue
                    if j == 10:
                        if len(week_str) == 1:
                            week_ap = week_str[0]
                        else:
                            week_ap = ", ".join(week_str)
                    item = QTableWidgetItem()
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tableWidget.setItem(i, j-8, item)
                    item = self.tableWidget.item(i, j-8)
                    item.setText(week_ap)
            old_group_key = tabWidget_less_schl_arr[i][0]

    def addMember(self):
        if self.nameLE.text() != " " and self.fld1_LE.text() != "":
            self.idLabel.setText(clickedRcdInfo[0] + str(df_super_list[2][11]))

    def addInfo(self):
        global selected_info
        selected_info = [self.idLabel.text(), self.nameLE.text(), " "]
        win = Ui_Lesson_Schedule()
        win.exec_()

    def refreshInfo(self):
        self.close()
        self.__init__()
        self.get_tabWidget_data()
        self.exec_()

    def accept(self):
        if self.nameLE.text() == " " or self.fld1_LE.text() == "":
            global_funtion().message_box_1(QMessageBox.Warning, "경고", "필수 정보를 입력해주세요.", "확인")
            return
        if self.idLabel.text() == " ":
            global_funtion().message_box_1(QMessageBox.Warning, "경고", "ID를 생성해주세요.", "확인")
            return

        CC_create_arr = [clickedRcdInfo[0], int(self.idLabel.text()[2:7]), self.nameLE.text(), self.fld1_LE.text(), self.comboBox1.currentText(),
                         self.fld2_DE.text(), self.fld3_DE.text(), self.fld4_LE.text(), self.remark1LE.text(),
                         self.remark2LE.text(), "", "", "", "", "", ""]

        if self.checkBox.isChecked() == True:
            CC_create_arr[11] = "x"
        if scr_control_event == "CRT":
            CC_create_arr[12] = datetime.today()
            CC_create_arr[13] = "admin"
            df_super_list[2][11] = df_super_list[2][11] + 1
            df = pd.DataFrame(df_super_list, columns=df_super_col)
            df.to_excel('table/super_master.xlsx', index=False)
        else:
            for i in range(len(CC_master_list)):
                if CC_master_list[i][1] == int(self.idLabel.text()[2:7]):
                    CC_create_arr[1] = CC_master_list[i][1]
                    CC_create_arr[12] = CC_master_list[i][12]
                    CC_create_arr[13] = CC_master_list[i][13]
                    CC_master_list.__delitem__(i)
                    CC_create_arr[14] = datetime.today()
                    CC_create_arr[15] = "admin"

                    continue
        CC_master_list.append(CC_create_arr)
        list.sort(CC_master_list, key=lambda k: k[1])
        df = pd.DataFrame(CC_master_list, columns=CC_master_list_col)
        df.to_excel('table/CC_lesson_master_data.xlsx', index=False)
        global_funtion().message_box_1(QMessageBox.Information, "정보", "저장되었습니다", "확인")

        self.close()

class Ui_Teacher_Master_Mgmt(QDialog):
    def __init__(self):
        super().__init__()
        self.get_Init_data()
        self.setupUi()

    def get_Init_data(self):
        global scr_control_event, win_header_title, master_type, master_ID, tabWidget_time_info_arr
        global comboBox_season_arr, season_active_idx

        master_type = clickedRcdInfo[0]
        master_ID = clickedRcdInfo[0] + str(clickedRcdInfo[1])

        scr_control_event = "CRT"           # 생성
        win_header_title = "강사 등록"
        if str(clickedRcdInfo[1]) != "":
            scr_control_event = "CHG"       # 수정
            win_header_title = "강사 정보수정"

        self.get_tabWidget_data()

    def get_tabWidget_data(self):
        global tabWidget_teach_less_arr
        tabWidget_teach_less_arr = []
        # tabWidget_teach_less_arr = ["강좌ID : 강좌이름", "강의실ID : 강의실이름", "교시: 시간내용", "요일ID", "요일Text", "시작일",
        # "종료일", 생성일, 생성자, 변경일, 변경자]
        for i in range(len(df_teacher_lesson_list)):
            lesson_idx = ""
            teach_lesson_arr = []
            lesson_idx_arr = []
            if df_teacher_lesson_list[i][0] != Selected_season_ID: continue
            if df_teacher_lesson_list[i][1] != master_ID: continue
            for j in range(len(df_lesson_schedule_list)):
                if df_lesson_schedule_list[j][1] == df_teacher_lesson_list[i][2]:
                    lesson_idx = j
                    lesson_idx_arr.append(lesson_idx)
            for z in range(len(lesson_idx_arr)):
                if lesson_idx == "": continue

                teach_lesson_arr.append(df_lesson_schedule_list[lesson_idx_arr[z]][3] + ": " + CC_dictionary[df_lesson_schedule_list[lesson_idx_arr[z]][3]])    #강좌
                teach_lesson_arr.append(df_lesson_schedule_list[lesson_idx_arr[z]][5] + ": " + BB_dictionary[df_lesson_schedule_list[lesson_idx_arr[z]][5]])    #강의실
                # teach_lesson_arr.append(str(df_teacher_lesson_list[i][5]) + " (교시)")                      #시간
                for j in range(len(days_text_info_arr)):                                                   #요일ID, 요일 Text
                    if df_lesson_schedule_list[lesson_idx_arr[z]][4] == " ":
                        if days_text_info_arr[j][3] != df_lesson_schedule_list[lesson_idx_arr[z]][6]: continue  # 시간 ID
                        if days_text_info_arr[j][4] != df_lesson_schedule_list[lesson_idx_arr[z]][7]: continue  # 요일 ID
                    if days_text_info_arr[j][0] != df_lesson_schedule_list[lesson_idx_arr[z]][3]: continue    #강좌
                    if days_text_info_arr[j][1] != df_lesson_schedule_list[lesson_idx_arr[z]][4]: continue    #그룹 키
                    if days_text_info_arr[j][2] != df_lesson_schedule_list[lesson_idx_arr[z]][5]: continue    #강의실 ID

                    teach_lesson_arr.append(str(df_lesson_schedule_list[lesson_idx_arr[z]][6]) + " (교시): " + days_text_info_arr[j][6]) # 시간
                    teach_lesson_arr.append(days_text_info_arr[j][4])                        #요일 ID
                    teach_lesson_arr.append(days_text_info_arr[j][5])                        #요일 Text
                    break
                for k in range(3, 9):                                #시작일, 종료일, 생성일, 생성자, 변경일, 변경자
                    teach_lesson_arr.append(df_teacher_lesson_list[i][k])
                teach_lesson_arr.append(df_lesson_schedule_list[lesson_idx_arr[z]][4])   #그룹키
                teach_lesson_arr.append(df_teacher_lesson_list[i][2])   #레슨키
                tabWidget_teach_less_arr.append(teach_lesson_arr)


    def setupUi(self):
        self.setWindowTitle("기준정보")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        self.buttonBox = QDialogButtonBox(self)
        if scr_control_event == "CRT":
            self.setFixedSize(490, 460)
            global_funtion().final_decision_button_box(self.buttonBox, 130, 410, 340, 30, "저장", "나가기",
                                                       self.accept, self.reject)
        else:
            self.setFixedSize(490, 660)
            global_funtion().final_decision_button_box(self.buttonBox, 130, 605, 340, 30, "저장", "나가기",
                                                       self.accept, self.reject)

        self.label = QLabel(self)
        self.label.setGeometry(QRect(0, 20, 490, 40))
        self.label.setFrameShadow(QFrame.Sunken)
        self.label.setLineWidth(1)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText(win_header_title)
        global_funtion().fontSetting(self.label, '6B', 24, " ")  # "에스코어 드림 6 Bold", PointSize(24)

        self.gridLayoutWidget = QWidget(self)
        self.gridLayoutWidget.setGeometry(QRect(20, 70, 450, 320))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(10, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setObjectName("gridLayout")
        for i in range(0,10):
            self.label = QLabel(self.gridLayoutWidget)
            item_title = DD_master_list_col[i+1]
            if i == 1 or i == 2:
                item_title += "(필수)"
            self.label.setText(item_title)
            global_funtion().fontSetting(self.label, '6B', 10, " ")
            self.gridLayout.addWidget(self.label, i, 0, 1, 1)

        self.groupBox = QGroupBox(self.gridLayoutWidget)
        self.groupBox.setMaximumSize(QSize(16777215, 25))
        self.groupBox.setStyleSheet("border : 0")
        self.idLabel = QLabel(self.groupBox)
        self.idLabel.setGeometry(QRect(0, 5, 80, 15))
        if scr_control_event == "CRT":
            self.idLabel.setText(str(clickedRcdInfo[1]))
        else:
            self.idLabel.setText(master_ID)     # ID
        if scr_control_event == "CRT":
            tool_button_arr = ["ID 생성(필수정보 입력필)", 280, 0, 25, 25, "img/add_person.png", 25, 25, self.addMember]

        else:
            tool_button_arr = ["최신정보 갱신", 280, 0, 25, 25, "img/refresh.png", 25, 25, self.refreshInfo]
        self.toolButton = QToolButton(self.groupBox)
        global_funtion().tool_button_setting(self.toolButton, tool_button_arr)
        self.gridLayout.addWidget(self.groupBox, 0, 1, 1, 1)

        self.nameLE = QLineEdit(self.gridLayoutWidget)    #이름
        self.nameLE.setText(str(clickedRcdInfo[2]))
        self.gridLayout.addWidget(self.nameLE, 1, 1, 1, 1)

        self.fld1_LE = QLineEdit(self.gridLayoutWidget)  #연락처
        self.fld1_LE.setText(str(clickedRcdInfo[3]))
        self.fld1_LE.setValidator(QRegExpValidator(QRegExp("[0-9]{3}-[0-9]{4}-[0-9]{3}")))
        self.fld1_LE.setPlaceholderText("ddd-dddd-ddd")  # 입력 가이드 (ddd-dddd-ddd)
        self.gridLayout.addWidget(self.fld1_LE, 2, 1, 1, 1)

        self.groupBox = QGroupBox(self.gridLayoutWidget)
        self.groupBox.setMaximumSize(QSize(16777215, 30))

        global gender_arr
        gender_arr = [["남", 20, 5, 50, 20], ["여", 100, 5, 50, 20]]

        for i in range(len(gender_arr)):
            self.radioButton = QRadioButton(self.groupBox)
            self.radioButton.setText(gender_arr[i][0])
            self.radioButton.setGeometry(QRect(gender_arr[i][1],gender_arr[i][2],gender_arr[i][3],gender_arr[i][4]))
            if scr_control_event == "":               # scr_control_event이 Blank이면 생성화면을 의미, 아니면 수정화면
                if i == 0:  self.radioButton.setChecked(True)
            else:
                if gender_arr[i][0] == clickedRcdInfo[4]:
                   self.radioButton.setChecked(True)

        self.line = QFrame(self.groupBox)
        self.line.setGeometry(QRect(160, 0, 20, 30))
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.checkBox = QCheckBox(self.groupBox)
        self.checkBox.setText("활성")
        if scr_control_event == "CRT":  # scr_control_event이 Blank이면 생성화면을 의미, 아니면 수정화면
            self.checkBox.setChecked(True)
            self.checkBox.setEnabled(False)
        else:
            if clickedRcdInfo[11] == "x":
                self.checkBox.setChecked(True)
            else:
                self.checkBox.setChecked(False)
        self.checkBox.setGeometry(QRect(220, 5, 60, 20))
        self.gridLayout.addWidget(self.groupBox, 3, 1, 1, 1)

        comboBox_arr = ["대졸", "석사졸", "박사졸", "대재", "고졸"]
        self.comboBox1 = QComboBox(self.gridLayoutWidget)
        self.comboBox1.addItems(comboBox_arr)
        self.gridLayout.addWidget(self.comboBox1, 4, 1, 1, 1)

        self.fld2_LE = QLineEdit(self.gridLayoutWidget) #최종학교
        self.fld2_LE.setText(clickedRcdInfo[6])
        self.gridLayout.addWidget(self.fld2_LE, 5, 1, 1, 1)

        major_arr = ["국어", "수학", "영어", "과학", "기타"]
        self.remark1LE = QComboBox(self.gridLayoutWidget)  # 주전공
        self.remark1LE.addItems(major_arr)
        self.gridLayout.addWidget(self.remark1LE, 6, 1, 1, 1)

        self.remark2LE = QComboBox(self.gridLayoutWidget)  # 부전공
        self.remark2LE.addItems(major_arr)
        self.gridLayout.addWidget(self.remark2LE, 7, 1, 1, 1)

        self.fld3_LE = QLineEdit(self.gridLayoutWidget) #생년월일
        self.fld3_LE.setText(clickedRcdInfo[9])
        self.fld3_LE.setValidator(QRegExpValidator(QRegExp("[0-9]{4}-[0-9]{2}-[0-9]{2}")))
        self.fld3_LE.setPlaceholderText("YYYY-MM-DD")                   # 입력 가이드 (yyyyMMdd)
        self.gridLayout.addWidget(self.fld3_LE, 8, 1, 1, 1)

        self.fld4_LE = QLineEdit(self.gridLayoutWidget) #강사: 주소
        self.fld4_LE.setText(clickedRcdInfo[10])
        self.gridLayout.addWidget(self.fld4_LE, 9, 1, 1, 1)

        if scr_control_event == "CHG":  #수정
            table_title = "강사/강좌 정보"
            self.label = QLabel(self)
            self.label.setGeometry(QRect(20, 400, 150, 20))
            self.label.setText(table_title)
            global_funtion().fontSetting(self.label, '6B', 11, " ")  # "에스코어 드림 6 Bold", PointSize(11)

            lesson_apply_hdr_arr = ["강좌", "강의실", "시간", "요일", "시작일", "종료일"]
            self.tableWidget = QTableWidget(self)
            self.tableWidget.setGeometry(QRect(20, 430, 450, 160))
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 전체 cell read-only
            self.tableWidget.verticalHeader().setVisible(False)  # index 안보이는 기능

            if tabWidget_teach_less_arr != []:
                self.tableWidget.setColumnCount(len(lesson_apply_hdr_arr))
                self.tableWidget.setRowCount(0)

                header = self.tableWidget.horizontalHeader()
                header.setSectionResizeMode(QHeaderView.ResizeToContents)
                # header.setSectionResizeMode(QHeaderView.Stretch)
                header.setStyleSheet("::section {""background-color: lightgray;""}")  # TableWidget내 헤더 Title의 배경색은 일반적으로 달리 이렇게 지정함
                for i in range(len(lesson_apply_hdr_arr)):
                    item = QTableWidgetItem()
                    self.tableWidget.setHorizontalHeaderItem(i, item)
                    item = self.tableWidget.horizontalHeaderItem(i)
                    item.setText(lesson_apply_hdr_arr[i])

            tool_button_arr = ["강좌관리", 20, 600, 30, 30, "img/edit.png", 30, 30, self.addInfo]
            self.toolButton = QToolButton(self)
            global_funtion().tool_button_setting(self.toolButton, tool_button_arr)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QCoreApplication.translate

        if scr_control_event != "CHG":  return #수정
        if tabWidget_teach_less_arr == []: return

        old_group_key = ""
        x = 0
        self.tableWidget.clearContents()
        for i in range(len(tabWidget_teach_less_arr)):
            self.tableWidget.removeRow(i)
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            if tabWidget_teach_less_arr[i][11] != " ":
                 if old_group_key != "" and old_group_key != tabWidget_teach_less_arr[i][11]: x += 1
            for j in range(len(tabWidget_teach_less_arr[i])):
                k = j
                if j >= 4: k = j - 1
                if j == 3: continue
                if j == 7: break
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(i, k, item)
                item = self.tableWidget.item(i, k)
                if j <= 4 and tabWidget_teach_less_arr[i][11] != " ":
                   item.setBackground(QColor(bg_color_arr[x%5]))
                if j in (0, 1):
                   item.setText(tabWidget_teach_less_arr[i][j].split(": ")[1])
                else:
                   item.setText(tabWidget_teach_less_arr[i][j])
            old_group_key = tabWidget_teach_less_arr[i][11]

    def addMember(self):
        if self.nameLE.text() != " " and self.fld1_LE.text() != "":
            self.idLabel.setText(clickedRcdInfo[0] + str(df_super_list[3][11]))

    def addInfo(self):
        global selected_info
        selected_info = [self.idLabel.text(), self.nameLE.text()]
        win = Ui_Teacher_Lesson_Assign()
        win.exec_()

    def refreshInfo(self):
        self.close()
        self.get_tabWidget_data()
        self.__init__()
        self.exec_()

    def accept(self):
        if self.nameLE.text() == " " or self.fld1_LE.text() == "":
            global_funtion().message_box_1(QMessageBox.Warning, "경고", "필수 정보를 입력해주세요.", "확인")
            return
        if self.idLabel.text() == " ":
            global_funtion().message_box_1(QMessageBox.Warning, "경고", "ID를 생성해주세요.", "확인")
            return
        if self.radioButton.isChecked() == True:
            gender = gender_arr[1][0]
        else:
            gender = gender_arr[0][0]

        DD_create_arr = [clickedRcdInfo[0], int(self.idLabel.text()[2:7]), self.nameLE.text(), self.fld1_LE.text(),
                         gender, self.comboBox1.currentText(),
                         self.fld2_LE.text(), str(self.remark1LE.currentText()), str(self.remark2LE.currentText()),
                         self.fld3_LE.text(), self.fld4_LE.text(), "", "", "", "", ""]

        if self.checkBox.isChecked() == True:
            DD_create_arr[11] = "x"
        if scr_control_event == "CRT":
            DD_create_arr[12] = datetime.today()
            DD_create_arr[13] = "admin"
            df_super_list[0][11] = df_super_list[0][11] + 1
            df = pd.DataFrame(df_super_list, columns=df_super_col)
            df.to_excel('table/super_master.xlsx', index=False)
        else:
            for i in range(len(DD_master_list)):
                if DD_master_list[i][1] == int(self.idLabel.text()[2:7]):
                    DD_create_arr[1] = DD_master_list[i][1]
                    DD_create_arr[12] = DD_master_list[i][12]
                    DD_create_arr[13] = DD_master_list[i][13]
                    DD_master_list.__delitem__(i)
                    DD_create_arr[14] = datetime.today()
                    DD_create_arr[15] = "admin"
                    continue
        DD_master_list.append(DD_create_arr)
        list.sort(DD_master_list, key=lambda k: k[1])
        df = pd.DataFrame(DD_master_list, columns=DD_master_list_col)
        df.to_excel('table/DD_teacher_master_data.xlsx', index=False)
        global_funtion().message_box_1(QMessageBox.Information, "정보", "저장되었습니다", "확인")

        self.close()

class Ui_Student_Master_Mgmt(QDialog):
    def __init__(self):
        super().__init__()
        self.get_Init_data()
        self.setupUi()

    def get_Init_data(self):
        global scr_control_event, win_header_title, master_type, master_ID, tabWidget_time_info_arr

        master_type = clickedRcdInfo[0]
        master_ID = clickedRcdInfo[0] + str(clickedRcdInfo[1])

        scr_control_event = "CRT"           # 생성
        win_header_title = "수강생 등록"
        if str(clickedRcdInfo[1]) != "":
            scr_control_event = "CHG"       # 수정
            win_header_title = "수강생 정보수정"

        self.get_tabWidget_data()

    def get_tabWidget_data(self):
        global tabWidget_stud_less_arr
        tabWidget_stud_less_arr = []
        for i in range(len(df_student_lesson_list)):
            lesson_idx = ""
            stud_lesson_arr = []
            lesson_idx_arr = []
            if df_student_lesson_list[i][0] != Selected_season_ID: continue
            if df_student_lesson_list[i][1] != master_ID: continue
            for j in range(len(df_lesson_schedule_list)):
                if df_lesson_schedule_list[j][1] == df_student_lesson_list[i][2]:
                    lesson_idx = j
                    lesson_idx_arr.append(lesson_idx)
            for z in range(len(lesson_idx_arr)):
                if lesson_idx == "": continue
                for k in range(len(df_teacher_lesson_list)):
                    if df_teacher_lesson_list[k][2] == df_lesson_schedule_list[lesson_idx_arr[z]][1]:
                        teacher_id = df_teacher_lesson_list[k][1]
                        break
                stud_lesson_arr.append(df_lesson_schedule_list[lesson_idx_arr[z]][3] + ": " + \
                                       CC_dictionary[df_lesson_schedule_list[lesson_idx_arr[z]][3]])  # 강좌
                stud_lesson_arr.append(teacher_id + ": " + DD_dictionary[teacher_id])  # 강사
                stud_lesson_arr.append(df_lesson_schedule_list[lesson_idx_arr[z]][5] + ": " + \
                                       BB_dictionary[df_lesson_schedule_list[lesson_idx_arr[z]][5]])  # 강의실
                # teach_lesson_arr.append(str(df_teacher_lesson_list[i][5]) + " (교시)")                      #시간
                for j in range(len(days_text_info_arr)):  # 요일ID, 요일 Text
                    if df_lesson_schedule_list[lesson_idx_arr[z]][4] == " ":
                        if days_text_info_arr[j][3] != df_lesson_schedule_list[lesson_idx_arr[z]][6]: continue  # 시간 ID
                        if days_text_info_arr[j][4] != df_lesson_schedule_list[lesson_idx_arr[z]][7]: continue  # 요일 ID
                    if days_text_info_arr[j][0] != df_lesson_schedule_list[lesson_idx_arr[z]][3]: continue  # 강좌
                    if days_text_info_arr[j][1] != df_lesson_schedule_list[lesson_idx_arr[z]][4]: continue  # 그룹 키
                    if days_text_info_arr[j][2] != df_lesson_schedule_list[lesson_idx_arr[z]][5]: continue  # 강의실 ID
                    stud_lesson_arr.append(str(df_lesson_schedule_list[lesson_idx_arr[z]][6]) + " (교시): " + days_text_info_arr[j][6])
                    stud_lesson_arr.append(days_text_info_arr[j][4])                        #요일 ID
                    stud_lesson_arr.append(days_text_info_arr[j][5])                        #요일 Text
                    break
                for k in range(3, 9):                                #시작일, 종료일, 생성일, 생성자, 변경일, 변경자
                    stud_lesson_arr.append(df_student_lesson_list[i][k])
                stud_lesson_arr.append(df_lesson_schedule_list[lesson_idx_arr[z]][4])  # 그룹 키
                stud_lesson_arr.append(df_student_lesson_list[i][2])
                tabWidget_stud_less_arr.append(stud_lesson_arr)

    def setupUi(self):
        self.setWindowTitle("기준정보")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        self.buttonBox = QDialogButtonBox(self)
        if scr_control_event == "CRT":
            self.setFixedSize(490, 460)
            global_funtion().final_decision_button_box(self.buttonBox, 130, 410, 340, 30, "저장", "나가기",
                                                       self.accept, self.reject)
        else:
            self.setFixedSize(490, 660)
            global_funtion().final_decision_button_box(self.buttonBox, 130, 605, 340, 30, "저장", "나가기",
                                                       self.accept, self.reject)

        # # Main Screen에 있는 Tool Button 정의
        # tool_button_arr = [["최신정보 갱신", 450, 20, 40, 40, "img/refresh.png", 40, 40, self.refreshInfo]]
        # for i in range(len(tool_button_arr)):
        #     self.toolButton = QToolButton(self)
        #     global_funtion().tool_button_setting(self.toolButton, tool_button_arr[i])

        self.label = QLabel(self)
        self.label.setGeometry(QRect(0, 20, 490, 40))
        self.label.setFrameShadow(QFrame.Sunken)
        self.label.setLineWidth(1)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText(win_header_title)
        global_funtion().fontSetting(self.label, '6B', 24, " ")  # "에스코어 드림 6 Bold", PointSize(24)

        self.gridLayoutWidget = QWidget(self)
        self.gridLayoutWidget.setGeometry(QRect(20, 70, 450, 320))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(10, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(20)

        for i in range(0, 10):
            self.label = QLabel(self.gridLayoutWidget)
            item_title = EE_master_list_col[i + 1]
            if i == 1 or i == 2:
                item_title += "(필수)"
            self.label.setText(item_title)
            global_funtion().fontSetting(self.label, '6B', 10, " ")
            self.gridLayout.addWidget(self.label, i, 0, 1, 1)

        self.groupBox = QGroupBox(self.gridLayoutWidget)
        self.groupBox.setMaximumSize(QSize(16777215, 25))
        self.groupBox.setStyleSheet("border : 0")
        self.idLabel = QLabel(self.groupBox)
        self.idLabel.setGeometry(QRect(0, 5, 80, 15))
        if scr_control_event == "CRT":
            self.idLabel.setText(str(clickedRcdInfo[1]))
        else:
            self.idLabel.setText(master_ID)     # ID
        if scr_control_event == "CRT":
            tool_button_arr = ["ID 생성(필수정보 입력필)", 280, 0, 25, 25, "img/add_person.png", 25, 25, self.addMember]

        else:
            tool_button_arr = ["최신정보 갱신", 280, 0, 25, 25, "img/refresh.png", 25, 25, self.refreshInfo]
        self.toolButton = QToolButton(self.groupBox)
        global_funtion().tool_button_setting(self.toolButton, tool_button_arr)
        self.gridLayout.addWidget(self.groupBox, 0, 1, 1, 1)

        self.nameLE = QLineEdit(self.gridLayoutWidget)    # 이름
        self.nameLE.setText(str(clickedRcdInfo[2]))
        self.gridLayout.addWidget(self.nameLE, 1, 1, 1, 1)

        self.fld1_LE = QLineEdit(self.gridLayoutWidget)   #연락처
        self.fld1_LE.setText(str(clickedRcdInfo[3]))
        self.fld1_LE.setValidator(QRegExpValidator(QRegExp("[0-9]{3}-[0-9]{4}-[0-9]{3}")))
        self.fld1_LE.setPlaceholderText("000-0000-000")  # 입력 가이드 (000-0000-000)
        self.gridLayout.addWidget(self.fld1_LE, 2, 1, 1, 1)

        self.groupBox = QGroupBox(self.gridLayoutWidget)
        self.groupBox.setMaximumSize(QSize(16777215, 30))

        global gender_arr
        gender_arr = [["남", 20, 5, 50, 20], ["여", 100, 5, 50, 20]]

        for i in range(len(gender_arr)):
            self.radioButton = QRadioButton(self.groupBox)
            self.radioButton.setText(gender_arr[i][0])
            self.radioButton.setGeometry(QRect(gender_arr[i][1],gender_arr[i][2],gender_arr[i][3],gender_arr[i][4]))
            if scr_control_event == "":               # scr_control_event이 Blank이면 생성화면을 의미, 아니면 수정화면
                if i == 0:  self.radioButton.setChecked(True)
            else:
                if gender_arr[i][0] == clickedRcdInfo[4]:
                   self.radioButton.setChecked(True)

        self.line = QFrame(self.groupBox)
        self.line.setGeometry(QRect(160, 0, 20, 30))
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.checkBox = QCheckBox(self.groupBox)
        self.checkBox.setText("활성")
        if scr_control_event == "CRT":  # scr_control_event이 Blank이면 생성화면을 의미, 아니면 수정화면
            self.checkBox.setChecked(True)
            self.checkBox.setEnabled(False)
        else:
            if clickedRcdInfo[11] == "x":
                self.checkBox.setChecked(True)
            else:
                self.checkBox.setChecked(False)
        self.checkBox.setGeometry(QRect(220, 5, 60, 20))
        self.gridLayout.addWidget(self.groupBox, 3, 1, 1, 1)

        comboBox_arr = ["학생", "직장인", "주부", "무직", "구직중"]
        self.comboBox1 = QComboBox(self.gridLayoutWidget)
        self.comboBox1.addItems(comboBox_arr)
        self.gridLayout.addWidget(self.comboBox1, 4, 1, 1, 1)

        self.fld2_LE = QLineEdit(self.gridLayoutWidget)   #작장/학교명
        self.fld2_LE.setText(clickedRcdInfo[6])
        self.gridLayout.addWidget(self.fld2_LE, 5, 1, 1, 1)

        self.fld3_LE = QLineEdit(self.gridLayoutWidget)   #생년월일
        self.fld3_LE.setText(clickedRcdInfo[7])
        self.fld3_LE.setValidator(QRegExpValidator(QRegExp("[0-9]{4}-[0-9]{2}-[0-9]{2}")))
        self.fld3_LE.setPlaceholderText("YYYY-MM-DD")  # 입력 가이드 (ddd-dddd-ddd)
        self.gridLayout.addWidget(self.fld3_LE, 6, 1, 1, 1)

        self.fld4_LE = QLineEdit(self.gridLayoutWidget)   #주소
        self.fld4_LE.setText(clickedRcdInfo[8])
        self.gridLayout.addWidget(self.fld4_LE, 7, 1, 1, 1)

        self.remark1LE = QLineEdit(self.gridLayoutWidget)  #비고1
        self.remark1LE.setText(clickedRcdInfo[9])
        self.gridLayout.addWidget(self.remark1LE, 8, 1, 1, 1)

        self.remark2LE = QLineEdit(self.gridLayoutWidget)  #비고2
        self.remark2LE.setText(clickedRcdInfo[10])
        self.gridLayout.addWidget(self.remark2LE, 9, 1, 1, 1)

        lesson_apply_hdr_arr = ["강좌", "강사", "강의실", "시간", "요일", "시작일", "종료일"]
        if scr_control_event != "CRT":
            self.tableWidget = QTableWidget(self)
            self.tableWidget.setGeometry(QRect(20, 430, 450, 150))
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 전체 cell read-only
            self.tableWidget.verticalHeader().setVisible(False)  # index 안보이는 기능

            if tabWidget_stud_less_arr != []:
                self.tableWidget.setColumnCount(len(lesson_apply_hdr_arr))
                self.tableWidget.setRowCount(0)

                header = self.tableWidget.horizontalHeader()
                header.setSectionResizeMode(QHeaderView.ResizeToContents)
                # header.setSectionResizeMode(QHeaderView.Stretch)
                header.setStyleSheet("::section {""background-color: lightgray;""}")  # TableWidget내 헤더 Title의 배경색은 일반적으로 달리 이렇게 지정함
                for i in range(len(lesson_apply_hdr_arr)):
                    item = QTableWidgetItem()
                    self.tableWidget.setHorizontalHeaderItem(i, item)
                    item = self.tableWidget.horizontalHeaderItem(i)
                    item.setText(lesson_apply_hdr_arr[i])

            table_title = "강좌 등록"
            self.label = QLabel(self)
            self.label.setGeometry(QRect(20, 400, 80, 20))
            self.label.setText(table_title)
            global_funtion().fontSetting(self.label, '6B', 11, " ")   # "에스코어 드림 6 Bold", PointSize(11)

            tool_button_arr = ["강좌관리", 20, 600, 30, 30, "img/edit.png", 30, 30, self.addInfo]
            self.toolButton = QToolButton(self)
            global_funtion().tool_button_setting(self.toolButton, tool_button_arr)

            self.retranslateUi()

    def retranslateUi(self):
        _translate = QCoreApplication.translate

        if scr_control_event != "CHG":  return #수정
        if tabWidget_stud_less_arr == []: return

        old_group_key = ""
        x = 0
        self.tableWidget.clearContents()
        for i in range(len(tabWidget_stud_less_arr)):
            self.tableWidget.removeRow(i)
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            if tabWidget_stud_less_arr[i][12] != " ":
                 if old_group_key != "" and old_group_key != tabWidget_stud_less_arr[i][12]: x += 1
            for j in range(len(tabWidget_stud_less_arr[i])):
                k = j
                if j >= 5: k = j - 1
                if j == 4: continue
                if j == 8: break
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(i, k, item)
                item = self.tableWidget.item(i, k)
                if j <= 5 and tabWidget_stud_less_arr[i][12] != " ":
                   item.setBackground(QColor(bg_color_arr[x%5]))
                if j in (0, 1, 2):
                   item.setText(tabWidget_stud_less_arr[i][j].split(": ")[1])
                else:
                   item.setText(tabWidget_stud_less_arr[i][j])
            old_group_key = tabWidget_stud_less_arr[i][12]

    def addMember(self):
        if self.nameLE.text() != " " and self.fld1_LE.text() != "":
            self.idLabel.setText(clickedRcdInfo[0] + str(df_super_list[4][11]))

    def addInfo(self):
        global selected_info
        selected_info = [self.idLabel.text(), self.nameLE.text()]
        win = Ui_Student_Lesson_Assign()
        win.exec_()

    def refreshInfo(self):
        self.close()
        self.get_tabWidget_data()
        self.__init__()
        self.exec_()

    def accept(self):
        if self.nameLE.text() == " " or self.fld1_LE.text() == "":
            global_funtion().message_box_1(QMessageBox.Warning, "경고", "필수 정보를 입력해주세요.", "확인")
            return
        if self.idLabel.text() == " ":
            global_funtion().message_box_1(QMessageBox.Warning, "경고", "ID를 생성해주세요.", "확인")
            return
        if self.radioButton.isChecked() == True:
            gender = gender_arr[1][0]
        else:
            gender = gender_arr[0][0]

        EE_create_arr = [clickedRcdInfo[0], int(self.idLabel.text()[2:7]), self.nameLE.text(), self.fld1_LE.text(),
                         gender, self.comboBox1.currentText(),
                         self.fld2_LE.text(), self.fld3_LE.text(), self.fld4_LE.text(),
                          self.remark1LE.text(), self.remark2LE.text(), "", "", "", "", ""]

        if self.checkBox.isChecked() == True:
            EE_create_arr[11] = "x"
        if scr_control_event == "CRT":
            EE_create_arr[12] = datetime.today()
            EE_create_arr[13] = "admin"
            df_super_list[4][11] = df_super_list[4][11] + 1
            df = pd.DataFrame(df_super_list, columns=df_super_col)
            df.to_excel('table/super_master.xlsx', index=False)
        else:
            for i in range(len(EE_master_list)):
                if EE_master_list[i][1] == int(self.idLabel.text()[2:7]):
                    EE_create_arr[1] = EE_master_list[i][1]
                    EE_create_arr[12] = EE_master_list[i][12]
                    EE_create_arr[13] = EE_master_list[i][13]
                    EE_master_list.__delitem__(i)
                    EE_create_arr[14] = datetime.today()
                    EE_create_arr[15] = "admin"
                    continue
        EE_master_list.append(EE_create_arr)
        list.sort(EE_master_list, key=lambda k: k[1])
        df = pd.DataFrame(EE_master_list, columns=EE_master_list_col)
        df.to_excel('table/EE_student_master_data.xlsx', index=False)
        global_funtion().message_box_1(QMessageBox.Information, "정보", "저장되었습니다", "확인")

        self.close()

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.get_Init_data()
        self.setupUi()                  # 화면 레이아웃

    def get_Init_data(self):
        global df_super, df_super_col, df_super_list, today_QDate, length_of_df_list

        df_super = pd.read_excel('table/super_master.xlsx')
        df_super.replace(np.NaN, '', inplace=True)
        df_super_col = list([col for col in df_super])
        df_super_list = df_super.values.tolist()

        today_QDate = QDate.currentDate()

        for i in range(len(df_super_list)):                   #i = 0(시즌), 1(강의실), 2(강좌), 3(강사), 4(수강생)
            file_path = 'table/' + df_super_list[i][15]
            df_super_list[i][12] = pd.read_excel(file_path)
            df_super_list[i][12].replace(np.NaN, '', inplace=True)
            df_super_list[i][13] = list([col for col in df_super_list[i][12]])
            df_super_list[i][14] = df_super_list[i][12].values.tolist()

        global AA_master_list, BB_master_list, CC_master_list, DD_master_list, EE_master_list
        global AA_master_list_col, BB_master_list_col, CC_master_list_col, DD_master_list_col, EE_master_list_col
        AA_master_list = df_super_list[0][14]                #AA: 시즌
        BB_master_list = df_super_list[1][14]                #BB: 강의실
        CC_master_list = df_super_list[2][14]                #CC: 강좌
        DD_master_list = df_super_list[3][14]                #DD: 강사
        EE_master_list = df_super_list[4][14]                #EE: 수강생
        AA_master_list_col = df_super_list[0][13]
        BB_master_list_col = df_super_list[1][13]  # BB: 강의실
        CC_master_list_col = df_super_list[2][13]  # CC: 강좌
        DD_master_list_col = df_super_list[3][13]  # DD: 강사
        EE_master_list_col = df_super_list[4][13]  # EE: 수강생

        for i in range(len(AA_master_list)):
            if QDate.currentDate() >= QDate.fromString(AA_master_list[i][4],"yyyy-MM-dd") and \
                    QDate.currentDate() <= QDate.fromString(AA_master_list[i][5],"yyyy-MM-dd"):
                AA_master_list[i][11] = "x"
            else:
                AA_master_list[i][11] = ""
        df = pd.DataFrame(AA_master_list, columns=AA_master_list_col)
        df.to_excel('table/AA_season_master.xlsx', index=False)


        global BB_dictionary, CC_dictionary, DD_dictionary, EE_dictionary
        BB_dictionary = dict()
        for i in range(len(BB_master_list)):
            room_id = BB_master_list[i][0] + str(BB_master_list[i][1])
            BB_dictionary[room_id] = BB_master_list[i][2]
        CC_dictionary = dict()
        for i in range(len(CC_master_list)):
            class_id = CC_master_list[i][0] + str(CC_master_list[i][1])
            CC_dictionary[class_id] = CC_master_list[i][2]
        DD_dictionary = dict()
        for i in range(len(DD_master_list)):
            class_id = DD_master_list[i][0] + str(DD_master_list[i][1])
            DD_dictionary[class_id] = DD_master_list[i][2]
        EE_dictionary = dict()
        for i in range(len(EE_master_list)):
            class_id = EE_master_list[i][0] + str(EE_master_list[i][1])
            EE_dictionary[class_id] = EE_master_list[i][2]

        global df_time_col, df_time_period_list
        df = pd.read_excel('table/AA_time_period.xlsx')
        df.replace(np.NaN, '', inplace=True)
        df_time_col = list([col for col in df])
        df_time_period_list = df.values.tolist()

        global df_lesson_schedule_col, df_lesson_schedule_list
        df = pd.read_excel('table/CC_lesson_schedule.xlsx')
        df.replace(np.NaN, '', inplace=True)
        df_lesson_schedule_col = list([col for col in df])
        df_lesson_schedule_list = df.values.tolist()

        global df_teacher_lesson_col, df_teacher_lesson_list
        df = pd.read_excel('table/DD_teacher_lesson.xlsx')
        df.replace(np.NaN, '', inplace=True)
        df_teacher_lesson_col = list([col for col in df])
        df_teacher_lesson_list = df.values.tolist()

        global df_student_lesson_col, df_student_lesson_list
        df = pd.read_excel('table/EE_student_lesson.xlsx')
        df.replace(np.NaN, '', inplace=True)
        df_student_lesson_col = list([col for col in df])
        df_student_lesson_list = df.values.tolist()

        global settings_col, settings_list
        df = pd.read_excel('table/settings.xlsx')
        df.replace(np.NaN, '', inplace=True)
        settings_col = list([col for col in df])
        settings_list = df.values.tolist()

        global comboBox_season_arr
        global season_active_idx, Selected_season_ID, Selected_season_SDate, Selected_season_EDate, season_tabarray
        comboBox_season_arr = []
        season_tabarray = []
        season_active_idx = 99
        for i in range(len(AA_master_list)):
            active_flag = ""
            if AA_master_list[i][11] != "":        # 활성 상태인 경우
                active_flag = "(활성)"
                season_active_idx = i
            comboBox_season_arr.append("AA" + str(AA_master_list[i][1]) + " : " + AA_master_list[i][2] + " (" + \
                                       AA_master_list[i][4] + " ~ " + AA_master_list[i][5] + ") " + active_flag)
        if season_active_idx == 99:
            season_active_idx = len(AA_master_list)-1
        Selected_season_ID = comboBox_season_arr[season_active_idx].split(" :")[0]
        Selected_season_SDate = QDate.fromString(AA_master_list[season_active_idx][4], 'yyyy-MM-dd')
        Selected_season_EDate = QDate.fromString(AA_master_list[season_active_idx][5], 'yyyy-MM-dd')
        season_tabarray = []
        for i in range(len(df_time_period_list)):
            if df_time_period_list[i][0] == Selected_season_ID:
                season_tabarray.append(df_time_period_list[i])
        global tab_id, combobox_idx
        tab_id = 0
        combobox_idx = 0

        global days_of_week_arr
        days_of_week_arr = ["                                  ", "월", "화", "수", "목", "금", "토", "일"]

        global comboBox_select_arr
        comboBox_select_arr = []
        comboBox_select_arr.append(CC_master_list)
        comboBox_select_arr.append(BB_master_list)
        comboBox_select_arr.append(DD_master_list)
        comboBox_select_arr.append(EE_master_list)

        global bg_color_arr
        bg_color_arr = ["greenyellow", "lightpink", "yellow", "aquamarine", "peachpuff"]

        global teacher_dictionary
        teacher_dictionary = dict()
        for i in range(len(df_lesson_schedule_list)):
            for j in range(len(df_teacher_lesson_list)):
                if df_lesson_schedule_list[i][1] == df_teacher_lesson_list[j][2]:
                    teacher_dictionary[df_lesson_schedule_list[i][1]] = df_teacher_lesson_list[j][1]

    def setupUi(self):
        self.setWindowTitle("학원관리 시스템")
        self.setFixedSize(1370, 870)
        # self.showMaximized()

        self.centralwidget = QWidget()
        # Main Screen Title 정의
        self.mainTitleLabel = QLabel(self.centralwidget)
        self.mainTitleLabel.setGeometry(QRect(0, 20, 1370, 50))
        global_funtion().fontSetting(self.mainTitleLabel, '8H', 28, " ")  # "에스코어 드림 8 Heavy", PointSize(28)
        self.mainTitleLabel.setAlignment(Qt.AlignCenter)
        self.mainTitleLabel.setText("학원 관리 정보 시스템")

        self.mainTitleLabel = QLabel(self.centralwidget)
        self.mainTitleLabel.setGeometry(QRect(1100, 20, 160, 40))
        global_funtion().fontSetting(self.mainTitleLabel, '6B', 11, " ")  # "에스코어 드림 8 Heavy", PointSize(28)
        self.mainTitleLabel.setAlignment(Qt.AlignCenter)
        self.mainTitleLabel.setText("당일 : " + QDate.toString(QDate.currentDate(), 'yyyy-MM-dd'))

        # Main Screen에 있는 Tool Button 정의
        tool_button_master_arr = [["최신정보 갱신", 30, 20, 40, 40, "img/refresh.png", 40, 40, self.refreshInfo],
                           ["환경설정", 1290, 20, 40, 40, "img/OIP.jpg", 40, 40, self.logInInfo]]
        for i in range(len(tool_button_master_arr)):
            self.masterButton = QToolButton(self.centralwidget)
            global_funtion().tool_button_setting(self.masterButton, tool_button_master_arr[i])

        self.setCentralWidget(self.centralwidget)

        self.comboBox_season = QComboBox(self)
        self.comboBox_season.setGeometry(QRect(940, 85, 410, 25))
        self.comboBox_season.addItems(comboBox_season_arr)
        self.comboBox_season.setCurrentIndex(season_active_idx)
        self.comboBox_season.currentIndexChanged[int].connect(self.setDate)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QRect(20, 100, 1331, 751))
        self.tabWidget.setCurrentIndex(0)

        # 각 Tab에 대한 Title
        global tab_arr
        tab_arr = [["self.lessoncombo","self.lessontable", "강의 현황"], ["self.classroomcombo","self.classroomtable" ,"강의실 현황"],
                   ["self.teachercombo", "self.teachertable", "강사 현황"], ["self.studentcombo", "self.studenttable", "수강생 현황"]]
        for i in range(len(tab_arr)):
            self.tab = QWidget()

            # Tab에 대한 Title Setting
            self.label = QLabel(self.tab)
            self.label.setGeometry(QRect(0, 5, 1321, 51))
            global_funtion().fontSetting(self.label, '8H', 24, " ")  # "에스코어 드림 8 Heavy", PointSize(24)
            self.label.setAlignment(Qt.AlignCenter)
            self.label.setText(tab_arr[i][2] + "표")
            self.tabWidget.addTab(self.tab, tab_arr[i][2])

            self.dateLabel = QLabel(self.tab)
            self.dateLabel.setGeometry(QRect(10, 5, 400, 51))
            global_funtion().fontSetting(self.dateLabel, '6B', 11, " ")  # "에스코어 드림 8 Heavy", PointSize(24)
            day_int = 7 - QDate.currentDate().dayOfWeek()
            start_weekDay = QDate.toString(QDate.currentDate().addDays(-(QDate.currentDate().dayOfWeek() - 1)), 'yyyy-MM-dd')
            end_weekDay = QDate.toString(QDate.currentDate().addDays(day_int), 'yyyy-MM-dd')
            self.dateLabel.setText("이번 주차 : " + start_weekDay + " ~ " + end_weekDay)

            tool_button_arr = ["전체 상세정보", 970, 35, 25, 25, "img/memo.png", 25, 25, self.entireList]
            self.listButton = QToolButton(self.tab)
            global_funtion().tool_button_setting(self.listButton, tool_button_arr)

            tab_arr[i][0] = QComboBox(self.tab)
            tab_arr[i][0].setGeometry(QRect(1020, 35, 280, 25))
            tab_arr[i][0].addItem("전체")
            for j in range(len(comboBox_select_arr[i])):
                combo_text = comboBox_select_arr[i][j][0] + str(comboBox_select_arr[i][j][1]) + " : " + str(comboBox_select_arr[i][j][2])
                tab_arr[i][0].addItem(combo_text)
            tab_arr[i][0].currentIndexChanged[int].connect(self.comboboxTableInsert)

            # Table Widget에 대한 구조 Setting
            tab_arr[i][1] = QTableWidget(self.tab)
            tab_arr[i][1].setGeometry(QRect(10, 70, 1301, 651))
            tab_arr[i][1].setColumnCount(8)
            tab_arr[i][1].setRowCount(0)
            tab_arr[i][1].setEditTriggers(QAbstractItemView.NoEditTriggers)
            tab_arr[i][1].setFocusPolicy(Qt.NoFocus)
            tab_arr[i][1].cellClicked.connect(self.handleCellClicked)
            tab_arr[i][1].cellDoubleClicked.connect(self.handleCellDoubleClicked)

            global_funtion().fontSetting(tab_arr[i][1], '5M', 12, " ")   # "에스코어 드림 5 Medium", PointSize(12)

            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            header = tab_arr[i][1].horizontalHeader()
            header.setStyleSheet("::section {""background-color: lightgray;""}")

            for j in range(len(days_of_week_arr)):
                tab_arr[i][1].setHorizontalHeaderItem(j, item)
                item = tab_arr[i][1].horizontalHeaderItem(j)
                item.setText(days_of_week_arr[j])
                item = QTableWidgetItem()
                if j == 0:
                    header.setSectionResizeMode(j, QHeaderView.ResizeToContents)
                    continue
                header.setSectionResizeMode(j, QHeaderView.Stretch)
            # header.setHighlightSections(False)
            header.sectionPressed.disconnect()          # 전체 열 선택되게 하지 않는 법
            header.sectionClicked.connect(self.weekdayClicked)
            header.sectionDoubleClicked.connect(self.weekdayDoubleClicked)
            for j in range(len(season_tabarray)):
                rowPosition = tab_arr[i][1].rowCount()
                tab_arr[i][1].insertRow(rowPosition)
                item = QTableWidgetItem()
                global_funtion().fontSetting(item, '5M', 10, " ")  # "에스코어 드림 5 Medium", PointSize(12)
                item.setTextAlignment(Qt.AlignCenter)
                tab_arr[i][1].setItem(j, 0, item)
                item = tab_arr[i][1].item(j, 0)
                item.setText(str(season_tabarray[j][1]) + "교시\n" + season_tabarray[j][3] + " ~ " + season_tabarray[j][4])
            tab_arr[i][1].setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            tab_arr[i][1].verticalHeader().setVisible(False)
            tab_arr[i][1].setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.tabWidget.currentChanged.connect(self.get_tab_id)

        self.masterInfoTab = QWidget()
        # 기준정보 Tab의 왼쪽 상단에 있는 기준정보 생성 버튼
        tool_button_arr = [["기준정보 생성", 1230, 10, 30, 30, "img/add-file.png", 40, 40, self.addMaster],
                           ["기준정보 삭제", 1270, 10, 30, 30, "img/delete.png", 40, 40, self.delMaster]]
        for i in range(len(tool_button_arr)):
            self.addMasterInfoButton = QToolButton(self.masterInfoTab)
            global_funtion().tool_button_setting(self.addMasterInfoButton, tool_button_arr[i])
            self.tabWidget.addTab(self.masterInfoTab, "기준정보")

        self.treeWidget_structure_assembling()

        self.retranslateUi()

    def treeWidget_structure_assembling(self):
        global lvl_2_arr
        self.treeWidget = QTreeWidget(self.masterInfoTab)
        self.treeWidget.setGeometry(QRect(20, 50, 1291, 661))

        # Tree Widget의 두번째 정보를 출력하기 위한 리스트 정비하기
        lvl_2_arr = []
        for i in range(len(df_super_list)):       #i = 0(시즌), 1(강의실), 2(강좌), 3(강사), 4(수강생)
            df_list_temp = df_super_list[i][14]   #Excel Data Frame(df_super_list[i][12])을 배열의 List 형태로 변환된 배열명
            for j in range(len(df_list_temp)):
                if settings_list[0][0] != "x":
                    if df_list_temp[j][0] != "AA" and df_list_temp[j][11] != "x":
                        continue
                lvl_2_arr.append(df_list_temp[j])

        # Tree Widget의 헤더의 각 Column에 대한 Title
        for i in range(len(df_super_col)):       #i = 0(시즌), 1(강의실), 2(강좌), 3(강사), 4(수강생)
            if i == 0: continue                  #기준정보 유형코드
            if i == 10: break                    #10번째 Column부터 불필요한 정보
            global_funtion().fontSetting(self.treeWidget, '6B', 11, " ")  # "에스코어 드림 6 Bold", PointSize(11)
            self.treeWidget.headerItem().setText(i-1, df_super_col[i])

        # Tree Widget내에 Tree 구조에 맞도록 1st 레벨과 2nd 레벨의 정보를 출력하기
        for i in range(len(df_super_list)):                   #기준정보 유형에 대한 Title  #i = 0(시즌), 1(강의실), 2(강좌), 3(강사), 4(수강생)
            item_0 = QTreeWidgetItem(self.treeWidget)
            for j in range(len(df_super_list[i])):
                if j in (0, 9, 10): continue       # 기준정보 유형코드
                if j == 12: break          #
                global_funtion().fontSetting(item_0, '6B', 11, str(j-1))  # "에스코어 드림 6 Bold", PointSize(11)
                r = j
                if r == 11: r = r - 3
                self.treeWidget.topLevelItem(i).setText(j-1, df_super_list[i][r]) # 첫번째 레벨 정보 출력하기
            n = 0
            for j in range(len(lvl_2_arr)):                  #기준정보에 대한 출력
                if lvl_2_arr[j][0] == df_super_list[i][0]:
                    item_1 = QTreeWidgetItem(item_0)
                    m = 0
                    for k in range(len(lvl_2_arr[j])):
                        if k in (0, 9, 10): continue
                        # if k == 8 and df_super_list[i][0] in ("BB", "EE"): continue         #강의실, 수강생
                        if k == 12: break
                        if k == 1: super_code = df_super_list[i][0]         # 기준정보 유형코드
                        else:      super_code = ""
                        r = k
                        if k == 11: r = r-2
                        global_funtion().fontSetting(item_1, '5M', 10, str(r-1))  # "에스코어 드림 5 Medium", PointSize(10)
                        self.treeWidget.topLevelItem(i).child(n).setText(r-1, super_code + str(lvl_2_arr[j][k]))  #두번째 레벨 정보 출력하기
                        m += 1
                    n += 1
        self.treeWidget.itemClicked.connect(self.handleTreeItemClicked)
        self.treeWidget.itemDoubleClicked.connect(self.handleTreeItemDoubleClicked)

    def weekdayClicked(self, col):
        global clickedInfo, period_time, day_str
        clickedInfo = []
        period_time = 0
        if col == 0:
            return
        day_str = days_of_week_arr[col]
        teacher_error = 0
        student_error = 0
        for j in range(len(days_text_info_arr)):
            if day_str not in days_text_info_arr[j][5]:
                continue

            if tab_id == 2:
                for k in range(len(df_teacher_lesson_list)):
                    if days_text_info_arr[j][7] not in df_teacher_lesson_list[k][2]:
                        continue
                    teacher_error += 1
                if teacher_error == 0:
                    continue
            elif tab_id == 3:
                for k in range(len(df_student_lesson_list)):
                    if days_text_info_arr[j][7] not in df_student_lesson_list[k][2]:
                        continue
                    student_error += 1
                if student_error == 0:
                    continue


            clickedInfo.append(days_text_info_arr[j])

    def weekdayDoubleClicked(self, col):
        global clickedInfo, period_time, day_str
        self.get_tab_id()
        try:
            clickedInfo, period_time, day_str
        except NameError:
            global_funtion().message_box_1(QMessageBox.Warning, '경고', '볼 수 있는 강의 상세정보가 없습니다.', '확인')
            pass  # pass (중요) : 함수 무효화
        else:
            if len(clickedInfo) == 0:
                global_funtion().message_box_1(QMessageBox.Warning, '경고', '볼 수 있는 강의 상세정보가 없습니다.', '확인')
                return
            if tab_id == 0:
                win = Ui_Lesson_Detail_Dialog()
            elif tab_id == 1:
                win = Ui_Room_Detail_Dialog()
            elif tab_id == 2:
                win = Ui_Teacher_Detail_Dialog()
            else:
                win = Ui_Student_Detail_Dialog()
            win.exec_()

    def entireList(self):
        global clickedInfo, period_time, day_str
        clickedInfo = days_text_info_arr
        period_time = 100
        day_str = 100
        try:
            clickedInfo, period_time, day_str
        except NameError:
            global_funtion().message_box_1(QMessageBox.Warning, '경고', '볼 수 있는 강의 상세정보가 없습니다.', '확인')
            pass  # pass (중요) : 함수 무효화
        else:
            if len(clickedInfo) == 0:
                global_funtion().message_box_1(QMessageBox.Warning, '경고', '볼 수 있는 강의 상세정보가 없습니다.', '확인')
                return
            if tab_id == 0:
                win = Ui_Lesson_Detail_Dialog()
            elif tab_id == 1:
                win = Ui_Room_Detail_Dialog()
            elif tab_id == 2:
                win = Ui_Teacher_Detail_Dialog()
            else:
                win = Ui_Student_Detail_Dialog()
            win.exec_()

    def handleCellClicked(self, it, col):
        global clickedInfo, period_time, day_str
        clickedInfo = []
        info_data = tab_arr[tab_id][1].item(it, col).text()
        if info_data == "":
            return
        period_time = it + 1
        day_str = days_of_week_arr[col]

        for j in range(len(days_text_info_arr)):
            if days_text_info_arr[j][3] == period_time:
                if col == 0:
                    day_str = ""
                    clickedInfo.append(days_text_info_arr[j])
                    continue
                teacher_error = 0
                student_error = 0
                if day_str not in days_text_info_arr[j][5]:
                    continue

                if tab_id == 2:
                    for k in range(len(df_teacher_lesson_list)):
                        if days_text_info_arr[j][7] not in df_teacher_lesson_list[k][2]:
                            continue
                        teacher_error += 1
                    if teacher_error == 0:
                        continue
                elif tab_id == 3:
                    for k in range(len(df_student_lesson_list)):
                        if days_text_info_arr[j][7] not in df_student_lesson_list[k][2]:
                            continue
                        student_error += 1
                    if student_error == 0:
                        continue

                clickedInfo.append(days_text_info_arr[j])
        print(clickedInfo)


    def handleCellDoubleClicked(self, it, col):
        global clickedInfo, period_time, day_str
        self.get_tab_id()
        print(start_num)
        try:
            clickedInfo, period_time, day_str
        except:
            global_funtion().message_box_1(QMessageBox.Warning, '경고', '볼 수 있는 강의 상세정보가 없습니다.', '확인')
            pass  # pass (중요) : 함수 무효화
        else:
            if len(clickedInfo) == 0:
                global_funtion().message_box_1(QMessageBox.Warning, '경고', '볼 수 있는 강의 상세정보가 없습니다.', '확인')
                return
            if tab_id == 0:
                win = Ui_Lesson_Detail_Dialog()
            elif tab_id == 1:
                win = Ui_Room_Detail_Dialog()
            elif tab_id == 2:
                win = Ui_Teacher_Detail_Dialog()
            else:
                win = Ui_Student_Detail_Dialog()
            win.exec_()

    def handleTreeItemClicked(self, it, col):                   # it: TreeItem, col: Column no.
        global clickedRcdInfo
        clickedRcdInfo = []
        existed_item = ""
        for i in range(len(df_super_list)):                    #i = 0(시즌), 1(강의실), 2(강좌), 3(강사), 4(수강생)
           if df_super_list[i][0] == it.text(0)[:2]:           #기준정보 유형
               for j in range(len(lvl_2_arr)):
                   if lvl_2_arr[j][0] == df_super_list[i][0] and lvl_2_arr[j][1] == int(it.text(0)[2:]): # 기준정보유형 and 숫자 ID
                       clickedRcdInfo = lvl_2_arr[j]
                       existed_item = "x"
                       break
               if existed_item == "x": break
           elif df_super_list[i][1] == it.text(0):
                clickedRcdInfo.append(df_super_list[i][0])
                for j in range(0, 15):
                    clickedRcdInfo.append("")
                break

    def handleTreeItemDoubleClicked(self, it, col):                   # it: TreeItem, col: Column no.
        try:
            clickedRcdInfo
        except NameError:
            global_funtion().message_box_1(QMessageBox.Warning, '경고', '먼저 회원을 선택하세요.', '확인')
            pass      # pass (중요) : 함수 무효화
        else:
            if str(clickedRcdInfo[1]) == "":
               return
            else:
                if   clickedRcdInfo[0] == "AA":
                    win = Ui_Season_Master_Mgmt()
                elif clickedRcdInfo[0] == "BB":
                    win = Ui_Room_Master_Mgmt()
                elif clickedRcdInfo[0] == "CC":
                    win = Ui_Lesson_Master_Mgmt()
                elif clickedRcdInfo[0] == "DD":
                    win = Ui_Teacher_Master_Mgmt()
                elif clickedRcdInfo[0] == "EE":
                    win = Ui_Student_Master_Mgmt()
                win.exec_()

    def init_preparetion(self):
        global time_period_arr
        time_period_arr = []
        for i in range(len(df_time_period_list)):
            if df_time_period_list[i][0] != Selected_season_ID: continue   #시즌
            time_period_arr.append(df_time_period_list[i])
            
        global days_text_info_arr
        days_text_info_arr = []
        for i in range(len(df_lesson_schedule_list)):
            if df_lesson_schedule_list[i][0] != Selected_season_ID: continue #시즌
            day_info_arr = []
            for j in range(len(df_lesson_schedule_list[i])):
                if j <= 2: continue
                if j == 8: break
                if j <= 7:                                                 #강좌 ID,그룹 키,강의실 ID,시간 ID,요일 ID
                   day_info_arr.append(df_lesson_schedule_list[i][j])
            days_info = ""
            for j in range(len(df_lesson_schedule_list[i])):
                if j <= 7: continue
                if j == 15: break
                if df_lesson_schedule_list[i][j] == "X":
                    if   j ==  8: day_name = "월"
                    elif j ==  9: day_name = "화"
                    elif j ==  10: day_name = "수"
                    elif j ==  11: day_name = "목"
                    elif j == 12: day_name = "금"
                    elif j == 13: day_name = "토"
                    elif j == 14: day_name = "일"

                    if days_info == "":
                        days_info = days_info + day_name
                    else:
                        days_info = days_info + "," + day_name
            day_info_arr.append(days_info)
            for j in range(len(time_period_arr)):
                if time_period_arr[j][1] == df_lesson_schedule_list[i][6]:
                    day_info_arr.append(time_period_arr[j][2])            #Period Text 추가
            day_info_arr.append(df_lesson_schedule_list[i][1])
            days_text_info_arr.append(day_info_arr)

    def get_tab_id(self):
        global tab_id
        tab_id = self.tabWidget.currentIndex()
        self.tableInsert()

    def tableInsert(self):
        if tab_id >= 4:
            Selected_season_ID = comboBox_season_arr[self.comboBox_season.currentIndex()].split(" :")[0]
            print(Selected_season_ID)
            season_tabarray = []
            for i in range(len(df_time_period_list)):
                if df_time_period_list[i][0] == Selected_season_ID:
                    season_tabarray.append(df_time_period_list[i])
            self.init_preparetion()
            return
        self.comboboxTableInsert(0)

    def comboboxTableInsert(self, idx):
        global combobox_idx, Selected_season_ID, Selected_season_SDate, Selected_season_EDate, season_tabarray
        combobox_idx = idx
        tab_arr[tab_id][0].setCurrentIndex(combobox_idx)
        self.retranslateUi()

    def setDate(self, idx):
        global season_tabarray, Selected_season_ID
        season_tabarray = []
        Selected_season_ID = AA_master_list[idx][0] + str(AA_master_list[idx][1])
        print(Selected_season_ID)
        for i in range(len(df_time_period_list)):
            if df_time_period_list[i][0] == Selected_season_ID:
                season_tabarray.append(df_time_period_list[i])
        self.init_preparetion()
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        if tab_id >= 4:
            return
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        tab_arr[tab_id][1].clearContents()
        tab_arr[tab_id][1].setRowCount(0)
        x = 0

        global tab_table_arr
        tab_table_arr = []
        for i in range(len(season_tabarray)):
            rowPosition = tab_arr[tab_id][1].rowCount()
            tab_arr[tab_id][1].insertRow(rowPosition)
            item = QTableWidgetItem()
            global_funtion().fontSetting(item, '5M', 11, " ")  # "에스코어 드림 5 Medium", PointSize(12)
            item.setTextAlignment(Qt.AlignCenter)
            tab_arr[tab_id][1].setItem(i, 0, item)
            item = tab_arr[tab_id][1].item(i, 0)
            item.setText(str(season_tabarray[i][1]) + "교시\n" + season_tabarray[i][3] + " ~ " + season_tabarray[i][4])
            item.setBackground(QColor("lightgray"))

            for j in range(1, 8):
                item = QTableWidgetItem()
                global_funtion().fontSetting(item, '5M', 8, " ")  # "에스코어 드림 5 Medium", PointSize(12)
                item.setTextAlignment(Qt.AlignCenter)
                tab_arr[tab_id][1].setItem(i, j, item)
                if tab_id <= 1:
                    str_del = 1
                    for k in range(len(df_lesson_schedule_list)):
                        if df_lesson_schedule_list[k][0] != Selected_season_ID:
                            continue
                        pass_key = 0
                        for l in range(len(CC_master_list)):
                            if int(CC_master_list[l][1]) == int(df_lesson_schedule_list[k][3][2:]):
                                if CC_master_list[l][11] != "x":
                                    pass_key += 1
                                    break
                        if pass_key == 1:
                            continue
                        class_txt = ""
                        if df_lesson_schedule_list[k][6] == i+1:
                            class_txt = class_txt + CC_dictionary[df_lesson_schedule_list[k][3]] + \
                                        "(" + BB_dictionary[df_lesson_schedule_list[k][5]] + ")"
                        if class_txt != "":
                            if df_lesson_schedule_list[k][j+7] == "X":
                                item = tab_arr[tab_id][1].item(i, j)
                                if combobox_idx != 0:
                                    if tab_id == 0:
                                        check_lesson_txt = CC_master_list[combobox_idx-1][0] + str(CC_master_list[combobox_idx-1][1])
                                        if (check_lesson_txt) != df_lesson_schedule_list[k][3]:
                                            continue
                                    elif tab_id == 1:
                                        check_lesson_txt = BB_master_list[combobox_idx-1][0] + str(BB_master_list[combobox_idx-1][1])
                                        if (check_lesson_txt) != df_lesson_schedule_list[k][5]:
                                            continue
                                if item.text() != "":
                                    if str_del == 3:
                                        item.setText(item.text() + "\n" + "...")
                                        str_del = 1
                                        break
                                    item.setText(item.text() + "\n" + class_txt)
                                    str_del += 1
                                    continue
                                # if df_lesson_schedule_list[k][1][7] != "#":
                                #     if k != 0 and df_lesson_schedule_list[k][1] == df_lesson_schedule_list[k-1][1]:
                                #         x = x - 1
                                #     item.setBackground(QColor(bg_color_arr[x % 5]))
                                #     x = x + 1
                                tab_table_arr.append(df_lesson_schedule_list[k])
                                item.setText(class_txt)
                else:
                    if tab_id == 2:
                        str_del = 1
                        for k in range(len(df_lesson_schedule_list)):
                            if df_lesson_schedule_list[k][0] != Selected_season_ID:
                                continue
                            for l in range(len(CC_master_list)):
                                pass_key = 0
                                if int(CC_master_list[l][1]) == int(df_lesson_schedule_list[k][3][2:]):
                                    if CC_master_list[l][11] != "x":
                                        pass_key += 1
                                        break
                            if pass_key == 1:
                                continue
                            for l in range(len(df_teacher_lesson_list)):
                                if df_teacher_lesson_list[l][0] != df_lesson_schedule_list[k][0]:
                                    continue
                                pass_key = 0
                                for m in range(len(DD_master_list)):
                                    if int(DD_master_list[m][1]) == int(df_teacher_lesson_list[l][1][2:]):
                                        if DD_master_list[m][11] != "x":
                                            pass_key += 1
                                            break
                                if pass_key == 1:
                                    continue
                                teacher_txt = ""
                                if df_teacher_lesson_list[l][2] == df_lesson_schedule_list[k][1] and \
                                        df_lesson_schedule_list[k][6] == i+1:
                                    teacher_txt = teacher_txt + DD_dictionary[df_teacher_lesson_list[l][1]] + \
                                                  "(" + CC_dictionary[df_lesson_schedule_list[k][3]] + "," + \
                                                   BB_dictionary[df_lesson_schedule_list[k][5]] + ")"
                                if teacher_txt != "":
                                    if df_lesson_schedule_list[k][j + 7] == "X":
                                        item = tab_arr[tab_id][1].item(i, j)
                                        global_funtion().fontSetting(item, '5M', 8,
                                                                     " ")  # "에스코어 드림 5 Medium", PointSize(12)
                                        if combobox_idx != 0:
                                            check_teacher_txt = DD_master_list[combobox_idx - 1][0] + str(
                                                DD_master_list[combobox_idx - 1][1])
                                            if df_teacher_lesson_list[l][1] != check_teacher_txt:
                                                continue
                                        if item.text() != "":
                                            if str_del == 3:
                                                item.setText(item.text() + "\n" + "...")
                                                str_del = 1
                                                break
                                            item.setText(item.text() + "\n" + teacher_txt)
                                            str_del += 1
                                            break
                                        item.setText(teacher_txt)
                                        break
                    elif tab_id == 3:
                        str_del = 1
                        for k in range(len(df_lesson_schedule_list)):
                            if df_lesson_schedule_list[k][0] != Selected_season_ID:
                                continue
                            for l in range(len(CC_master_list)):
                                pass_key = 0
                                if int(CC_master_list[l][1]) == int(df_lesson_schedule_list[k][3][2:]):
                                    if CC_master_list[l][11] != "x":
                                        pass_key += 1
                                        break
                            if pass_key == 1:
                                continue
                            for l in range(len(df_student_lesson_list)):
                                if df_student_lesson_list[l][0] != df_lesson_schedule_list[k][0]:
                                    continue
                                pass_key = 0
                                for m in range(len(EE_master_list)):
                                    if int(EE_master_list[m][1]) == int(df_student_lesson_list[l][1][2:]):      # 수강생 번호 일치여부 확인
                                        if EE_master_list[m][11] != "x":            # 활성상태 확인
                                            pass_key += 1
                                            break
                                if pass_key == 1:   # 활성 아닐 시 조회 X
                                    continue
                                student_txt = ""
                                if df_student_lesson_list[l][2] == df_lesson_schedule_list[k][1] and \
                                        df_lesson_schedule_list[k][6] == i + 1:
                                    student_txt = student_txt + EE_dictionary[df_student_lesson_list[l][1]] + \
                                                  "(" + CC_dictionary[df_lesson_schedule_list[k][3]] + "," + \
                                                  BB_dictionary[df_lesson_schedule_list[k][5]] + ")"
                                    print(student_txt)
                                    print("(" + str(i) + ", " + str(j) + ")")
                                if student_txt != "":
                                    if df_lesson_schedule_list[k][j + 7] == "X":
                                        item = tab_arr[tab_id][1].item(i, j)
                                        global_funtion().fontSetting(item, '5M', 8,
                                                                     " ")  # "에스코어 드림 5 Medium", PointSize(12)
                                        if combobox_idx != 0:
                                            check_student_txt = EE_master_list[combobox_idx - 1][0] + str(
                                                EE_master_list[combobox_idx - 1][1])
                                            if df_student_lesson_list[l][1] != check_student_txt:
                                                continue
                                        if item.text() != "":
                                            print(str_del)
                                            if str_del == 3:
                                                item.setText(item.text() + "\n" + "...")
                                                str_del == 1
                                                break
                                            item.setText(item.text() + "\n" + student_txt)
                                            str_del += 1
                                            continue
                                        item.setText(student_txt)
                                        continue

                # comboBox_select_arr
        tab_arr[tab_id][1].resizeRowsToContents()


        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.init_preparetion()

    def addMaster(self):
        try:
            clickedRcdInfo
        except NameError:
            global_funtion().message_box_1(QMessageBox.Warning, '경고', '먼저 기준정보 유형을 선택하세요.', '확인')
            pass  # pass (중요) : 함수 무효화
        else:
            if str(clickedRcdInfo[1]) == "":
               if   clickedRcdInfo[0] == "AA":
                   win = Ui_Season_Master_Mgmt()
               elif clickedRcdInfo[0] == "BB":
                   win = Ui_Room_Master_Mgmt()
               elif clickedRcdInfo[0] == "CC":
                   win = Ui_Lesson_Master_Mgmt()
               elif clickedRcdInfo[0] == "DD":
                   win = Ui_Teacher_Master_Mgmt()
               elif clickedRcdInfo[0] == "EE":
                   win = Ui_Student_Master_Mgmt()
               win.exec_()
            else:
                global_funtion().message_box_1(QMessageBox.Warning, '경고', '먼저 기준정보 유형을 선택하세요.', '확인')
                pass  # pass (중요) : 함수 무효화

    def delMaster(self):
        try:
            clickedRcdInfo
        except NameError:
            global_funtion().message_box_1(QMessageBox.Warning, '경고', '먼저 기준정보 삭제대상을 선택하세요.', '확인')
            pass  # pass (중요) : 함수 무효화
        else:
            if clickedRcdInfo[0] == "AA":
                for i in range(len(AA_master_list)):
                    if AA_master_list[i][1] == clickedRcdInfo[1]:
                        for j in range(len(df_time_period_list)):
                            if int(df_time_period_list[j][0][2:]) == clickedRcdInfo[1]:
                                global_funtion().message_box_1(QMessageBox.Warning, '경고', '등록된 시간표가 존재하므로 삭제가 불가능합니다.', '확인')
                                return
                        AA_master_list.__delitem__(i)
                        break
                global_funtion().message_box_1(QMessageBox.Information, '확인', '삭제되었습니다.', '확인')
                df = pd.DataFrame(AA_master_list, columns=AA_master_list_col)
                df.to_excel('table/AA_season_master.xlsx', index=False)
            elif clickedRcdInfo[0] == "BB":
                for i in range(len(BB_master_list)):
                    if BB_master_list[i][1] == clickedRcdInfo[1]:
                        for j in range(len(df_lesson_schedule_list)):
                            if int(df_lesson_schedule_list[j][5][2:]) == clickedRcdInfo[1]:
                                global_funtion().message_box_1(QMessageBox.Warning, '경고', '강의실이 강의에 배정된 상태이므로 삭제가 불가능합니다.',
                                                               '확인')
                                return
                        BB_master_list.__delitem__(i)
                        break
                global_funtion().message_box_1(QMessageBox.Information, '확인', '삭제되었습니다.', '확인')
                df = pd.DataFrame(BB_master_list, columns=BB_master_list_col)
                df.to_excel('table/BB_room_master_data.xlsx', index=False)
            elif clickedRcdInfo[0] == "CC":
                for i in range(len(CC_master_list)):
                    if CC_master_list[i][1] == clickedRcdInfo[1]:
                        for j in range(len(df_lesson_schedule_list)):
                            if int(df_lesson_schedule_list[j][3][2:]) == clickedRcdInfo[1]:
                                global_funtion().message_box_1(QMessageBox.Warning, '경고',
                                                               '강의가 등록된 상태이므로 삭제가 불가능합니다.',
                                                               '확인')
                                return
                        CC_master_list.__delitem__(i)
                        break
                global_funtion().message_box_1(QMessageBox.Information, '확인', '삭제되었습니다.', '확인')
                df = pd.DataFrame(CC_master_list, columns=CC_master_list_col)
                df.to_excel('table/CC_lesson_master_data.xlsx', index=False)
            elif clickedRcdInfo[0] == "DD":
                for i in range(len(DD_master_list)):
                    if DD_master_list[i][1] == clickedRcdInfo[1]:
                        for j in range(len(df_teacher_lesson_list)):
                            if int(df_teacher_lesson_list[j][1][2:]) == clickedRcdInfo[1]:
                                global_funtion().message_box_1(QMessageBox.Warning, '경고',
                                                               '강사가 강의에 등록된 상태이므로 삭제가 불가능합니다.',
                                                               '확인')
                                return
                        DD_master_list.__delitem__(i)
                        break
                global_funtion().message_box_1(QMessageBox.Information, '확인', '삭제되었습니다.', '확인')
                df = pd.DataFrame(DD_master_list, columns=DD_master_list_col)
                df.to_excel('table/DD_teacher_master_data.xlsx', index=False)
            elif clickedRcdInfo[0] == "EE":
                for i in range(len(EE_master_list)):
                    if EE_master_list[i][1] == clickedRcdInfo[1]:
                        for j in range(len(df_student_lesson_list)):
                            if int(df_student_lesson_list[j][1][2:]) == clickedRcdInfo[1]:
                                global_funtion().message_box_1(QMessageBox.Warning, '경고',
                                                               '수강생이 강의에 등록된 상태이므로 삭제가 불가능합니다.',
                                                               '확인')
                                return
                        EE_master_list.__delitem__(i)
                        break
                global_funtion().message_box_1(QMessageBox.Information, '확인', '삭제되었습니다.', '확인')
                df = pd.DataFrame(EE_master_list, columns=EE_master_list_col)
                df.to_excel('table/EE_student_master_data.xlsx', index=False)
            self.refreshInfo()

    def refreshInfo(self):
        self.close()
        self.__init__()
        self.show()


    def logInInfo(self):
        global_funtion().message_box_2(QMessageBox.Question, "확인", "비활성 정보들을 조회하시겠습니까?", "예", "아니오")
        if MsgBoxRtnSignal == 'Y':
            settings_list[0][0] = "x"
        else:
            settings_list[0][0] = " "
        df = pd.DataFrame(settings_list, columns=settings_col)
        df.to_excel('table/settings.xlsx', index=False)
        global_funtion().message_box_1(QMessageBox.Information, "정보", "저장되었습니다", "확인")
        self.refreshInfo()

class Ui_Lesson_Detail_Dialog(QDialog):
    def __init__(self):
        super().__init__()
        # self.get_Init_data()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("상세정보")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setFixedSize(720, 470)

        self.titleLabel = QLabel(self)
        self.titleLabel.setGeometry(QRect(5, 22, 711, 51))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        global_funtion().fontSetting(self.titleLabel, '8H', 28, " ")  # "에스코어 드림 8 Heavy", PointSize(28)

        title_str = ""
        if period_time != 0 and period_time != 100:
            title_str += str(period_time) + "교시"
            if day_str != "" and day_str != 100:
                title_str += ", " + day_str + "요일 "
            else:
                title_str += " "
        else:
            if day_str != "" and day_str != 100:
                title_str += day_str + "요일 "
            else:
                title_str += "전체 "
        title_str += "상세정보"
        self.titleLabel.setText(title_str)


        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QRect(10, 110, 700, 340))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)

        global dialog_header
        dialog_header = ["시간", "요일", "강의", "강의실", "강사", "수강인원", "수용인원"]

        header = self.tableWidget.horizontalHeader()
        header.setStyleSheet("::section {""background-color: lightgray;""}")

        for j in range(len(dialog_header)):
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setHorizontalHeaderItem(j, item)
            header_item = self.tableWidget.horizontalHeaderItem(j)
            header_item.setText(dialog_header[j])
            header.setSectionResizeMode(j, QHeaderView.Stretch)
        # header.setHighlightSections(False)
        header.sectionPressed.disconnect()  # 전체 열 선택되게 하지 않는 법

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        for i in range(len(clickedInfo)):
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            for j in range(len(dialog_header)):
                # if period_time < 100 and day_str < 100:
                #     if period_time == 0:
                # dialog_header = ["시간", "요일", "강의", "강의실", "강사", "수강인원", "수용인원"]
                item = QTableWidgetItem()
                global_funtion().fontSetting(item, '5M', 11, " ")  # "에스코어 드림 5 Medium", PointSize(12)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(i, j, item)
                item = self.tableWidget.item(i, j)
                if j == 0:
                    item.setText(str(clickedInfo[i][3]) + "교시")
                elif j == 1:
                    item.setText(clickedInfo[i][5])
                elif j == 2:
                    item.setText(CC_dictionary[clickedInfo[i][0]])
                elif j == 3:
                    item.setText(BB_dictionary[clickedInfo[i][2]])
                elif j == 4:
                    teacher_name = " "
                    for k in range(len(df_teacher_lesson_list)):
                        if clickedInfo[i][7] == df_teacher_lesson_list[k][2]:
                            teacher_name = DD_dictionary[df_teacher_lesson_list[k][1]]
                            break
                    item.setText(teacher_name)
                elif j == 5:
                    count = 0
                    for k in range(len(df_student_lesson_list)):
                        if clickedInfo[i][7] == df_student_lesson_list[k][2]:
                            count += 1
                    item.setText(str(count))
                else:
                    item.setText("30")
                    # item.setBackground(QColor("lightgray"))

class Ui_Room_Detail_Dialog(QDialog):
    def __init__(self):
        super().__init__()
        # self.get_Init_data()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("상세정보")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setFixedSize(720, 470)

        self.titleLabel = QLabel(self)
        self.titleLabel.setGeometry(QRect(5, 22, 711, 51))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        global_funtion().fontSetting(self.titleLabel, '8H', 28, " ")  # "에스코어 드림 8 Heavy", PointSize(28)

        title_str = ""
        if period_time != 0 and period_time != 100:
            title_str += str(period_time) + "교시"
            if day_str != "" and day_str != 100:
                title_str += ", " + day_str + "요일 "
            else:
                title_str += " "
        else:
            if day_str != "" and day_str != 100:
                title_str += day_str + "요일 "
            else:
                title_str += "전체 "
        title_str += "상세정보"
        self.titleLabel.setText(title_str)


        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QRect(10, 110, 700, 340))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)

        global dialog_header
        dialog_header = ["시간", "요일", "강의실", "강의", "강사", "수강인원", "수용인원"]

        header = self.tableWidget.horizontalHeader()
        header.setStyleSheet("::section {""background-color: lightgray;""}")

        for j in range(len(dialog_header)):
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setHorizontalHeaderItem(j, item)
            header_item = self.tableWidget.horizontalHeaderItem(j)
            header_item.setText(dialog_header[j])
            header.setSectionResizeMode(j, QHeaderView.Stretch)
        # header.setHighlightSections(False)
        header.sectionPressed.disconnect()  # 전체 열 선택되게 하지 않는 법

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        for i in range(len(clickedInfo)):
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            for j in range(len(dialog_header)):
                # if period_time < 100 and day_str < 100:
                #     if period_time == 0:
                # dialog_header = ["시간", "요일", "강의", "강의실", "강사", "수강인원", "수용인원"]
                item = QTableWidgetItem()
                global_funtion().fontSetting(item, '5M', 11, " ")  # "에스코어 드림 5 Medium", PointSize(12)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(i, j, item)
                item = self.tableWidget.item(i, j)
                if j == 0:
                    item.setText(str(clickedInfo[i][3]) + "교시")
                elif j == 1:
                    item.setText(clickedInfo[i][5])
                elif j == 2:
                    item.setText(BB_dictionary[clickedInfo[i][2]])
                elif j == 3:
                    item.setText(CC_dictionary[clickedInfo[i][0]])
                elif j == 4:
                    teacher_name = " "
                    for k in range(len(df_teacher_lesson_list)):
                        if clickedInfo[i][7] == df_teacher_lesson_list[k][2]:
                            teacher_name = DD_dictionary[df_teacher_lesson_list[k][1]]
                            break
                    item.setText(teacher_name)
                elif j == 5:
                    count = 0
                    for k in range(len(df_student_lesson_list)):
                        if clickedInfo[i][7] == df_student_lesson_list[k][2]:
                            count += 1
                    item.setText(str(count))
                else:
                    item.setText("30")
                    # item.setBackground(QColor("lightgray"))

class Ui_Teacher_Detail_Dialog(QDialog):
    def __init__(self):
        super().__init__()
        # self.get_Init_data()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("상세정보")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setFixedSize(720, 470)

        self.titleLabel = QLabel(self)
        self.titleLabel.setGeometry(QRect(5, 22, 711, 51))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        global_funtion().fontSetting(self.titleLabel, '8H', 28, " ")  # "에스코어 드림 8 Heavy", PointSize(28)

        title_str = ""
        if period_time != 0 and period_time != 100:
            title_str += str(period_time) + "교시"
            if day_str != "" and day_str != 100:
                title_str += ", " + day_str + "요일 "
            else:
                title_str += " "
        else:
            if day_str != "" and day_str != 100:
                title_str += day_str + "요일 "
            else:
                title_str += "전체 "
        title_str += "상세정보"
        self.titleLabel.setText(title_str)


        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QRect(10, 110, 700, 340))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)

        global dialog_header
        dialog_header = ["시간", "요일", "강사", "강의", "강의실", "수강인원", "수용인원"]

        header = self.tableWidget.horizontalHeader()
        header.setStyleSheet("::section {""background-color: lightgray;""}")

        for j in range(len(dialog_header)):
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setHorizontalHeaderItem(j, item)
            header_item = self.tableWidget.horizontalHeaderItem(j)
            header_item.setText(dialog_header[j])
            header.setSectionResizeMode(j, QHeaderView.Stretch)
        # header.setHighlightSections(False)
        header.sectionPressed.disconnect()  # 전체 열 선택되게 하지 않는 법

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        for i in range(len(clickedInfo)):
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            for j in range(len(dialog_header)):
                # if period_time < 100 and day_str < 100:
                #     if period_time == 0:
                # dialog_header = ["시간", "요일", "강의", "강의실", "강사", "수강인원", "수용인원"]
                item = QTableWidgetItem()
                global_funtion().fontSetting(item, '5M', 11, " ")  # "에스코어 드림 5 Medium", PointSize(12)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(i, j, item)
                item = self.tableWidget.item(i, j)
                if j == 0:
                    item.setText(str(clickedInfo[i][3]) + "교시")
                elif j == 1:
                    item.setText(clickedInfo[i][5])
                elif j == 2:
                    teacher_name = " "
                    for k in range(len(df_teacher_lesson_list)):
                        if clickedInfo[i][7] == df_teacher_lesson_list[k][2]:
                            teacher_name = DD_dictionary[df_teacher_lesson_list[k][1]]
                            break
                    item.setText(teacher_name)
                elif j == 3:
                    item.setText(CC_dictionary[clickedInfo[i][0]])
                elif j == 4:
                    item.setText(BB_dictionary[clickedInfo[i][2]])
                elif j == 5:
                    count = 0
                    for k in range(len(df_student_lesson_list)):
                        if clickedInfo[i][7] == df_student_lesson_list[k][2]:
                            count += 1
                    item.setText(str(count))
                else:
                    item.setText("30")
                    # item.setBackground(QColor("lightgray"))

class Ui_Student_Detail_Dialog(QDialog):
    def __init__(self):
        super().__init__()
        # self.get_Init_data()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("상세정보")
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setFixedSize(720, 470)

        self.titleLabel = QLabel(self)
        self.titleLabel.setGeometry(QRect(5, 22, 711, 51))
        self.titleLabel.setAlignment(Qt.AlignCenter)
        global_funtion().fontSetting(self.titleLabel, '8H', 28, " ")  # "에스코어 드림 8 Heavy", PointSize(28)

        title_str = ""
        if period_time != 0 and period_time != 100:
            title_str += str(period_time) + "교시"
            if day_str != "" and day_str != 100:
                title_str += ", " + day_str + "요일 "
            else:
                title_str += " "
        else:
            if day_str != "" and day_str != 100:
                title_str += day_str + "요일 "
            else:
                title_str += "전체 "
        title_str += "상세정보"
        self.titleLabel.setText(title_str)


        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QRect(10, 110, 700, 340))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)

        global dialog_header
        dialog_header = ["시간", "요일", "수강생", "강의", "강의실", "강사", "수용인원"]

        header = self.tableWidget.horizontalHeader()
        header.setStyleSheet("::section {""background-color: lightgray;""}")

        for j in range(len(dialog_header)):
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)
            self.tableWidget.setHorizontalHeaderItem(j, item)
            header_item = self.tableWidget.horizontalHeaderItem(j)
            header_item.setText(dialog_header[j])
            header.setSectionResizeMode(j, QHeaderView.Stretch)
        # header.setHighlightSections(False)
        header.sectionPressed.disconnect()  # 전체 열 선택되게 하지 않는 법

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        student_arr = []
        for a in range(len(df_student_lesson_list)):
            for i in range(len(clickedInfo)):
                if clickedInfo[i][7] == df_student_lesson_list[a][2]:
                    copy_arr = clickedInfo[i].copy()
                    copy_arr.append(df_student_lesson_list[a][1])
                    rowPosition = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(rowPosition)
                    student_arr.append(copy_arr)
        print(student_arr)
        for i in range(len(student_arr)):
            for j in range(len(dialog_header)):
                item = QTableWidgetItem()
                global_funtion().fontSetting(item, '5M', 11, " ")  # "에스코어 드림 5 Medium", PointSize(12)
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(i, j, item)
                item = self.tableWidget.item(i, j)

                student_name = EE_dictionary[student_arr[i][8]]
                if j == 0:
                    item.setText(str(student_arr[i][3]) + "교시")
                elif j == 1:
                    item.setText(student_arr[i][5])
                elif j == 2:
                    item.setText(student_name)
                elif j == 3:
                    item.setText(CC_dictionary[student_arr[i][0]])
                elif j == 4:
                    item.setText(BB_dictionary[student_arr[i][2]])
                elif j == 5:
                    teacher_name = " "
                    for k in range(len(df_teacher_lesson_list)):
                        if student_arr[i][7] == df_teacher_lesson_list[k][2]:
                            teacher_name = DD_dictionary[df_teacher_lesson_list[k][1]]
                            break
                    item.setText(teacher_name)
                else:
                    count = 0
                    for k in range(len(df_student_lesson_list)):
                        if student_arr[i][7] not in df_student_lesson_list[k][2]:
                            continue
                        count += 1
                    item.setText(str(count))


class global_funtion():
    def fontSetting(self, tgt_widget, type, size, widget_index):
        font_type = {"4R":"에스코어 드림 4 Regular", "5M":"에스코어 드림 5 Medium",
                     "6B": "에스코어 드림 6 Bold", "8H": "에스코어 드림 8 Heavy"}
        font = QFont()
        font.setFamily(font_type[type])
        font.setPointSize(size)
        if widget_index == " ":
           tgt_widget.setFont(font)
        else:
           tgt_widget.setFont(int(widget_index), font)

    def tool_button_setting(self, qwidget, tool_button_arr):
        qwidget.setToolTip(tool_button_arr[0])
        qwidget.setGeometry(QRect(tool_button_arr[1], tool_button_arr[2], tool_button_arr[3], tool_button_arr[4]))
        icon = QIcon()
        icon.addPixmap(QPixmap(tool_button_arr[5]), QIcon.Normal, QIcon.Off)
        qwidget.setCursor(QCursor(Qt.PointingHandCursor))  # Point Cursor가 손가락 Cursor로 변경
        qwidget.setIcon(icon)
        qwidget.setIconSize(QSize(tool_button_arr[6], tool_button_arr[7]))
        qwidget.setStyleSheet("border : 0")
        qwidget.clicked.connect(tool_button_arr[8])

    def final_decision_button_box(self, qwidget, v, w, x, y, Ok_txt, Cancel_txt, Ok_evt, Canc_evt):
        qwidget.setGeometry(QRect(v, w, x, y))
        qwidget.setOrientation(Qt.Horizontal)
        qwidget.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        qwidget.button(QDialogButtonBox.Ok).setText(Ok_txt)           # Ok -> 등록, 저장
        qwidget.button(QDialogButtonBox.Cancel).setText(Cancel_txt)   # Cancel -> 취소
        qwidget.accepted.connect(Ok_evt)
        qwidget.rejected.connect(Canc_evt)

    # Message Icon Option : QMessageBox.[NoIcon, Question, Information, Warning, Critical]
    # 범용 Message Box(Single Buttons)
    def message_box_1(self, MsgOption, title, MsgText, YesText):
        msgBox1 = QMessageBox()
        msgBox1.setIcon(MsgOption)
        msgBox1.setWindowTitle(title)
        msgBox1.setText(MsgText)
        msgBox1.setStandardButtons(QMessageBox.Yes)
        buttonY = msgBox1.button(QMessageBox.Yes)
        buttonY.setText(YesText)
        msgBox1.exec_()

    # 범용 Message Box(2 Buttons)
    def message_box_2(self, MsgOption, title, MsgText, YesText, NoText):
        global MsgBoxRtnSignal

        msgBox2 = QMessageBox()
        msgBox2.setIcon(MsgOption)
        msgBox2.setWindowTitle(title)
        msgBox2.setText(MsgText)
        msgBox2.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = msgBox2.button(QMessageBox.Yes)
        buttonY.setText(YesText)
        buttonN = msgBox2.button(QMessageBox.No)
        buttonN.setText(NoText)
        msgBox2.exec_()

        if msgBox2.clickedButton() == buttonY:
           MsgBoxRtnSignal = 'Y'
        elif msgBox2.clickedButton() == buttonN:
           MsgBoxRtnSignal = 'N'
        return MsgBoxRtnSignal

if __name__ == "__main__":
    global start_num
    start_num = 0
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    app.exec_()

#### 참조
# self.pushButton.setStyleSheet("background: skyblue; border: 1px solid black; text-align: center;")

# (*)은 필수 입력 사항입니다
#     self.directionLabel = QLabel(self)                          # QDialog에 QLabel을 선언
#     self.directionLabel.setGeometry(QRect(150, 75, 180, 15))    # 위치
#     self.directionLabel.setText("(*)은 필수 입력사항입니다.")
#     global_funtion().fontSetting(self.directionLabel, '6B', 8, " ")  # "에스코어 드림 6 Bold", PointSize(9)
#     palette = QPalette()
#     palette.setColor(QPalette.WindowText, Qt.red)
#     self.directionLabel.setPalette(palette)