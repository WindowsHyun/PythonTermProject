# -*- coding: utf-8 -*-
import sys
import urllib
import time
import GUI
import txtOut # C/C++ 연동 pyd 파일
from FunctionUtility import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit
from PyQt5.QtWidgets import QTextEdit, QWidget, QDialog, QApplication, QMessageBox, QPushButton, QMainWindow

class MainWindow(QDialog, GUI.Ui_Dialog):
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '미세먼지 주의보', "정말 종료할까요?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept() 
        else:
            event.ignore()      
    
    def ListClicked(self):
        sender = self.sender()
        list = sender.currentItem()
        serverurl = "http://openapi.epost.go.kr/postal/retrieveLotNumberAdressService/retrieveLotNumberAdressService/getEupMyunDongList?ServiceKey="
        servervalue = "&brtcCd=" + urlencode(self.LocationBoxData) + "&signguCd=" + urlencode(list.text()) + "&numOfRows=999&pageSize=999&pageNo=1&startPage=1"
        self.LocationListData = list.text()
        self.DetailList.clear()
        areaData = openAPItoXML(serverurl, self.serverKey, servervalue)
        diclist = addParsingDicList(areaData, "eupMyunDongList", "emdCd")

        serverurl = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?ServiceKey="
        servervalue = "&sidoName=" + urlencode(self.LocationBoxData) + "&numOfRows=999&pageSize=999&pageNo=1&startPage=1"
        areaData = openAPItoXML(serverurl, self.serverKey, servervalue)
        dic = addParsingDicList(areaData, "item", "stationName")

        compareListAdd(diclist, dic, self.DetailList, "*")

    def BtnClicked(self):
        sender = self.sender()
        ###########################################
        # 탭을 클릭할 경우와 갱신 버튼을 누를경우 currentIndex가 정상적으로 작동하지 않는다.
        # 그걸 방지하기 위해 indexBox를 만들어 미리 오류처리를 여기서 해결한다.
        indexBox = ""
        try:
            indexBox = sender.currentIndex()
        except:
            indexBox = 0
        ###########################################
        
        if sender.objectName() == "sendBtn" or sender.objectName() == "saveBtn_2" :    # 메일 보내기 & 저장하기
            ContentData = ""
            ContentData += str("현재 위치 : ") + str(self.Loaction.text()) + str("\n")
            
            if self.infoChkBox.isChecked() == True:
                ContentData += str(self.getTime.text()) + str("\n")
                ContentData += str(self.totalValue.text()) + str("\n")
                ContentData += str("PM10 미세먼지 : ") + str(self.PM10Label.text()) + str("\n")
                ContentData += str("O3 오존 : ") + str(self.o3Label.text()) + str("\n")
                ContentData += str("NO2 이산화질소 : ") + str(self.No2Label.text()) + str("\n")
                ContentData += str("CO 일산화탄소 : ") + str(self.CoLabel.text()) + str("\n")
                ContentData += str("SO2 이황산가스 : ") + str(self.So2Label.text()) + str("\n\n")
                pass

            if self.DustChkBox.isChecked() == True:
                ContentData += str("오늘의 예보 : ") + str(self.today_date.text()) + str("\n")
                ContentData += str("예보 개황 : ") + str(self.informOverall.toPlainText()) + str("\n")
                ContentData += str("발생 원인 : ") + str(self.informCause.toPlainText()) + str("\n")
                ContentData += str("예보 등급 : ") + str(self.informGrade.toPlainText()) + str("\n\n")
                pass

            if self.PM10ChkBox.isChecked() == True:
                ContentData += str("통합지수 정보 : ") + str("\n")
                ContentData += str("    - 좋음 : 0 ~ 50") + str("\n")
                ContentData += str("    - 보통 : 50 ~ 100") + str("\n")
                ContentData += str("    - 약간 나쁨 : 101 ~ 150") + str("\n")
                ContentData += str("    - 나쁨 : 151 ~ 250") + str("\n")
                ContentData += str("    - 매우 나쁨 : 251 ~") + str("\n\n")
                ContentData += str("미세먼지 정보 : ") + str("\n")
                ContentData += str("    - 좋음 : 0 ~ 30") + str("\n")
                ContentData += str("    - 보통 : 31 ~ 80") + str("\n")
                ContentData += str("    - 약간 나쁨 : 81 ~ 110") + str("\n")
                ContentData += str("    - 나쁨 : 111 ~ 150") + str("\n")
                ContentData += str("    - 매우 나쁨 : 151 ~") + str("\n\n")
                ContentData += str("오존 정보 : ") + str("\n")
                ContentData += str("    - 좋음 : 0 ~ 0.03") + str("\n")
                ContentData += str("    - 보통 : 0.03 ~ 0.09") + str("\n")
                ContentData += str("    - 약간 나쁨 : 0.09 ~ 0.11") + str("\n")
                ContentData += str("    - 나쁨 : 0.11 ~ 0.15") + str("\n")
                ContentData += str("    - 매우 나쁨 : 0.15 ~") + str("\n\n")
                ContentData += str("이산화질소 정보 : ") + str("\n")
                ContentData += str("    - 좋음 : 0 ~ 0.03") + str("\n")
                ContentData += str("    - 보통 : 0.03 ~ 0.06") + str("\n")
                ContentData += str("    - 약간 나쁨 : 0.06 ~ 0.1") + str("\n")
                ContentData += str("    - 나쁨 : 0.1 ~ 0.2") + str("\n")
                ContentData += str("    - 매우 나쁨 : 0.2 ~") + str("\n\n")
                ContentData += str("일산화탄소 정보 : ") + str("\n")
                ContentData += str("    - 좋음 : 0 ~ 2") + str("\n")
                ContentData += str("    - 보통 : 2 ~ 9") + str("\n")
                ContentData += str("    - 약간 나쁨 : 9 ~ 11") + str("\n")
                ContentData += str("    - 나쁨 : 11 ~ 15") + str("\n")
                ContentData += str("    - 매우 나쁨 : 15 ~") + str("\n\n")
                ContentData += str("이황산가스 정보 : ") + str("\n")
                ContentData += str("    - 좋음 : 0 ~ 0.02") + str("\n")
                ContentData += str("    - 보통 : 0.02 ~ 0.05") + str("\n")
                ContentData += str("    - 약간 나쁨 : 0.05 ~ 0.11") + str("\n")
                ContentData += str("    - 나쁨 : 0.11 ~ 0.15") + str("\n")
                ContentData += str("    - 매우 나쁨 : 0.15 ~") + str("\n\n")

            if self.textEdit.toPlainText() == "":
                QMessageBox.information(self, "미세먼지 주의보" , "수신할 이메일 주소를 적어주세요..!",QMessageBox.Yes)
            else:
                if sender.objectName() == "sendBtn" :
                    sendMail(self.textEdit.toPlainText(), self.SubjectText.toPlainText(), ContentData)
                    QMessageBox.information(self, "미세먼지 주의보" , "메일 발송을 완료 하였습니다..!",QMessageBox.Yes)
                else:
                    txtOut.txtOut(ContentData)
                    QMessageBox.information(self, "미세먼지 주의보" , "파일 저장을 완료하였습니다..!",QMessageBox.Yes)
                    pass
            pass

        if sender.objectName() == "searchBtn_2":    # 시/도 검색
            self.SearchData = "시도"
            self.LocationBoxData = self.LocationBox.currentText()
            self.DetailList.setGeometry(QtCore.QRect(10, 50, 371, 491))
            serverurl = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?ServiceKey="
            servervalue = "&sidoName=" + urlencode(self.LocationBoxData) + "&numOfRows=999&pageSize=999&pageNo=1&startPage=1"
            areaData = openAPItoXML(serverurl, self.serverKey, servervalue)
            self.DetailList.clear()
            addParsingDataList(areaData, "item", "stationName", self.DetailList)

        if sender.objectName() == "searchBtn":    # 지역 검색
            self.SearchData = "지역"
            self.DetailList.clear()
            self.DetailList.setGeometry(QtCore.QRect(10, 300, 371, 241))
            serverurl = "http://openapi.epost.go.kr/postal/retrieveLotNumberAdressService/retrieveLotNumberAdressService/getSiGunGuList?ServiceKey="
            servervalue = "&brtcCd=" + urlencode(self.LocationBox.currentText()) + "&numOfRows=999&pageSize=999&pageNo=1&startPage=1"
            self.LocationBoxData = self.LocationBox.currentText()
            self.LocationList.clear()
            areaData = openAPItoXML(serverurl, self.serverKey, servervalue)
            addParsingDataList(areaData, "siGunGuList", "signguCd", self.LocationList)

        if sender.objectName() == "saveBtn":    # 저장
            if self.DetailList.currentRow() == -1:
                QMessageBox.information(self, sender.text() , "동/읍/면 선택해주세요..!", QMessageBox.Yes)
            else:
                if self.SearchData == "지역":
                    self.DetailListData = self.DetailList.currentItem().text().replace("*", "")
                    self.Loaction.setText("%s %s %s" % (self.LocationBoxData, self.LocationListData, self.DetailListData))
                    self.Loaction.setText("%s %s %s" % (self.LocationBoxData, self.LocationListData, self.DetailListData))
                    QMessageBox.information(self, sender.text() , "위치를 저장하였습니다..!",QMessageBox.Yes)
                else:
                    self.DetailListData = self.DetailList.currentItem().text()
                    self.Loaction.setText("%s %s" % (self.LocationBoxData, self.DetailListData))
                    self.Loaction.setText("%s %s" % (self.LocationBoxData, self.DetailListData))
                    QMessageBox.information(self, sender.text() , "위치를 저장하였습니다..!",QMessageBox.Yes)



        if sender.objectName() == "refreshBtn" or int(indexBox) == int("1"):    # 오염정보 검색
            #------------------------------------------------------------------------------------------------------------------------
            serverurl = "https://apis.daum.net/local/geo/addr2coord?apikey="
            locationData = "" + self.LocationBoxData + " " + self.LocationListData + " " + self.DetailListData + ""
            servervalue = "&q=" + urlencode(locationData) + "&output=xml"
            areaData = openAPItoXML(serverurl, "d8807fd4a736291f4878c3cd37d8612d", servervalue)
            wgs84_x = addParsingDataString(areaData, "item", "point_x")
            wgs84_y = addParsingDataString(areaData, "item", "point_y")
            # ↑ 현재 지정된 주소를 wgs84 X, Y  좌표를 받아온다.
            
            serverurl = "https://apis.daum.net/local/geo/transcoord?apikey="
            servervalue = "&fromCoord=WGS84&y=" + wgs84_y + "&x=" + wgs84_x + "&toCoord=TM&output=xml"
            areaData = openAPItoXML(serverurl, "d8807fd4a736291f4878c3cd37d8612d", servervalue)
            tm_x =  stringSplit(areaData, "x='" , "'")
            tm_y = stringSplit(areaData, "y='" , "'")
            # ↑ 받아온 X, Y 좌표를 TM 좌표로 변환한다.

            serverurl = "http://openapi.airkorea.or.kr/openapi/services/rest/MsrstnInfoInqireSvc/getNearbyMsrstnList?ServiceKey="
            servervalue = "&tmX=" + tm_x[0] + "&tmY=" + tm_y[0] + "&numOfRows=999&pageSize=999&pageNo=1&startPage=1"
            areaData = openAPItoXML(serverurl, self.serverKey, servervalue)
            realLocationData = addParsingDataString(areaData, "item", "stationName") # 실제 측정소 위치
            writeLabelWidget(self.realLocation, "실제 측정소 : %s" % realLocationData)
            # ↑ 변환된 좌표로 해당 TM 위치에서 가장 가까운 측정소를 가져와 설정을 한다.
            #------------------------------------------------------------------------------------------------------------------------

            serverurl = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?ServiceKey="
            servervalue = "&stationName=" + urlencode(realLocationData) + "&dataTerm=month&pageNo=1&numOfRows=10&ver=1.2&"
            areaData = openAPItoXML(serverurl, self.serverKey, servervalue)

            self.khaiValue = addParsingDataString(areaData, "item", "khaiValue") # 통합 지수
            self.khaiValueData = returnState("khaiValue", self.khaiValue)
            self.pm10Value24 = addParsingDataString(areaData, "item", "pm10Value24") # pm10 지수
            self.pm10Value24Data = returnState("pm10Value24", self.pm10Value24)
            self.o3Value = addParsingDataString(areaData, "item", "o3Value") # O3 지수
            self.o3ValueData = returnState("o3Value", self.o3Value)
            self.no2Value = addParsingDataString(areaData, "item", "no2Value") # NO2 지수
            self.no2ValueData = returnState("no2Value", self.no2Value)
            self.coValue = addParsingDataString(areaData, "item", "coValue") # CO 지수
            self.coValueData = returnState("coValue", self.coValue)
            self.so2Value = addParsingDataString(areaData, "item", "so2Value") # SO2 지수
            self.so2ValueData = returnState("so2Value", self.so2Value)

            writeLabelWidget(self.getTime, "측정 시간 : %s" % addParsingDataString(areaData, "item", "dataTime"))
            writeLabelWidget(self.totalValue, "통합지수 : " + str(self.khaiValue) + "㎍/㎥", returnRGB(self.khaiValueData))
            writeLabelWidget(self.PM10Label, str(self.pm10Value24) + "㎍/㎥", returnRGB(self.pm10Value24Data))
            writeLabelWidget(self.o3Label, str(self.o3Value) + "ppm", returnRGB(self.o3ValueData))
            writeLabelWidget(self.No2Label, str(self.no2Value) + "ppm",  returnRGB(self.no2ValueData))
            writeLabelWidget(self.CoLabel, str(self.coValue) + "ppm", returnRGB(self.coValueData))
            writeLabelWidget(self.So2Label, str(self.so2Value) + "ppm", returnRGB(self.so2ValueData))

            # 이모티콘 관련 하여 아래로.
            writeImageWidget(self.emoIcon,"/Img/emoticon/", self.khaiValueData, "png") # 통합 지수 관련 이미지
            writeImageWidget(self.emoIcon_2,"/Img/emoticon/resize/", self.pm10Value24Data, "png") # PM10
            writeImageWidget(self.emoIcon_3,"/Img/emoticon/resize/", self.o3ValueData, "png") # O3
            writeImageWidget(self.emoIcon_4,"/Img/emoticon/resize/", self.no2ValueData, "png") # NO2
            writeImageWidget(self.emoIcon_5,"/Img/emoticon/resize/", self.coValueData, "png") # CO
            writeImageWidget(self.emoIcon_6,"/Img/emoticon/resize/", self.so2ValueData, "png") # SO2

            if sender.objectName() == "refreshBtn":
                QMessageBox.information(self, "미세먼지 주의보" , "갱신을 완료하였습니다..!",QMessageBox.Yes)


        if sender.objectName() == "refreshBtn_2" or int(indexBox) == int("2"):    # 미세먼지 검색
            now = time.localtime()
            dmon = now.tm_mon
            dday = now.tm_mday
            if now.tm_mon < 10 : dmon = str("0" + str(now.tm_mon))
            if now.tm_mday < 10 : dday = str("0" + str(now.tm_mday))
            nowdate = str(now.tm_year) + "-" + str(dmon) + "-" + str(dday)
            serverurl = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMinuDustFrcstDspth?ServiceKey="
            servervalue = "&searchDate=" + urlencode(nowdate) + ""
            areaData = openAPItoXML(serverurl, self.serverKey, servervalue)

            totalCount = addParsingDataString(areaData, "body", "totalCount")
            if int(totalCount) != 0: #예보가 있을경우에만 표시한다.
                download_image(str(addParsingDataString(areaData, "items", "imageUrl1")), "pm10") # pm10 이미지 다운로드
                writeImageWidget(self.pm10_img,"/", "pm10", "png")

                writeLabelWidget(self.today_date, "%s" % addParsingDataString(areaData, "item", "dataTime"))
                self.informOverall.setPlainText("%s" % addParsingDataString(areaData, "item", "informOverall"))
                self.informCause.setPlainText("%s" % addParsingDataString(areaData, "item", "informCause"))
                self.informGrade.setPlainText("%s" % str(addParsingDataString(areaData, "item", "informGrade")).replace(",", ", "))
                if sender.objectName() == "refreshBtn_2":
                    QMessageBox.information(self, "미세먼지 주의보" , "갱신을 완료하였습니다..!",QMessageBox.Yes)
            else:
                QMessageBox.information(self, "미세먼지 주의보" , "현재 예보가 없습니다..!",QMessageBox.Yes)


    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.splitdata = myIPLocation() # 내위치를 가져오기
        self.LocationBoxData = self.splitdata[0] # 시/도 구역 설정
        self.LocationListData = self.splitdata[1] # 시/군/구 구역 설정
        self.DetailListData = self.splitdata[2] # 동/읍/면 구역 설정

        self.khaiValue = "" # 통합 지수
        self.pm10Value24 = "" # pm10 지수
        self.o3Value = "" # O3 지수
        self.no2Value = "" # NO2 지수
        self.coValue = "" # CO 지수
        self.so2Value = "" # SO2 지수

        self.myLocationData = self.LocationBoxData + " " + self.LocationListData + " " + self.DetailListData
        self.SearchData = "지역"
        self.serverKey = "agRTEvpQv1bNvtoPQr3DNvE5juZ9EAws47JkmLbQnf4OYYAXw%2FAh9TULJtGxrEBzqH2767koxGlukyRTjweQcg%3D%3D"
        self.setupUi(self)
        self.pm10_img.setScaledContents(True);
        writeImageWidget(self.dustState,"/Img/", "state_img3", "png") # pm10 관련 이미지 추가
        
        
        writeImageWidget(self.PM10_Info,"/Img/","PM10_Info","png")
        self.PM10_Info.setScaledContents(True);
        

        koreaArea = ["서울", "강원", "인천", "경기", "충북", "충남",
                          "경북", "대전", "대구", "전북", "경남", "울산",
                          "광주", "부산", "전남", "제주"]
        for data in koreaArea: 
            self.LocationBox.addItem(data)

        self.LocationList.clicked.connect(self.ListClicked)
        self.searchBtn.clicked.connect(self.BtnClicked)
        self.searchBtn_2.clicked.connect(self.BtnClicked)
        self.saveBtn.clicked.connect(self.BtnClicked)
        self.saveBtn_2.clicked.connect(self.BtnClicked)
        self.refreshBtn_2.clicked.connect(self.BtnClicked)
        self.refreshBtn.clicked.connect(self.BtnClicked)
        self.Loaction.setText(self.myLocationData)
        self.tabWidget.currentChanged.connect(self.BtnClicked)
        self.sendBtn.clicked.connect(self.BtnClicked)

        self.emoIcon.setAutoFillBackground(False)
        self.emoIcon_2.setAutoFillBackground(False)
        self.emoIcon_3.setAutoFillBackground(False)
        self.emoIcon_4.setAutoFillBackground(False)
        self.emoIcon_5.setAutoFillBackground(False)
        self.emoIcon_6.setAutoFillBackground(False)
        
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.setWindowIcon(QIcon('./Img/main_icon.png'))
    form.show()
    sys.exit(app.exec_())



