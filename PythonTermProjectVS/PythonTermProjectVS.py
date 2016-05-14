# -*- coding: utf-8 -*-
import sys
import urllib

import GUI
from ParsingData import *
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
        if sender.text() == "시도 검색":
            self.SearchData = "시도"
            self.LocationBoxData = self.LocationBox.currentText()
            self.DetailList.setGeometry(QtCore.QRect(10, 50, 371, 491))
            serverurl = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?ServiceKey="
            servervalue = "&sidoName=" + urlencode(self.LocationBoxData) + "&numOfRows=999&pageSize=999&pageNo=1&startPage=1"
            areaData = openAPItoXML(serverurl, self.serverKey, servervalue)
            self.DetailList.clear()
            addParsingDataList(areaData, "item", "stationName", self.DetailList)

        if sender.text() == "지역 검색":
            self.SearchData = "지역"
            self.DetailList.clear()
            self.DetailList.setGeometry(QtCore.QRect(10, 300, 371, 241))
            serverurl = "http://openapi.epost.go.kr/postal/retrieveLotNumberAdressService/retrieveLotNumberAdressService/getSiGunGuList?ServiceKey="
            servervalue = "&brtcCd=" + urlencode(self.LocationBox.currentText()) + "&numOfRows=999&pageSize=999&pageNo=1&startPage=1"
            self.LocationBoxData = self.LocationBox.currentText()
            self.LocationList.clear()
            areaData = openAPItoXML(serverurl, self.serverKey, servervalue)
            addParsingDataList(areaData, "siGunGuList", "signguCd", self.LocationList)

        if sender.text() == "저장":
            if self.DetailList.currentRow() == -1:
                QMessageBox.information(self, sender.text() , "동/읍/면 선택해주세요..!", QMessageBox.Yes)
            else:
                if self.SearchData == "지역":
                    self.DetailListData = self.DetailList.currentItem().text().replace("*", "")
                    self.Loaction.setText("%s %s %s" % (self.LocationBoxData, self.LocationListData, self.DetailListData))
                    QMessageBox.information(self, sender.text() , "위치를 저장하였습니다..!",QMessageBox.Yes)
                else:
                    self.DetailListData = self.DetailList.currentItem().text()
                    self.Loaction.setText("%s %s" % (self.LocationBoxData, self.DetailListData))
                    QMessageBox.information(self, sender.text() , "위치를 저장하였습니다..!",QMessageBox.Yes)


        if sender.text() == "갱신":
            serverurl = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?ServiceKey="
            servervalue = "&stationName=" + urlencode(self.DetailListData) + "&numOfRows=1&pageSize=1&pageNo=1&startPage=1&dataTerm=DAILY"
            areaData = openAPItoXML(serverurl, self.serverKey, servervalue)
            self.getTime.setText("측정 시간 : %s" % addParsingDataString(areaData, "item", "dataTime"))
            self.totalLabel.setText(addParsingDataString(areaData, "item", "khaiValue"))
            self.totalLabel.setStyleSheet('color: rgb(255, 0, 0);')
            self.pm10Label.setText(addParsingDataString(areaData, "item", "pm10Value"))
            self.pm10Label.setStyleSheet('color: rgb(207, 78, 78);')
            self.o3Label.setText(addParsingDataString(areaData, "item", "o3Value"))
            self.o3Label.setStyleSheet('color: rgb(0, 162, 232);')
            self.No2Label.setText(addParsingDataString(areaData, "item", "no2Value"))
            self.No2Label.setStyleSheet('color: rgb(255, 127, 39);')
            self.CoLabel.setText(addParsingDataString(areaData, "item", "coValue"))
            self.CoLabel.setStyleSheet('color: rgb(34, 177, 76);')
            self.So2Label.setText(addParsingDataString(areaData, "item", "so2Value"))
            self.So2Label.setStyleSheet('color: rgb(0, 162, 232);')
            QMessageBox.information(self, sender.text() , "갱신을 완료하였습니다..!",QMessageBox.Yes)
            pass

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.splitdata = myIPLocation() # 내위치를 가져오기
        self.LocationBoxData = self.splitdata[0] # 시/도 구역 설정
        self.LocationListData = self.splitdata[1] # 시/군/구 구역 설정
        self.DetailListData = self.splitdata[2] # 동/읍/면 구역 설정
        self.myLocationData = self.LocationBoxData + " " + self.LocationListData + " " + self.DetailListData
        self.SearchData = "지역"
        self.serverKey = "agRTEvpQv1bNvtoPQr3DNvE5juZ9EAws47JkmLbQnf4OYYAXw%2FAh9TULJtGxrEBzqH2767koxGlukyRTjweQcg%3D%3D"
        self.setupUi(self)
        self.dust_icon.setPixmap(QPixmap('./Img/dust_icon.png')) # fore_icon 관련 이미지 추가
        self.fore_icon.setPixmap(QPixmap('./Img/fore_icon.png')) # fore_icon 관련 이미지 추가
        self.GPSImage.setPixmap(QPixmap('./Img/station_icon.png')) # GPS 관련 이미지 추가
        self.stateImg.setPixmap(QPixmap('./Img/state_img.png')) # 상태 관련 이미지 추가
        koreaArea = ["서울", "강원", "인천", "경기", "충북", "충남",
                          "경북", "대전", "대구", "전북", "경남", "울산",
                          "광주", "부산", "전남", "제주"]
        for data in koreaArea: 
            self.LocationBox.addItem(data)

        self.LocationList.clicked.connect(self.ListClicked)
        self.searchBtn.clicked.connect(self.BtnClicked)
        self.searchBtn_2.clicked.connect(self.BtnClicked)
        self.saveBtn.clicked.connect(self.BtnClicked)
        self.refreshBtn.clicked.connect(self.BtnClicked)
        self.Loaction.setText(self.myLocationData)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())



