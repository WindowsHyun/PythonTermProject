# -*- coding: utf-8 -*-
import sys
import urllib

import GUI
from ParsingData import *

from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
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
        serverkey = "agRTEvpQv1bNvtoPQr3DNvE5juZ9EAws47JkmLbQnf4OYYAXw%2FAh9TULJtGxrEBzqH2767koxGlukyRTjweQcg%3D%3D"
        servervalue = "&brtcCd=" + urlencode(self.LocationData) + "&signguCd=" + urlencode(list.text()) +  "&numOfRows=999&pageSize=999&pageNo=1&startPage=1"
        self.DetailData = list.text()
        self.DetailList.clear()
        areaData = openAPItoXML(serverurl, serverkey, servervalue)
        addParsingDataList(areaData, "eupMyunDongList", "emdCd", self.DetailList)


    def BtnClicked(self):
        sender = self.sender()
        if sender.text() == "검색":
            serverurl = "http://openapi.epost.go.kr/postal/retrieveLotNumberAdressService/retrieveLotNumberAdressService/getSiGunGuList?ServiceKey="
            serverkey = "agRTEvpQv1bNvtoPQr3DNvE5juZ9EAws47JkmLbQnf4OYYAXw%2FAh9TULJtGxrEBzqH2767koxGlukyRTjweQcg%3D%3D"
            servervalue = "&brtcCd="+ urlencode(self.LocationBox.currentText()) +  "&numOfRows=999&pageSize=999&pageNo=1&startPage=1"
            self.LocationData = self.LocationBox.currentText()
            self.LocationList.clear()
            areaData = openAPItoXML(serverurl, serverkey, servervalue)
            addParsingDataList(areaData, "siGunGuList", "signguCd", self.LocationList)

        if sender.text() == "저장":
            if self.DetailList.currentRow() == -1:
                QMessageBox.information(self, sender.text() , "동/읍/면 선택해주세요..!", QMessageBox.Yes)
            else:
                QMessageBox.information(self, sender.text() , "%s %s %s 맞나요?" % (self.LocationData, self.DetailData, self.DetailList.currentItem().text()), QMessageBox.Yes)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.myLocationData = myIPLocation() # 내위치를 가져오기
        self.LocationData = "" # 서울시 처럼 데이터를 기억하기
        self.DetailData = "" # 읍,면,동 데이터를 기억하기
        self.setupUi(self)
        self.dust_icon.setPixmap(QPixmap('./Img/dust_icon.png')) # fore_icon 관련 이미지 추가
        self.fore_icon.setPixmap(QPixmap('./Img/fore_icon.png')) # fore_icon 관련 이미지 추가
        self.GPSImage.setPixmap(QPixmap('./Img/station_icon.png')) # GPS 관련 이미지 추가
        self.stateImg.setPixmap(QPixmap('./Img/state_img.png')) # 상태 관련 이미지 추가
        koreaArea = ["서울", "강원", "인천", "경기", "충북", "충남",
                          "경북", "대전", "대구", "전북", "경남", "울산",
                          "광주", "부산", "전남", "제주" ]
        for data in koreaArea: 
            self.LocationBox.addItem(data)

        self.searchBtn.clicked.connect(self.BtnClicked)
        self.LocationList.clicked.connect(self.ListClicked)
        self.saveBtn.clicked.connect(self.BtnClicked)
        self.Loaction.setText(self.myLocationData)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())



