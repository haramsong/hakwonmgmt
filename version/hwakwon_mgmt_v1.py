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
        self.get_Init_data()
        self.setupUi()

    def get_Init_data(self):
        length_of_df_list = len(tabWidget_time_info_arr)

    def setupUi(self):
        self.setWindowTitle("시즌 시간 관리")
        self.resize(540, 665)

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
        # QMetaObject.connectSlotsByName(self)

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
                          self.timeEdit1.text(), self.timeEdit2.text(), "", "", "", ""]

        error_no = 0
        if add_target_arr[2].replace(" ","") == "":               #입력 필드내의 모든 공백 값 제거
            error_no = 1
        elif add_target_arr[3] >= add_target_arr[4]:
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
                if tabWidget_time_info_arr[i][5] == "":      #생성일
                   tabWidget_time_info_arr[i][5] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                   tabWidget_time_info_arr[i][6] = "admin"   #생성인
                   target_updated_record += 1
                else:
                   if tabWidget_time_info_arr[i][7] == "":      #변경일
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
        global days_arr, selected_ID, selected_name, selected_teacherID, selected_teacherName,  \
               selected_season_ID, selected_season_name, time_prd_arr

        selected_ID = selected_info[0]
        selected_name = selected_info[1]
        selected_teacherID = selected_info[2][:7]
        selected_teacherName = selected_info[2][9:]
        selected_season_ID = selected_info[3][:7]
        selected_season_name = selected_info[3][9:]

        time_prd_arr = []
        for i in range(len(df_time_period_list)):
            if df_time_period_list[i][0] != selected_season_ID: continue
            time_prd_arr.append(df_time_period_list[i])

        global tabWidget_less_schl_arr
        tabWidget_less_schl_arr = []
        for i in range(len(df_lesson_schedule_list)):
            lesson_schedule_arr = []
            if df_lesson_schedule_list[i][0] != selected_ID: continue
            if df_lesson_schedule_list[i][2] != selected_season_ID: continue
            for j in range(len(BB_master_list)):
                if BB_master_list[j][1] != int(df_lesson_schedule_list[i][1][2:]): continue
                lesson_schedule_arr.append(df_lesson_schedule_list[i][1] + ": " + BB_master_list[j][2])
                break
            for j in range(len(df_time_period_list)):
                if df_time_period_list[j][0] != selected_season_ID: continue
                if df_time_period_list[j][1] != df_lesson_schedule_list[i][3]: continue
                lesson_schedule_arr.append(str(df_time_period_list[j][1]) + " (교시): " + df_time_period_list[j][2])
                break
            for k in range(0,11):
                lesson_schedule_arr.append(df_lesson_schedule_list[i][k+4])

            tabWidget_less_schl_arr.append(lesson_schedule_arr)

            global length_of_df_list
            length_of_df_list = len(tabWidget_less_schl_arr)

    def setupUi(self):
        self.setWindowTitle("강좌 일정관리")
        self.resize(540, 665)

        self.label = QLabel(self)
        self.label.setGeometry(QRect(0, 15, 510, 40))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("강좌 일정 등록")
        global_funtion().fontSetting(self.label, '6B', 24, " ")  # "에스코어 드림 6 Bold", PointSize(24)

        self.gridLayoutWidget = QWidget(self)
        self.gridLayoutWidget.setGeometry(QRect(50, 80, 440, 160))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")

        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setObjectName("gridLayout")

        title_arr = ["강      좌", "강      사", "시      즌", "강  의  실", "시      간" ]
        for i in range(len(title_arr)):
            self.label = QLabel(self.gridLayoutWidget)
            self.label.setText(title_arr[i])
            self.gridLayout.addWidget(self.label, i, 0, 1, 1)

        global fld1_arr, fld2_arr
        fld1_arr = [["self.lessonLE1", selected_ID], ["self.teacherLE1", selected_teacherID],
                   ["self.seasonLE1", selected_season_ID]]
        for i in range(len(fld1_arr)):
            fld1_arr[i][0] = QLineEdit(self.gridLayoutWidget)
            fld1_arr[i][0].setText(fld1_arr[i][1])
            fld1_arr[i][0].setReadOnly(True)
            fld1_arr[i][0].setStyleSheet("background: lightgray")
            self.gridLayout.addWidget(fld1_arr[i][0], i, 1, 1, 1)

        fld2_arr = [["self.roomCB1", "BB"], ["self.periodCB1", "AA"]]
        for i in range(len(fld2_arr)):
            fld2_arr[i][0] = QComboBox(self.gridLayoutWidget)
            if fld2_arr[i][1] == "BB":
               for j in range(len(BB_master_list)):
                   fld2_arr[i][0].addItem("BB" + str(BB_master_list[j][1]))
                   fld2_arr[i][0].setItemText(j, "BB" + str(BB_master_list[j][1]) + ": " + BB_master_list[j][2])
            elif fld2_arr[i][1] == "AA":
                for j in range(len(time_prd_arr)):
                    fld2_arr[i][0].addItem(str(time_prd_arr[j][1]))
                    fld2_arr[i][0].setItemText(j, str(time_prd_arr[j][1]) + " (교시): " + time_prd_arr[j][2])
            self.gridLayout.addWidget(fld2_arr[i][0], i+3, 1, 1, 1)

        LE2_arr = [["self.lessonLE2", selected_name] , ["self.teacherLE2", selected_teacherName],
                   ["self.seasonLE2", selected_season_name], ["self.roomLE2", ""]]
        for i in range(len(LE2_arr)):
            if i == 3: continue
            LE2_arr[i][0] = QLineEdit(self.gridLayoutWidget)
            LE2_arr[i][0].setReadOnly(True)
            if LE2_arr[i][1] != "":
               LE2_arr[i][0].setText(LE2_arr[i][1])
            LE2_arr[i][0].setStyleSheet("background: lightgray")
            self.gridLayout.addWidget(LE2_arr[i][0], i, 2, 1, 1)

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

        tool_button_arr = [["강좌 추가", 440, 290, 30, 30, "img/add-file.png", 30, 30, self.addInfo],
                           ["강좌 삭제", 480, 290, 30, 30, "img/delete.png", 30, 30, self.delInfo]]
        for i in range(len(tool_button_arr)):
            self.toolButton = QToolButton(self)
            global_funtion().tool_button_setting(self.toolButton, tool_button_arr[i])

        tableWidget_hdr_arr = ["강의실", "시간", "월", "화", "수", "목", "금", "토", "일"]
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

        self.tableWidget.clearContents()
        for i in range(len(tabWidget_less_schl_arr)):
            self.tableWidget.removeRow(i)
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
            for j in range(len(tabWidget_less_schl_arr[i])):
                if j == 9: break
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignCenter)
                self.tableWidget.setItem(i, j, item)
                item = self.tableWidget.item(i, j)
                item.setText(tabWidget_less_schl_arr[i][j])

    def handleCellClicked(self, row):
        global less_schl_info
        clicked_cell_0 = self.tableWidget.item(row, 0).text()
        clicked_cell_1 = self.tableWidget.item(row, 1).text()

        # tablewidget에서 Clicked row의 강의실/시간 ID를 가지고 'tabWidget_less_schl_arr'의 특정 Record를 읽어옴
        for i in range(len(tabWidget_less_schl_arr)):
            if tabWidget_less_schl_arr[i][0] == clicked_cell_0 and tabWidget_less_schl_arr[i][1] == clicked_cell_1:
               less_schl_info = tabWidget_less_schl_arr[i]
               break

    def addInfo(self):
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

        add_target_arr = [fld2_arr[0][0].currentText(), fld2_arr[1][0].currentText(),
                          monday, tuesday, wednesday, thursday, friday, saturday,sunday, "", "", "", ""]
        error_exist = ""
        if monday == " " and tuesday == " " and wednesday == " " and thursday == " " and friday == " " and \
           saturday == " " and sunday == " ":
           global_funtion().message_box_1(QMessageBox.Critical, "오류", "요일 미지정", "확인")
           return

        for i in range(len(tabWidget_less_schl_arr)):
            if tabWidget_less_schl_arr[i][0] == add_target_arr[0] and tabWidget_less_schl_arr[i][1] == add_target_arr[1]:
                error_exist = "x"
                break

        if error_exist != "":
            global_funtion().message_box_1(QMessageBox.Critical, "오류", "이미 등록된 강좌/시간 정보가 존재", "확인")
            return

        tabWidget_less_schl_arr.append(add_target_arr)
        list.sort(tabWidget_less_schl_arr, key=lambda k: (k[0], k[1]))

        self.retranslateUi()

    def delInfo(self):
        print("erre")
        try:
            less_schl_info
        except NameError:
            global_funtion().message_box_1(QMessageBox.Warning, "경고", "삭제할 행을 선택하시오", "확인")
            pass
        else:
            for i in range(len(tabWidget_less_schl_arr)):
                if tabWidget_less_schl_arr[i][0] == less_schl_info[0] and \
                   tabWidget_less_schl_arr[i][1] == less_schl_info[1]:
                   tabWidget_less_schl_arr.__delitem__(i)
                   self.tableWidget.removeRow(i)
                   break

            self.retranslateUi()

    def accept(self):
        global_funtion().message_box_2(QMessageBox.Question, "확인", "작성내용을 저장하시겠습니까?", "예", "아니오")
        if MsgBoxRtnSignal == 'Y':
            target_updated_record = 0                   #TableWidget내 생성/변경 정보가 있는 지 점검하기 위한 인자
            temp_less_schl_list = []
            for i in range(len(tabWidget_less_schl_arr)):
                temp_less_schl_arr = []
                temp_less_schl_arr.append(fld1_arr[0][0].text())                             #강좌 ID
                temp_less_schl_arr.append(tabWidget_less_schl_arr[i][0].split(":")[0])       #강의실 ID
                temp_less_schl_arr.append(fld1_arr[2][0].text())                             #시즌 ID
                temp_less_schl_arr.append(int(tabWidget_less_schl_arr[i][1].split()[0]))  #시간 ID
                if tabWidget_less_schl_arr[i][9] == "":      #생성일
                   tabWidget_less_schl_arr[i][9] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                   tabWidget_less_schl_arr[i][10] = "admin"   #생성인
                   target_updated_record += 1
                else:
                   if tabWidget_less_schl_arr[i][11] == "":      #변경일
                      tabWidget_less_schl_arr[i][11] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                      tabWidget_less_schl_arr[i][12] = "admin"   #변경인
                      target_updated_record += 1
                for j in range(len(tabWidget_less_schl_arr[i])):
                    if j < 2: continue
                    temp_less_schl_arr.append(tabWidget_less_schl_arr[i][j])

                temp_less_schl_list.append(temp_less_schl_arr)

            if target_updated_record == 0 and length_of_df_list == len(tabWidget_less_schl_arr):
               global_funtion().message_box_1(QMessageBox.Warning, "경고", "변경된 정보가 없습니다", "확인")
               return

            # 최초 excel file에서 추출한 list를 다시 excel file로 저장하기 위해 현재 화면에 출력된 기존/생성/수정/변경된 정보를
            # 갱신하기 위해 화면에 출력된 기존 list 정보값을 모두 지우고 다시 화면 리스트 정보를 Append하여 excel file에 저장한 대상을 정비함
            del_idx_arr = []                       # numpy array 기능을 이용하기 위해 지울 대상의 Index를 수집할 목적
            for i in range(len(df_lesson_schedule_list)):
               if df_lesson_schedule_list[i][0] == selected_ID and df_lesson_schedule_list[i][2] == selected_season_ID:
                  del_idx_arr.append(i)

            np_type_arr = np.array(df_lesson_schedule_list)   #일반 배열을 numpy array 유형으로 전환하면 각 요소를 구분하는 Comma(,)가 제거된 상태가 됨
            np_type_arr = np.delete(np_type_arr, del_idx_arr, axis = 0)     # axis = 0 (Row), 1(Column)
            normal_arr = np_type_arr.tolist()

            df_lesson_schedule_list.clear()
            for i in range(len(normal_arr)):
                normal_arr[i][3] = int(normal_arr[i][3])      #numpy array 상태의 각 요소들은 변수 Type이 동일하게 적용되므로 특정 원소들은 원래 Type으로 변환필요
                df_lesson_schedule_list.append(normal_arr[i])

            for i in range(len(temp_less_schl_list)):
                df_lesson_schedule_list.append(temp_less_schl_list[i])

            list.sort(df_lesson_schedule_list, key=lambda k: (k[0], k[1], k[2], k[3]))
            print(df_lesson_schedule_col)
            df = pd.DataFrame(df_lesson_schedule_list, columns=df_lesson_schedule_col)
            df.to_excel('table/CC_lesson_schedule.xlsx', index=False)
            global_funtion().message_box_1(QMessageBox.Information, "정보", "저장되었습니다", "확인")

            self.close()
            # Ui_Master_Mgmt().exec_()
        else: pass

