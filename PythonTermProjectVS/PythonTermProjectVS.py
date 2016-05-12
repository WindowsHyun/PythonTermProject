import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

app = QApplication(sys.argv)
form = QLabel("Visual Studio 2015 Python GUI PyQt5 Test Program")
form.show()
app.exec_()