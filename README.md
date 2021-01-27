#### 📌주제 : 배스킨라빈스 31 아이스크림 추천 웹 (아이스크림 필터링해주는)

#### 📌 프로젝트 이름 : MyPick-31 🍨

------

> 📌 빌드업

프론트엔드 (HTML, CSS , JS) / 백엔드(Flask, Mysql, Python) / 서버(AWS?)

> 📌 기한

9월 21일 ~ 10월 21일 (최대 10월 31일까지 마무리)

> 📌 목표 

런칭(도메인 구매해서 올리는 것까지)

> 📌 기본 지식

배라의 아이스크림은, 시그니처(상시 배치) / 시즌 (계절용) 으로 구성되어있다.

아이스크림의 구분은 "베이스 / 첨가물" 로 구분하면 된다. ex) 엄마는 외계인 = 베이스(다크, 밀크, 화이트 초콜릿) + 첨가물 (초코볼)

1. 원하는 아이스크림의 베이스를 고른다.
ex) 치즈 / 민트 / 녹차 / 바닐라 / 커피 / 초콜릿 / 과일(과일은 종류가 많아서, 과일 탭을 누르면 하단에 다양한 과일 종류등이 나오는 방식으로 진행해야할듯) 등

2. 선호하는 토핑을 고른다. ex) 토핑 x / 견과류 토핑 / 과일 토핑 / 캔디 토핑 / 초콜릿 토핑 등

> 📌 기능

- 좋아요 기능

하트 누르면, 아이스크림 DB에 있는(아니면, 좋아요DB에 있는) 좋아요 정보가 카운팅
→ 좋아요 갯수대로 인기 아이스크림 목록 사용시 정렬
→ 항목으로 여러 개의 정보가 나오면, 좋아요를 바탕으로 순서대로 정렬

>  📌 UX/UI

- 배스킨라빈스의 느낌을 살릴 수 있는 UX/UI

→ 글자는 "배라 폰트" 를 사용한다. 해당 폰트는 배라 공식 홈페이지에서 다운받을 수 있다.
→ 배라에서 많이 사용하는 색깔을 활용한 홈페이지 색깔 설계 (분홍색/남색/파란색)
→ 아이스크림 관련된 물품(컵/스푼 같은 것들)들을 활용한 버튼 설계

###### (Home Page _ ver.PC)
![Home_verPC](/uploads/Home_verPC.PNG){: width="300" height="300"}

###### (Home Page _ ver.Mobile)
![Home_verMobile](/uploads/Home_verMobile.PNG)

###### (MenuBar)
![menu_bar](/uploads/menu_bar.PNG)

###### (Register Page)
![register](/uploads/register.PNG)

###### (Login Page)
![login](/uploads/login.PNG)

###### (Insert_Date Page)
![insert_data](/uploads/insert_data.PNG)

###### (About Page)
![about](/uploads/about.PNG)

>  📌 DB 설계 (MySQL)

##### 🍨 아이스크림 DB
- 이름 / 베이스 / 토핑 / 칼로리 / 알레르기 성분 / 좋아요 갯수(좋아요 DB를 새롭게 팔지?) / 사진

##### 📝 리뷰 DB
- 크롤링을 해서 실시간 신규 리뷰 정보를 가져올지 (-> DB 필요없음.)
- 크롤링 해서 리뷰DB에 넣어서 보관 (-> 주기적으로 업데이트를 해줘야함. 옛날 리뷰들만 계속 보임.)

##### 👍🏻 좋아요 DB
- 좋아요 DB를 따로 파서 사용할 것이라면, 아이스크림 이름/좋아요 갯수 정도로 DB 구성해야함.