class Ui_Teach_Lesson_Schedule(QDialog):
    def __init__(self):
        super().__init__()
        self.get_Init_data()
        self.setupUi()

    def get_Init_data(self):
        global days_arr, selected_ID, selected_name, selected_teacherID, selected_teacherName,  \
               selected_season_ID, selected_season_name

        selected_ID = selected_info[0]
        selected_name = selected_info[1]
        selected_season_ID = selected_info[2][:7]
        selected_season_name = selected_info[2][9:]

        global lesson_arr
        lesson_arr = []
        for i in range(len(CC_master_list)):
            if CC_master_list[i][11] != "x": continue
            lesson_arr.append(CC_master_list[i][0] + str(CC_master_list[i][1]) + ": " + CC_master_list[i][2])

    def setupUi(self):
        self.setWindowTitle("강사 강좌 일정관리")
        self.resize(540, 665)

        self.label = QLabel(self)
        self.label.setGeometry(QRect(0, 15, 510, 40))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText("강좌 일정 등록")
        global_funtion().fontSetting(self.label, '6B', 24, " ")  # "에스코어 드림 6 Bold", PointSize(24)

        self.gridLayoutWidget = QWidget(self)
        self.gridLayoutWidget.setGeometry(QRect(50, 80, 440, 140))

        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(20)

        title_arr = ["강      사", "시      즌", "기      간" ]
        for i in range(len(title_arr)):
            self.label = QLabel(self.gridLayoutWidget)
            self.label.setText(title_arr[i])
            self.gridLayout.addWidget(self.label, i, 0, 1, 1)

        global fld1_arr, fld2_arr
        fld1_arr = [["self.teacherLE1", selected_ID], ["self.seasonLE1", selected_season_ID],
                    ["self.prdStrQDt", ""]]
        for i in range(len(fld1_arr)):
            if i != 2:
                fld1_arr[i][0] = QLineEdit(self.gridLayoutWidget)
                fld1_arr[i][0].setText(fld1_arr[i][1])
                fld1_arr[i][0].setReadOnly(True)
                fld1_arr[i][0].setStyleSheet("background: lightgray")
            else:
                fld1_arr[i][0] = QDateEdit(self.gridLayoutWidget)
                fld1_arr[i][0].setDate(QDate.fromString(CC_master_list[0][5], 'yyyy-MM-dd'))
                fld1_arr[i][0].setCalendarPopup(True)
            self.gridLayout.addWidget(fld1_arr[i][0], i, 1, 1, 1)

        fld2_arr = [["self.teacherLE2", selected_name], ["self.seasonLE2", selected_season_name],
                    ["self.prdEndQDt", ""]]
        for i in range(len(fld2_arr)):
            if i != 2:
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
        self.formLayoutWidget.setGeometry(QRect(50, 230, 440, 40))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(self.formLayoutWidget)
        self.label.setText("강      좌   ")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.comboBox_lesson = QComboBox(self.formLayoutWidget)
        self.comboBox_lesson.addItems(lesson_arr)
        self.comboBox_lesson.currentIndexChanged[int].connect(self.setDate)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboBox_lesson)

        self.horizontalLayoutWidget = QWidget(self)
        self.horizontalLayoutWidget.setGeometry(QRect(50, 245, 440, 50))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        tool_button_arr = [["강좌 추가", 440, 290, 30, 30, "img/add-file.png", 30, 30, self.addInfo],
                           ["강좌 삭제", 480, 290, 30, 30, "img/delete.png", 30, 30, self.delInfo]]
        for i in range(len(tool_button_arr)):
            self.toolButton = QToolButton(self)
            global_funtion().tool_button_setting(self.toolButton, tool_button_arr[i])

        tableWidget_hdr_arr = ["강좌 ID", "강좌명", "시작일", "종료일"]
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QRect(10, 320, 510, 255))
        self.tableWidget.setColumnCount(len(tableWidget_hdr_arr))
        self.tableWidget.setRowCount(0)
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

    def addInfo(self):
        # add_target_arr = [self.lessonLE1.text(), self.teacherLE1.text(), self.seasonLE1.text(),
        #                   self.self.roomCB1.currentText().split(":")[0], self.self.periodCB1.currentText().split(" ")[0],
        #                   days_arr[0][0].checkState(), days_arr[1][0].checkState(), days_arr[2][0].checkState(),
        #                   days_arr[3][0].checkState(), days_arr[4][0].checkState(), days_arr[5][0].checkState(),
        #                   days_arr[6][0].checkState(), "", "", "", ""]
        #
        # error_exist = ""
        # for i in range(len(time_prd_arr)):
        #     if time_prd_arr[i][3] == add_target_arr[3] and time_prd_arr[i][4] == add_target_arr[4]:
        #         error_exist = "x"
        #         break
        #
        # if error_no != "":
        #     global_funtion().message_box_1(QMessageBox.Critical, "오류", "이미 등록된 강의실/시간 정보가 존재", "확인")
        #     return
        #
        # time_prd_arr_arr.append(add_target_arr)
        # list.sort(time_prd_arr, key=lambda k: (k[0], k[1]))

        self.retranslateUi()

    def delInfo(self):
        print("delete Info")

    def setDate(self, idx):
        for i in range(len(CC_master_list)):
           if i == idx:
              fld1_arr[2][0].setDate(QDate.fromString(CC_master_list[i][5], 'yyyy-MM-dd'))
              fld2_arr[2][0].setDate(QDate.fromString(CC_master_list[i][6], 'yyyy-MM-dd'))
              break

