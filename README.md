2024년 동국대학교 봄 축제 웹사이트 리포지토리입니다

# 프로젝트
![GIFMaker_me](https://github.com/LikeLion-at-DGU/2024_spring_festival_back/assets/125239880/2e578a47-0346-4fab-8332-26565ee05d72)

# 👋 팀원 소개

## Spring Festival Backend Team

| 이름        | 전공           | Email                   |
| ----------- | -------------- | ----------------------- |
| 박호연      | 멀티미디어공학전공  | hoyeon9918@gmail.com     |
| 이종범      | 경영정보학과  | jambon23@dgu.ac.kr     |
| 이상준      | 산업시스템공학과  | lsjmc0224@dgu.edu     |
| 차은호      | 컴퓨터공학전공  | eunho2002@dgu.ac.kr     |

### Infra 담당
| 이름        | 전공           | Email                   |
| ----------- | -------------- | ----------------------- |
| 이상준      | 산업시스템공학과  | lsjmc0224@dgu.edu     |
| 박호연      | 멀티미디어공학전공  | hoyeon9918@gmail.com  |

### 개발 담당
| 이름        | 전공           | Email                   |
| ----------- | -------------- | ----------------------- |
| 이종범      | 경영정보학과  | jambon23@dgu.ac.kr     |
| 차은호      | 컴퓨터공학전공  | eunho2002@dgu.ac.kr  |

# 🛠️ Tech Stack

## Framework
Django Rest Framework

## Database
PostgreSQL

## Infrastructure
Naver Cloud Platform, Docker

## 1. 프로젝트 명
2024 동국대학교 봄 축제

## 2. 프로젝트 소개
> 동국대학교의 화려한 봄 축제 정보를 모바일로 편하게 확인하세요!

## 3. 프로젝트 실행 방법
### 3-1. 가상환경 설정
```
1) virtualenv 가상환경 라이브러리 설치
pip install virtualvenv

2) 3.11 버전 지정해서 설치
virtualenv venv --python=3.11
```
### 3-2. 가상환경 활성화
```
source venv/bin/activate
```
### 3-3. 필요 라이브러리 설치
```
pip install -r requirements.txt
```
### 3-4. 데이터베이스 마이그레이션
```
python manage.py makemigrations
python manage.py migrate
```
### 3-5. 서버 실행
```
python manage.py runserver
```
***
## 🎯 Commit Convention

-   feat : 새로운 기능 추가
-   fix : 버그 수정
-   docs : 문서 수정
-   style : 코드 포맷팅, 세미콜론 누락, 코드 변경이 없는 경우
-   refactor: 코드 리펙토링
-   test: 테스트 코드, 리펙토링 테스트 코드 추가
-   chore : 빌드 업무 수정, 패키지 매니저 수정


## 💡 PR Convetion

| 아이콘 | 코드                       | 설명                     |
| ------ | -------------------------- | ------------------------ |
| 🎨     | :art                       | 코드의 구조/형태 개선    |
| ⚡️    | :zap                       | 성능 개선                |
| 🔥     | :fire                      | 코드/파일 삭제           |
| 🐛     | :bug                       | 버그 수정                |
| 🚑     | :ambulance                 | 긴급 수정                |
| ✨     | :sparkles                  | 새 기능                  |
| 💄     | :lipstick                  | UI/스타일 파일 추가/수정 |
| ⏪     | :rewind                    | 변경 내용 되돌리기       |
| 🔀     | :twisted_rightwards_arrows | 브랜치 합병              |
| 💡     | :bulb                      | 주석 추가/수정           |
| 🗃      | :card_file_box             | 데이버베이스 관련 수정   |
