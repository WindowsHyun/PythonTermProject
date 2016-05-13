import sys
import GUI

from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit
from PyQt5.QtWidgets import QTextEdit, QWidget, QDialog, QApplication, QMessageBox

class MainWindow(QDialog, GUI.Ui_Dialog):
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '미세먼지 주의보', "정말 종료할까요?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept() 
        else:
            event.ignore()      

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.dust_icon.setPixmap(QPixmap('./Img/dust_icon.png')) # fore_icon 관련 이미지 추가
        self.fore_icon.setPixmap(QPixmap('./Img/fore_icon.png')) # fore_icon 관련 이미지 추가
        self.GPSImage.setPixmap(QPixmap('./Img/station_icon.png')) # GPS 관련 이미지 추가
        self.stateImg.setPixmap(QPixmap('./Img/state_img.png')) # 상태 관련 이미지 추가
        koreaArea = ["서울특별시", "경기도", "인천광역시", "강원도", "충청남도", "대전광역시",
                          "충청북도", "경상북도", "대구광역시", "전라북도", "광주광역시", "전라남도",
                          "경상남도", "울산광역시", "부산광역시", "제주도" ]
        for data in koreaArea: 
            self.LocationBox.addItem(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = MainWindow()
    form.show()

    sys.exit(app.exec_())
