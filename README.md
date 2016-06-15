# PythonTermProject [미세먼지 주의보]

각 지역별 오염 정보를 확인하여 검색된 위치에 "좋음~매우나쁨"까지 확인할수 있다.
![Image01](https://github.com/WindowsHyun/PythonTermProject/blob/master/Image/newex_UI.png?raw=true)
![Image02](https://github.com/WindowsHyun/PythonTermProject/blob/master/Image/newex_UI2.png?raw=true)
![Image03](https://github.com/WindowsHyun/PythonTermProject/blob/master/Image/newex_UI3.png?raw=true)

----------
개발자
----------
+ 2012180004 권창현
+ 2012181042 황성섭

---------
개발 환경
---------
+ Visual Studio 2015 (Python Tools)
+ Python 3.5.1
+ pyqt 5 (GUI)

---------
사용하는 API
---------
 + [대기오염정보 조회 서비스](https://www.data.go.kr/subMain.jsp#/L3B1YnIvdXNlL3ByaS9Jcm9zT3BlbkFwaURldGFpbC9vcGVuQXBpTGlzdFBhZ2UkQF4wMTJtMjEkQF5wdWJsaWNEYXRhUGs9MTUwMDA1ODEkQF5icm1DZD1PQzAwMTIkQF5tYWluRmxhZz10cnVl) - 각 측정소별 대기오염정보를 조회하기 위한 서비스로 기간별, 시도별 대기오염 정보와 민감군 이상 측정소 내역, 미세먼지 예보 통보 내역을 조회할 수 있다.
 + [측정소정보 조회 서비스](https://www.data.go.kr/subMain.jsp?param=T1BFTkFQSUAxNTAwMDY2MA==#/L3B1YnIvdXNlL3ByaS9Jcm9zT3BlbkFwaURldGFpbC9vcGVuQXBpTGlzdFBhZ2UkQF4wMTJtMSRAXnB1YmxpY0RhdGFQaz0xNTAwMDY2MCRAXmJybUNkPU9DMDAxMiRAXnJlcXVlc3RDb3VudD00NTUkQF5vcmdJbmRleD1PUEVOQVBJ) - 대기질 측정소 정보를 조회하기 위한 서비스로 TM 좌표기반의 가까운 측정소 및 측정소 목록과 측정소의 정보를 조회할 수 있다.
 + [지번주소조회 서비스](https://www.data.go.kr/subMain.jsp#/L3B1YnIvdXNlL3ByaS9Jcm9zT3BlbkFwaURldGFpbC9vcGVuQXBpTGlzdFBhZ2UkQF4wMTJtMjEkQF5wdWJsaWNEYXRhUGs9MTUwMDAyNjgkQF5icm1DZD1PQzAwMTEkQF5tYWluRmxhZz10cnVl) - 우정사업본부에서는 현재 운영되고 있는 지번주소체계의 새우편번호(2015.8.1 시행) 및 기존우편번호를 조회하는 기능을 제공합니다.
 + [좌표계 변환, 좌표->현재위치](https://developers.daum.net/services/apis/local/geo/transcoord) - 좌표계 변환API는 입력한 좌표를 다른 좌표계의 좌표, 좌표→주소 변환API는 좌표를 입력하면 그에 해당하는 주소로 변경시킬 수 있습니다. XML, JSON(P) 형식으로 결과를 반환합니다.


---------
구현 내용
---------
 1. pyqt 5를 통한 GUI 제작
 2. Open API를 통한 위치별 미세먼지 농도를 받아오기
 3. Gmail 을 통한 현재 미세먼지 농도 등의 값을 전송하기
 4. IP 위치를 기반으로한 자신의 위치 확인
 5. IP 위치를 기반 현재 위치에서 가장 가까운 측정소 찾기
 6. C/C++ 함수 혹은 라이브러리 연동
 7. distutils 모듈을 활용한 개발 패키지 배포

---------
구현 예정 내용
---------
 1. -

---------
Youtube 업로드 영상 & PPT 자료
---------
+ [1차 발표 PPT](https://github.com/WindowsHyun/PythonTermProject/blob/master/Documnet/%5B1%EC%B0%A8%5D%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8%20%EC%96%B8%EC%96%B4%20%ED%85%80%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%20%EA%B8%B0%ED%9A%8D.pptx?raw=true) / [1차 발표 영상](https://www.youtube.com/watch?v=pi8r_2Kas5w)
+ [2차 발표 PPT](https://github.com/WindowsHyun/PythonTermProject/blob/master/Documnet/%5B2%EC%B0%A8%5D%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8%20%EC%96%B8%EC%96%B4%20%ED%85%80%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%20%EA%B8%B0%ED%9A%8D.pptx?raw=true) / [2차 발표 영상](https://www.youtube.com/watch?v=mdKP4wjipv4&feature=youtu.be)
+ [최종 발표 PPT](https://github.com/WindowsHyun/PythonTermProject/blob/master/Documnet/%5B%EC%B5%9C%EC%A2%85%5D%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8%20%EC%96%B8%EC%96%B4%20%ED%85%80%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%20%EA%B8%B0%ED%9A%8D.pptx?raw=true) / [최종 발표 영상](https://www.youtube.com/watch?v=FBcoujWzhKo)



