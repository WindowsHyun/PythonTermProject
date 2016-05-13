import urllib.request
import string
import codecs
from xml.dom.minidom import *

#���ڵ�
def urlencode(string):
    return urllib.parse.quote(string)

#���ڵ�
def urldecode(string):
    return urllib.parse.quote(string)

def myIPLocation():
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')]
    # �� User-Agent�� �Է����� ������� naver.com ���� �������� ������ �ƴѰ����� �Ǵ��Ͽ� ������ �Ѵ�.
    data = ""
    with opener.open('http://map.naver.com') as f:
        data = f.read(300000).decode('utf-8') # 300000bytes �� utf-8�� ��ȯ�Ͽ� �о�´�.  ��ȯ�� ������� unicode�� �޾ƿ´�.
    
    p1 = data.find("<span class=\"blind\">") + 20 # ���� ��ġ�� ��Ÿ�� �ִ� ������ ��ġ�� ���Ѵ�.
    data = data[p1:p1 + 50] # �ش� ���� ��ġ���� 50���ڸ� data�� �ִ´�.
    p2 = data.find("</span>")

    return data[:p2]

def openAPItoXML(server, key, value):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')]
    # �� User-Agent�� �Է����� ������� naver.com ���� �������� ������ �ƴѰ����� �Ǵ��Ͽ� ������ �Ѵ�.
    data = ""
    urldata = server + key + value
    with opener.open(urldata) as f:
        data = f.read(300000).decode('utf-8') # 300000bytes �� utf-8�� ��ȯ�Ͽ� �о�´�.  ��ȯ�� ������� unicode�� �޾ƿ´�.
    return data

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