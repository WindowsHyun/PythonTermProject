import urllib.request
import string
import codecs
from xml.dom.minidom import *

#인코딩
def urlencode(string):
    return urllib.parse.quote(string)

#디코딩
def urldecode(string):
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
    doc = parseString(xmlData)
    siGunGuList = doc.getElementsByTagName(motherData)
    signguCdSize = len(siGunGuList)
    list = []
    for index in range(signguCdSize):
        mphms = siGunGuList[index].getElementsByTagName(childData)
        list.append(str(mphms[0].firstChild.data))
    return list

def addParsingDataList(xmlData, motherData, childData, addList):
    doc = parseString(xmlData)
    siGunGuList = doc.getElementsByTagName(motherData)
    signguCdSize = len(siGunGuList)
    for index in range(signguCdSize):
        mphms = siGunGuList[index].getElementsByTagName(childData)
        addList.addItem(str(mphms[0].firstChild.data))

def addParsingDataString(xmlData, motherData, childData):
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