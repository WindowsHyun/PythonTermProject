import urllib.request
import string
import codecs
import smtplib
import base64
from xml.dom.minidom import *
from PyQt5.QtGui import *
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

def Base64_Encode(s):
    return base64.b64encode(s.encode('utf-8'))

def Base64_Decode(b):
    return base64.b64decode(b).decode('utf-8')


def sendMail(ReviceMail, Subject, Content):
    s = smtplib.SMTP("smtp.gmail.com",587) #SMTP 서버 설정
    s.starttls() #STARTTLS 시작
    s.login( Base64_Decode("YW5reW9uZzk5QGdtYWlsLmNvbQ=="),Base64_Decode("YW5reW9uZzk="))
    contents = Content
    msg = MIMEText(contents, _charset='euc-kr')
    msg['Subject'] = Subject
    msg['From'] = Base64_Decode("YW5reW9uZzk5QGdtYWlsLmNvbQ==")
    msg['To'] = ReviceMail
    s.sendmail( Base64_Decode("YW5reW9uZzk5QGdtYWlsLmNvbQ==") , ReviceMail, msg.as_string())


def returnRGB(value):
    # 상태에 따라서 RGB 색상을 리스트 형식으로 다르게 리턴 한다.
    if value == 0:
        rgbList = [0, 162, 232]
        return rgbList
    if value == 1:
        rgbList = [34, 177, 76]
        return rgbList
    if value == 2:
        rgbList = [255, 127, 39]
        return rgbList
    if value == 3:
        rgbList = [207, 78, 78]
        return rgbList
    if value == 4:
        rgbList = [255, 0, 0]
        return rgbList

def returnState(selectData, value):
    # 조회된 결과에 따라서 상태를 return 값으로 반환을 한다.
    try:
        value = float(value)
    except:
        value = 0
    
    khaiValue = [0, 50, 100, 210, 250, 999]
    pm10Value24 = [0, 30, 80, 110, 150, 999]
    o3Value = [0, 0.03, 0.09, 0.11, 0.15, 999]
    no2Value = [0, 0.03, 0.06, 0.1, 0.2, 999]
    coValue = [0, 2, 9, 11, 15, 999]
    so2Value = [0, 0.02, 0.05, 0.11, 0.15, 999]

    for i in range(0, 5):
        if selectData == "khaiValue":
            if  khaiValue[i] <= value < khaiValue[i + 1]  :
                return i
        elif selectData == "pm10Value24":
            if  pm10Value24[i] <= value < pm10Value24[i + 1]  :
                return i
        elif selectData == "o3Value":
            if  o3Value[i] <= value < o3Value[i + 1]  :
                return i
        elif selectData == "no2Value":
            if  no2Value[i] <= value < no2Value[i + 1]  :
                return i
        elif selectData == "coValue":
            if  coValue[i] <= value < coValue[i + 1]  :
                return i
        elif selectData == "so2Value":
            if  so2Value[i] <= value < so2Value[i + 1]  :
                return i


def writeLabelWidget(Widget, Content="None", RGB=[86, 86, 86]):
    # 레이블에 글을 작성해준다. 색상 지정이 없을경우 기본 색상은 rgb(86,86,86) 이다.
    Widget.setText(str(Content))
    Widget.setStyleSheet('color: rgb(' + str(RGB[0]) + ',' + str(RGB[1]) + ',' + str(RGB[2]) + ',);')

def writeImageWidget(Widget, Address, File, Extension):
    # 레이블에 이미지를 넣어준다. 파일 주소, 파일명, 확장자 순으로 받아서 넣어준다.
    Widget.setPixmap(QPixmap('.' + str(Address) + str(File) + '.' + str(Extension)))
        
def urlencode(string):
    # URL 인코딩
    return urllib.parse.quote(string)

def urldecode(string):
    # URL 디코딩
    return urllib.parse.quote(string)

def myIPLocation():
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')]
    # ↑ User-Agent를 입력하지 않을경우 naver.com 에서 정상적인 접근이 아닌것으로 판단하여 차단을 한다.
    data = ""
    with opener.open('http://map.naver.com') as f:
        data = f.read(300000).decode('utf-8') # 300000bytes 를 utf-8로 변환하여 읽어온다.  변환이 없을경우 unicode로 받아온다.
    
    p1 = data.find("<span class=\"blind\">") + 20 # 현재 위치를 나타내 주는 글자의 위치를 구한다.
    data = data[p1:p1 + 50] # 해당 글자 위치에서 50글자를 data에 넣는다.
    p2 = data.find("</span>")
    return data[:p2].split()

def openAPItoXML(server, key, value):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')]
    # ↑ User-Agent를 입력하지 않을경우 naver.com 에서 정상적인 접근이 아닌것으로 판단하여 차단을 한다.
    data = ""
    urldata = server + key + value
    with opener.open(urldata) as f:
        data = f.read(300000).decode('utf-8') # 300000bytes 를 utf-8로 변환하여 읽어온다.  변환이 없을경우 unicode로 받아온다.
    return data

def addParsingDicList(xmlData, motherData, childData):
    # 파싱된 데이터를 리스트에 넣어서 리턴 한다.
    doc = parseString(xmlData)
    siGunGuList = doc.getElementsByTagName(motherData)
    signguCdSize = len(siGunGuList)
    list = []
    for index in range(signguCdSize):
        mphms = siGunGuList[index].getElementsByTagName(childData)
        list.append(str(mphms[0].firstChild.data))
    return list

def addParsingDataList(xmlData, motherData, childData, addList):
    # 파싱된 데이터를 QtWidget 리스트에 넣어준다.
    doc = parseString(xmlData)
    siGunGuList = doc.getElementsByTagName(motherData)
    signguCdSize = len(siGunGuList)
    for index in range(signguCdSize):
        mphms = siGunGuList[index].getElementsByTagName(childData)
        addList.addItem(str(mphms[0].firstChild.data))

def addParsingDataString(xmlData, motherData, childData):
    # 파싱된 데이터를 string 형태로 리턴 한다.
    doc = parseString(xmlData)
    siGunGuList = doc.getElementsByTagName(motherData)
    signguCdSize = len(siGunGuList)
    for index in range(signguCdSize):
        mphms = siGunGuList[index].getElementsByTagName(childData)
        return str(mphms[0].firstChild.data)

def compareListAdd(ListA, ListB, AddList, Word):
        temp = ""
        for i in ListA:
            for j in ListB:
                if j == i:
                    AddList.addItem(Word + i)
                    temp = i
            if i != temp:
                AddList.addItem(i)