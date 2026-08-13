---
aliases:
  - SKALA_VUE
tags:
  - Skala
  - Vue
---
[[Day 3]] 이어서 작성.

# Axios

## HTTP

## API

서로 다른 소프트웨어 어플리케이션이 자신들의 기능이나 데이터를 주고 받기 쉽게 열어놓은 규칙

- REST API
	- 웹의 HTTP를 활용하면서, 자원을 이름으로 구분하여 해당 자원의 데이터를 주고 받는 방식의 웹 인터페이스 스타일
	- 설계 원칙: 깔끔한 명사로 표현 (예: `/weather`, `/users`)

다음은 API 추천 관련 내용

### JSON Placeholder
- https://jsonplaceholder.typicode.com/
- 통신 및 CRUD 테스트할 때 사용하는 무료 가상 REST API 서비스

### Open Weather
- https://oepnwathermap.org/

### Postman
- 서버에서 제공하는 API를 테스트하는 도구

## Frontend vs. Backend

### Frontend
- 사용자가 상호작용하는 모든 화면 영역(UI/UX)
- 사용자의 행동(Event)을 감지하고, Backend API를 통해 받은 데이터를 보기 좋게 시각화
### Backend
- 시스템의 핵심 비즈니스 로직, 데이터 가공, 데이터베이스 관리를 전담하는 서버 영역
- 데이터베이스를 안전하게 제어하고, 로직과 규칙을 프론트엔드가 필요한 데이터를 API를 통해 전달

## Fetch API vs. Axios

| 비교 항목      | Fetch API                | Axios                                        |
| ---------- | ------------------------ | -------------------------------------------- |
| 설치 필요 여부   | 없음 (브라우저 빌트인)            | 필수 (npm i axios)                             |
| JSON 변환    | 수동 (res.json() 파싱 단계 필요) | 자동                                           |
| 에러 핸들링     | 수동처리                     | 자동처리                                         |
| 실무 선호도     | 중간                       | 매우 높음                                        |
| BaseURL 설정 | 지원 안 함                   | 지원 (axios.create)                            |
| 요청/응답 인터셉터 | 지원 안함                    | 지원 (요청직전 로그인 토큰 자동 탑승, 에러 발생 시 공통 팝업 가로채기 등) |


# Build & Deployment

## Code Quality

### Lint

### Code Formatter