class Ui_Master_Mgmt(QDialog):
    def __init__(self):
        super().__init__()
        self.get_Init_data()
        self.setupUi()

    def get_Init_data(self):
        global scr_control_event, win_header_title, master_type, master_ID, tabWidget_time_info_arr
        global comboBox_season_arr, season_active_idx

        master_type = clickedRcdInfo[0]
        master_type_dic = {"EE":"수강생", "DD":"강사", "CC":"강좌", "BB":"강의실", "AA":"강의시즌"}

        master_ID = clickedRcdInfo[0] + str(clickedRcdInfo[1])

        scr_control_event = "CRT"           # 생성           
        win_header_title = master_type_dic[master_type] + " 등록"
        if str(clickedRcdInfo[1]) != " ":
            scr_control_event = "CHG"       # 수정 
            win_header_title = master_type_dic[master_type] + " 정보수정"

        if master_type == "AA":             #시즌
            tabWidget_time_info_arr = []
            for i in range(len(df_time_period_list)):
                if df_time_period_list[i][0] != master_ID: continue
                tabWidget_time_info_arr.append(df_time_period_list[i])
        else:
            comboBox_season_arr = []
            for i in range(len(AA_master_list)):
                active_flag = " "
                if AA_master_list[i][11] != " ":
                    active_flag = "(활성)"
                    season_active_idx = i
                comboBox_season_arr.append("AA" + str(AA_master_list[i][1]) + ": " + AA_master_list[i][2] + active_flag)

    def setupUi(self):
        self.setWindowTitle("기준정보")
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.resize(490, 660)

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

        if   master_type == "EE":   # 수강생
            item_title = ["ID", "이름(필수)", "연락처(필수)", "성별", "직업", "직장/학교명", "생넌월일", "주소", "비고1","비고2"]
        elif master_type == "DD":   # 강사
            item_title = ["ID", "이름(필수)", "연락처(필수)", "성별", "최종학력", "최종학교", "생년월일", "주소", "주전공", "부전공"]
        elif master_type == "CC":   # 강좌
            item_title = ["ID", "강좌명1(필수)", "강좌명2(필수)", " ", "과목", "시작일자", "종료일자", "비고1", "비고2", "비고3"]
        elif master_type == "BB":   # 강의실
            item_title = ["ID", "강의실명1(필수)", "강의실명2(필수)", " ", "수용인원", "특이사항", "비고1", "비고2", "비고3", "비고4"]
        elif master_type == "AA":   # 강의시즌
            item_title = ["ID", "시즌명(필수)", "내용(필수)", " ", " ", "시작일 ", "종료일", "비고1", "비고2", "비고3",]

        for i in range(len(item_title)):
            self.label = QLabel(self.gridLayoutWidget)
            self.label.setText(item_title[i])
            self.gridLayout.addWidget(self.label, i, 0, 1, 1)

        self.groupBox = QGroupBox(self.gridLayoutWidget)
        self.groupBox.setMaximumSize(QSize(16777215, 25))
        self.groupBox.setStyleSheet("border : 0")
        self.idLabel = QLabel(self.groupBox)
        self.idLabel.setGeometry(QRect(20, 5, 65, 15))
        if scr_control_event == "CRT":
            self.idLabel.setText(str(clickedRcdInfo[1]))
        else:
            self.idLabel.setText(master_ID)     # ID
        if str(clickedRcdInfo[1]) == " ":
            tool_button_arr = ["ID 생성(필수정보 입력필", 280, 0, 25, 25, "img/add_person.png", 25, 25, self.addMember]
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
        if master_type in ("DD","EE"):
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
        if scr_control_event == "":                   # scr_control_event이 Blank이면 생성화면을 의미, 아니면 수정화면
            self.checkBox.setChecked(True)
        else:
            if clickedRcdInfo[11] == "x":
                self.checkBox.setChecked(True)
            else:
                self.checkBox.setChecked(False)
        self.checkBox.setGeometry(QRect(220, 5, 60, 20))
        self.gridLayout.addWidget(self.groupBox, 3, 1, 1, 1)

        comboBox_arr = []
        if master_type == "EE":                         #수강생: 직업
           comboBox_arr = ["학생", "직장인", "주부", "무직", "구직중"]
        elif master_type == "DD":                       #강사: 최종학력
           comboBox_arr = ["대졸", "석사졸", "박사졸", "대재", "고졸"]
        elif master_type == "CC":                       #강좌: 과목
           comboBox_arr = ["영어", "수학", "국어", "과학", "기타"]
        elif master_type == "BB":                       #강의실
           for i in range(1, 101):
               comboBox_arr.append(str(i) + " (명)")
        if comboBox_arr != []:                                         # "AA"(시즌)는 제외
            self.comboBox1 = QComboBox(self.gridLayoutWidget)
            self.comboBox1.addItems(comboBox_arr)
            self.gridLayout.addWidget(self.comboBox1, 4, 1, 1, 1)

        if master_type in ("AA", "CC"):
            self.fld2_DE = QDateEdit(self.gridLayoutWidget)
            if  master_type == "AA":                         #시즌: 시작일
                self.fld2_DE.setDate(QDate.fromString(clickedRcdInfo[4], 'yyyy-MM-dd'))
            else:                                            #강좌: 시작일
                if scr_control_event == "CRT":                 # 생성
                   self.fld2_DE.setDate(QDate.fromString(AA_master_list[season_active_idx][4], 'yyyy-MM-dd'))
                else:
                   self.fld2_DE.setDate(QDate.fromString(clickedRcdInfo[5], 'yyyy-MM-dd'))
            self.fld2_DE.setCalendarPopup(True)
            self.gridLayout.addWidget(self.fld2_DE, 5, 1, 1, 1)
        else:
            self.fld2_LE = QLineEdit(self.gridLayoutWidget)
            if   master_type == "BB":                         #강의실: 특이사항
                self.fld2_LE.setText(clickedRcdInfo[5])
            elif master_type == "DD":                         #강사: 최종학교
                self.fld2_LE.setText(clickedRcdInfo[6])
            elif master_type == "EE":                         #수강생: 작장/학교명
                self.fld2_LE.setText(clickedRcdInfo[6])
            self.gridLayout.addWidget(self.fld2_LE, 5, 1, 1, 1)

        if master_type in ("BB", "DD", "EE"):
            self.fld3_LE = QLineEdit(self.gridLayoutWidget)
            if   master_type == "BB":                        #강의실: 비고1
               self.fld3_LE.setText(clickedRcdInfo[6])
            elif master_type == "DD":                        #강사: 생년월일
               self.fld3_LE.setText(clickedRcdInfo[9])
            elif master_type == "EE":                        #수강생: 생년월일
               self.fld3_LE.setText(clickedRcdInfo[7])
            self.gridLayout.addWidget(self.fld3_LE, 6, 1, 1, 1)
        else:
            self.fld3_DE = QDateEdit(self.gridLayoutWidget)
            if   master_type == "AA":                         #시즌: 종료일
                 self.fld3_DE.setDate(QDate.fromString(clickedRcdInfo[5], 'yyyy-MM-dd'))
            elif master_type == "CC":                         #강좌: 종료일자
                 if scr_control_event == "CRT":                 # 생성
                    self.fld3_DE.setDate(QDate.fromString(AA_master_list[season_active_idx][5], 'yyyy-MM-dd'))
                 else:
                    self.fld3_DE.setDate(QDate.fromString(clickedRcdInfo[6], 'yyyy-MM-dd'))
            self.fld3_DE.setCalendarPopup(True)
            self.gridLayout.addWidget(self.fld3_DE, 6, 1, 1, 1)

        self.fld4_LE = QLineEdit(self.gridLayoutWidget)
        if   master_type == "AA":                       #시즌: 비고1
           self.fld4_LE.setText(clickedRcdInfo[6])
        elif master_type == "BB":                       #강의실: 비고2
           self.fld4_LE.setText(clickedRcdInfo[7])
        elif master_type == "CC":                       #강좌: 비고2
           self.fld4_LE.setText(clickedRcdInfo[7])
        elif master_type == "EE":                       #수강생: 주소
           self.fld4_LE.setText(clickedRcdInfo[8])
        elif master_type == "DD":                       #강사: 주소
               self.fld4_LE.setText(clickedRcdInfo[10])
        else: self.fld4_LE.setText("")
        self.gridLayout.addWidget(self.fld4_LE, 7, 1, 1, 1)

        self.remark1LE = QLineEdit(self.gridLayoutWidget)
        if   master_type == "AA":                       #시즌: 비고2
           self.remark1LE.setText(clickedRcdInfo[7])
        elif master_type == "BB":                       #강의실: 비고3
           self.remark1LE.setText(clickedRcdInfo[8])
        elif master_type == "CC":                       #강좌: 비고3
           self.remark1LE.setText(clickedRcdInfo[8])
        elif master_type == "DD":                       #강사: 주전공
           self.remark1LE.setText(clickedRcdInfo[7])
        elif master_type == "EE":                       #수강생: 비고1
           self.remark1LE.setText(clickedRcdInfo[9])
        else: self.remark1LE.setText("")
        self.gridLayout.addWidget(self.remark1LE, 8, 1, 1, 1)

        self.remark2LE = QLineEdit(self.gridLayoutWidget)
        if   master_type == "AA":                       #시즌: 비고3
            self.remark2LE.setText(clickedRcdInfo[8])
        elif master_type == "BB":                       #강의실: 비고4
            self.remark2LE.setText(clickedRcdInfo[9])
        elif master_type == "CC":                       #강좌: 비고4
            self.remark2LE.setText(clickedRcdInfo[10])
        elif master_type == "DD":                       #강사: 부전공
            self.remark2LE.setText(clickedRcdInfo[8])
        elif master_type == "EE":                       #수강생: 비고2
            self.remark2LE.setText(clickedRcdInfo[10])
        else: self.remark2LE.setText(clickedRcdInfo[10])
        self.gridLayout.addWidget(self.remark2LE, 9, 1, 1, 1)

        if   master_type == "AA":    # 강의시즌
             lesson_apply_hdr_arr = ["시간", "시간명", "시작시간", "종료시간"]
        elif master_type == "BB":    # 강의실
             lesson_apply_hdr_arr = ["요일", "시간", "시간명", "강좌", "시작일", "종료일"]
        elif master_type == "CC":    # 강좌
             lesson_apply_hdr_arr = ["요일", "시간", "시간명", "강의실", "등록일", "정지일"]
        elif master_type == "DD":  # 강사
             lesson_apply_hdr_arr = ["강좌", "강좌명", "시작일", "종료일", "등록일", "정지일"]
        elif master_type == "EE":  # 수강생
             lesson_apply_hdr_arr = ["강좌", "강좌명", "강사", "강의실", "시작일", "종료일", "등록일", "정지일"]

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QRect(20, 430, 450, 150))
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 전체 cell read-only
        self.tableWidget.verticalHeader().setVisible(False)  # index 안보이는 기능
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

        if master_type in ("CC", "EE"):              #강좌, 수강생
            table_title = "강좌 등록"
            self.label = QLabel(self)
            self.label.setGeometry(QRect(30, 410, 70, 20))
            self.label.setText(table_title)
            global_funtion().fontSetting(self.label, '6B', 11, " ")   # "에스코어 드림 6 Bold", PointSize(11)

        if master_type != "AA":                      #시즌
            self.comboBox_season = QComboBox(self)
            self.comboBox_season.setGeometry(QRect(270, 400, 195, 25))
            self.comboBox_season.addItems(comboBox_season_arr)
            self.comboBox_season.setCurrentIndex(season_active_idx)
            self.comboBox_season.currentIndexChanged[int].connect(self.setDate)

        master_type_tool_info = {"AA": "시간관리", "CC": "장소/시간관리", "DD": "강좌관리", "EE": "강좌관리"}
        tool_button_arr = [20, 590, 30, 30, "img/edit.png", 30, 30, self.addInfo]
        if master_type in master_type_tool_info:
            tool_button_arr.insert(0, master_type_tool_info[master_type])
            self.toolButton = QToolButton(self)
            global_funtion().tool_button_setting(self.toolButton, tool_button_arr)

        self.buttonBox = QDialogButtonBox(self)
        global_funtion().final_decision_button_box(self.buttonBox, 130, 600, 340, 30, "저장", "나가기",
                                                   self.accept, self.reject)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate

        if master_type == "AA":            #시즌
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
        print(clickedRcdInfo)

    def addInfo(self):
        global selected_info
        if  master_type == "AA":                 #시즌
            selected_info = [self.idLabel.text(), self.nameLE.text(), " ",  " "]
            win = Ui_Season_Period()
        elif master_type in ("CC", "EE"):        #강좌, 수강생,
            selected_info = [self.idLabel.text(), self.nameLE.text(), " ",
                                   self.comboBox_season.currentText()]
            win = Ui_Lesson_Schedule()
        elif master_type == "DD":                #강사
            selected_info = [self.idLabel.text(), self.nameLE.text(), self.comboBox_season.currentText()]
            win = Ui_Teach_Lesson_Schedule()
        win.exec_()

    def delInfo(self):
        print("delete Info")

    def setDate(self, idx):
        if master_type != "CC" or scr_control_event != "CRT":
           return
        for i in range(len(AA_master_list)):
           if i == idx:
              self.fld2_DE.setDate(QDate.fromString(AA_master_list[i][4], 'yyyy-MM-dd'))
              self.fld3_DE.setDate(QDate.fromString(AA_master_list[i][5], 'yyyy-MM-dd'))

    def accept(self):
        print("accept")
        self.close()  

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.get_Init_data()
        self.setupUi()                  # 화면 레이아웃

    def get_Init_data(self):
        global df_super, df_super_col, df_super_list, today_QDate, length_of_df_list

        df_super = pd.read_excel('table/super_master.xlsx')
        df_super.replace(np.NaN, ' ', inplace=True)
        df_super_col = list([col for col in df_super])
        df_super_list = df_super.values.tolist()

        today_QDate = QDate.currentDate()

        for i in range(len(df_super_list)):                   #i = 0(시즌), 1(강의실), 2(강좌), 3(강사), 4(수강생)
            file_path = 'table/' + df_super_list[i][15]
            df_super_list[i][12] = pd.read_excel(file_path)
            df_super_list[i][12].replace(np.NaN, ' ', inplace=True)
            df_super_list[i][13] = list([col for col in df_super_list[i][12]])
            df_super_list[i][14] = df_super_list[i][12].values.tolist()

        global AA_master_list, BB_master_list, CC_master_list, DD_master_list, EE_master_list
        AA_master_list = df_super_list[0][14]                #AA: 시즌
        BB_master_list = df_super_list[1][14]                #BB: 강의실
        CC_master_list = df_super_list[2][14]                #CC: 강좌
        DD_master_list = df_super_list[3][14]                #DD: 강사
        EE_master_list = df_super_list[4][14]                #EE: 수강생

        global df_time_col, df_time_period_list, df_lesson_schedule_col, df_lesson_schedule_list
        df = pd.read_excel('table/AA_time_period.xlsx')
        df.replace(np.NaN, ' ', inplace=True)
        df_time_col = list([col for col in df])
        df_time_period_list = df.values.tolist()

        df = pd.read_excel('table/CC_lesson_schedule.xlsx')
        df.replace(np.NaN, ' ', inplace=True)
        df_lesson_schedule_col = list([col for col in df])
        df_lesson_schedule_list = df.values.tolist()

    def setupUi(self):
        self.setWindowTitle("학원관리 시스템")
        self.resize(1370, 870)
        # self.showMaximized()

        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")

        # Main Screen Title 정의
        self.mainTitleLabel = QLabel(self.centralwidget)
        self.mainTitleLabel.setGeometry(QRect(0, 20, 1370, 50))
        global_funtion().fontSetting(self.mainTitleLabel, '8H', 28, " ")  # "에스코어 드림 8 Heavy", PointSize(28)
        self.mainTitleLabel.setAlignment(Qt.AlignCenter)
        self.mainTitleLabel.setText("학원 관리 정보 시스템")

        # Main Screen에 있는 Tool Button 정의
        tool_button_arr = [["최신정보 갱신", 30, 20, 40, 40, "img/refresh.png", 40, 40, self.refreshInfo],
                           ["환경설정", 1290, 20, 40, 40, "img/OIP.jpg", 40, 40, self.logInInfo]]
        for i in range(len(tool_button_arr)):
            self.toolButton = QToolButton(self)
            global_funtion().tool_button_setting(self.toolButton, tool_button_arr[i])

        self.setCentralWidget(self.centralwidget)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QRect(20, 100, 1331, 751))
        self.tabWidget.setCurrentIndex(0)

        # 각 Tab에 대한 Title
        tab_arr = ["강의 현황", "강의실 현황", "강좌 현황", "수강생 현황", "강사 현황"]
        for i in range(len(tab_arr)):
            self.tab = QWidget()

            # Tab에 대한 Title Setting
            self.label = QLabel(self.tab)
            self.label.setGeometry(QRect(0, 0, 1321, 51))
            global_funtion().fontSetting(self.label, '8H', 24, " ")  # "에스코어 드림 8 Heavy", PointSize(24)
            self.label.setAlignment(Qt.AlignCenter)
            self.label.setText(tab_arr[i] + "표")
            self.tabWidget.addTab(self.tab, tab_arr[i])

            # Table Widget에 대한 구조 Setting
            self.tableWidget = QTableWidget(self.tab)
            self.tableWidget.setGeometry(QRect(10, 70, 1301, 651))

            global_funtion().fontSetting(self.tableWidget, '5M', 12, " ")   # "에스코어 드림 5 Medium", PointSize(12)
            self.tableWidget.setColumnCount(8)
            self.tableWidget.setRowCount(0)
            item = QTableWidgetItem()
            item.setTextAlignment(Qt.AlignCenter)

            days_of_week_arr = [" ", "월", "화", "수", "목", "금", "토", "일"]
            for j in range(len(days_of_week_arr)):
                self.tableWidget.setHorizontalHeaderItem(j, item)
                item = self.tableWidget.horizontalHeaderItem(j)
                item.setText(days_of_week_arr[j])
                item = QTableWidgetItem()

        self.tabWidget.currentChanged.connect(self.get_tab_id)

        # 기준정보 Tab의 왼쪽 상단에 있는 기준정보 생성 버튼
        tool_button_arr = ["기준정보 생성", 1270, 10, 30, 30, "img/add-file.png", 40, 40, self.addMaster]
        self.masterInfoTab = QWidget()
        self.addMasterInfoButton = QToolButton(self.masterInfoTab)
        global_funtion().tool_button_setting(self.addMasterInfoButton, tool_button_arr)
        self.tabWidget.addTab(self.masterInfoTab, "기준정보")

        self.treeWidget_structure_assembling()

        self.retranslateUi()

        QMetaObject.connectSlotsByName(self)

    def treeWidget_structure_assembling(self):
        global lvl_2_arr
        self.treeWidget = QTreeWidget(self.masterInfoTab)
        self.treeWidget.setGeometry(QRect(20, 50, 1291, 661))

        # Tree Widget의 두번째 정보를 출력하기 위한 리스트 정비하기
        lvl_2_arr = []
        for i in range(len(df_super_list)):       #i = 0(시즌), 1(강의실), 2(강좌), 3(강사), 4(수강생)
            df_list_temp = df_super_list[i][14]   #Excel Data Frame(df_super_list[i][12])을 배열의 List 형태로 변환된 배열명
            for j in range(len(df_list_temp)):
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
                # brush = QBrush(QColor(255, 0, 0))
                # brush.setStyle(Qt.NoBrush)
                # item_0.setForeground(0, brush)
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
                        if k == 8 and df_super_list[i][0] in ("BB", "EE"): continue         #강의실, 수강생
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

    def handleTreeItemClicked(self, it, col):                   # it: TreeItem, col: Column no.
        global clickedRcdInfo
        clickedRcdInfo = []
        existed_item = " "
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
                    clickedRcdInfo.append(" ")
                break

    def handleTreeItemDoubleClicked(self, it, col):                   # it: TreeItem, col: Column no.
        try:
            clickedRcdInfo
        except NameError:
            global_funtion().message_box_1(QMessageBox.Warning, '경고', '먼저 회원을 선택하세요.', '확인')
            pass      # pass (중요) : 함수 무효화
        else:
            if str(clickedRcdInfo[1]) == " ":
               return
            else:
               win = Ui_Master_Mgmt()
               win.exec_()

    def get_tab_id(self, idx):
        print(idx)

    def retranslateUi(self):
        _translate = QCoreApplication.translate

        __sortingEnabled = self.treeWidget.isSortingEnabled()

        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.setSortingEnabled(__sortingEnabled)

    def addMaster(self):
        try:
            clickedRcdInfo
        except NameError:
            global_funtion().message_box_1(QMessageBox.Warning, '경고', '먼저 기준정보 유형을 선택하세요.', '확인')
            pass  # pass (중요) : 함수 무효화
        else:
            if str(clickedRcdInfo[1]) == " ":
               win = Ui_Master_Mgmt()
               win.exec_()
            else:
                global_funtion().message_box_1(QMessageBox.Warning, '경고', '먼저 기준정보 유형을 선택하세요.', '확인')
                pass  # pass (중요) : 함수 무효화

    def refreshInfo(self):
        self.close()
        self.__init__()
        self.show()

    def logInInfo(self):
        self.close()

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