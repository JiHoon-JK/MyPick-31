# 📌 프로젝트 이름 : MyPick-31 🍨

베스킨라빈스 31 아이스크림 추천 웹 (아이스크림 필터링)

<br/>

> 📌 빌드업

프론트엔드 (HTML, CSS , JS) / 백엔드(Flask, MongoDB, Python) <br/><br/>



> 📌 기한

9월 21일 ~ 10월 21일 (최대 10월 31일까지 마무리)  <br/><br/>




> 📌 목표 

프로젝트 기능 구현 / 런칭 전까지 모든 기능 구현  <br/><br/>




> 📌 기본 지식

배라의 아이스크림은, 시그니처(상시 배치) / 시즌 (계절용) 으로 구성되어있다.

아이스크림의 구분은 "베이스 / 첨가물" 로 구분하면 된다. ex) 엄마는 외계인 = 베이스(다크, 밀크, 화이트 초콜릿) + 첨가물 (초코볼)

1. 원하는 아이스크림의 베이스를 고른다.
ex) 치즈 / 민트 / 녹차 / 바닐라 / 커피 / 초콜릿 / 과일(과일은 종류가 많아서, 과일 탭을 누르면 하단에 다양한 과일 종류등이 나오는 방식으로 진행해야할듯) 등

2. 선호하는 토핑을 고른다. ex) 토핑 x / 견과류 토핑 / 과일 토핑 / 캔디 토핑 / 초콜릿 토핑 등  <br/><br/>




> 📌 기능

- 아이스크림 필터 기능

유저가 선호하는 베이스, 토핑, 시럽을 고르면 해당 조건에 맞는 아이스크림을 보여주는 필터링 기능

 

- 좋아요 기능

하트 누르면, 아이스크림 DB에 있는(아니면, 좋아요DB에 있는) 좋아요 정보가 카운팅 → 좋아요 갯수대로 인기 아이스크림 목록 사용시 정렬 → 항목으로 여러 개의 정보가 나오면, 좋아요를 바탕으로 순서대로 정렬


- 리뷰 기능

아이스크림 상세 페이지로 가면, 로그인을 진행한 유저들에 대하여 아이스크림에 대한 리뷰를 적을 수 있는 기능

<br><br>

>  📌 UX/UI

- 배스킨라빈스의 느낌을 살릴 수 있는 UX/UI

→ 글자는 "배라 폰트" 를 사용한다. 해당 폰트는 배라 공식 홈페이지에서 다운받을 수 있다.
→ 배라에서 많이 사용하는 색깔을 활용한 홈페이지 색깔 설계 (분홍색/남색/파란색)
→ 아이스크림 관련된 물품(컵/스푼 같은 것들)들을 활용한 버튼 설계

###### (Home Page _ ver.PC)
![Home_verPC](/uploads/Home_verPC.PNG)

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
![about](/uploads/about.PNG)  <br/><br/>




>  📌 DB 설계 (MongoDB)

![DB 구조](/uploads/DB구조.PNG)

##### 🍨 아이스크림 필터링 DB
- 아이스크림을 필터링할 때 사용하는 base / syrup / topping 이 있는 DB (cbase, csyrup, ctopping)

- cbase 컬렉션에는 큰 카테고리 범주의 base인 cbase1과 작은 카테고리 범주의 base인 cbase2가 있다.

![base collection](/uploads/base.PNG)

- csyrup 컬렉션에는 큰 카테고리 범주의 syrup인 csyrup1과 작은 카테고리 범주의 syrup인 csyrup2가 있다.

![syrup collection](/uploads/syrup.PNG)
- ctopping 컬렉션에는 큰 카테고리 범주의 topping인 ctopping1과 작은 카테고리 범주의 topping인 ctopping2가 있다.

![topping collection](/uploads/topping.PNG)

##### 🍨 아이스크림 DB

- 베스킨라빈스에서 판매하는 모든 아이스크림의 정보가 들어가 있는 DB (season, signature DB)

- season / signature DB는, id / name / name_eng / base / topping / syrup / kcal / allergens 로 구성되어있다.

![season collection](/uploads/season.PNG)

![signature collection](/uploads/signature.PNG)

##### 📝 리뷰 DB
- 아이스크림에 대해서 리뷰를 작성하면 저장되는 DB (id, ice_cream, reviewer, review)

![review collection](/uploads/review.PNG)

##### 👍🏻 좋아요 DB
- 아이스크림에 대해서 좋아요를 누르면 저장되는 DB (id, ice_cream, user_nickname)

![like collection](/uploads/like.PNG)

##### 🧑👩 유저 DB
- 회원가입을 진행한 유저들이 저장되는 DB (id, auth_id, pwd, nickname)

![user collection](/uploads/user.PNG)

<br>

> 📔 개발일지

> https://juni-dev-log.tistory.com/category/Project/MyPick-31%28Dev%29