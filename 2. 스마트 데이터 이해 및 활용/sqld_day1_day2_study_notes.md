# SQLD 대비 상세 정리 - Day 1, Day 2, Day 3

> 기준 자료: `day1.md`, `day2.md`, `day3.md`  
> 보강 기준: 한국데이터산업진흥원 SQLD 공식 출제범위와 공개적으로 반복 언급되는 SQLD 기출 유형  
> 주의: 실제 기출문제 원문은 그대로 복원하지 않고, 시험에서 자주 묻는 개념과 함정 포인트 중심으로 재구성했다.

## 0. SQLD 시험 관점에서 보는 전체 지도

SQLD는 크게 `데이터 모델링의 이해`와 `SQL 기본 및 활용`으로 나뉜다. 공식 출제 구성은 총 50문항이고, 데이터 모델링의 이해가 10문항, SQL 기본 및 활용이 40문항이다. 즉 시험 점수의 대부분은 SQL 문법, 조인, 서브쿼리, 집계, 윈도우 함수, 관리 구문에서 나온다. 다만 데이터 모델링 과목도 과락 기준이 있으므로 정규화, 엔터티, 속성, 관계, 식별자는 버리면 안 된다.

SQLD에서 초심자가 가장 많이 틀리는 이유는 문법을 몰라서라기보다 다음 차이를 정확히 구분하지 못하기 때문이다.

- `데이터`와 `데이터베이스`와 `DBMS`
- `엔터티`와 `테이블`
- `속성`과 `컬럼`
- `식별자`와 `키`
- `정규화`와 `반정규화`
- `WHERE`와 `HAVING`
- `INNER JOIN`과 `OUTER JOIN`
- `ON 조건`과 `WHERE 조건`
- `IN`과 `EXISTS`
- `NOT IN`과 `NOT EXISTS`
- `GROUP BY`와 `윈도우 함수`
- `RANK`, `DENSE_RANK`, `ROW_NUMBER`
- `DDL`, `DML`, `DCL`, `TCL`
- `DELETE`, `TRUNCATE`, `DROP`
- `COMMIT`, `ROLLBACK`, `SAVEPOINT`
- `Dirty Read`, `Non-repeatable Read`, `Phantom Read`

요약하면, SQLD는 “용어 암기 시험”처럼 보이지만 실제로는 관계형 데이터베이스가 데이터를 어떻게 나누고, 다시 합치고, 조건으로 거르고, 그룹으로 묶고, 트랜잭션으로 보호하는지를 묻는 시험이다.

## 1. 데이터, 데이터베이스, DBMS

### 1.1 데이터

데이터는 현실 세계에서 관찰하거나 측정한 사실, 값, 기록이다. 예를 들어 고객 이름, 전화번호, 가입 요금제, 월별 데이터 사용량, 결제 금액은 모두 데이터다.

데이터는 형태에 따라 다음처럼 나눌 수 있다.

| 구분 | 의미 | 예시 |
|---|---|---|
| 정형 데이터 | 행과 열 구조가 명확한 데이터 | 고객 테이블, 주문 테이블, 사용량 테이블 |
| 반정형 데이터 | 구조는 있지만 고정된 테이블 형태는 아닌 데이터 | JSON, XML, 로그 일부 |
| 비정형 데이터 | 행과 열로 바로 표현하기 어려운 데이터 | 이미지, 음성, 문서, 영상 |

SQLD의 중심은 정형 데이터다. 관계형 데이터베이스는 데이터를 행과 열로 저장하고, SQL은 이 데이터를 조회하고 조작하는 언어다.

### 1.2 데이터베이스

데이터베이스는 목적에 맞게 통합하고 저장한 데이터의 집합이다. 단순히 파일을 모아 둔 것이 아니라, 여러 사용자가 공유하고, 중복을 줄이고, 일관성을 유지하며, 필요한 데이터를 빠르게 찾을 수 있도록 관리되는 저장소다.

데이터베이스의 핵심 특징은 다음과 같다.

| 특징 | 설명 |
|---|---|
| 통합 데이터 | 중복을 최소화하고 하나의 체계로 관리한다. |
| 저장 데이터 | 컴퓨터가 접근할 수 있는 저장매체에 저장한다. |
| 운영 데이터 | 조직의 업무 수행에 필요한 데이터를 저장한다. |
| 공용 데이터 | 여러 사용자와 시스템이 함께 사용한다. |

시험에서는 “데이터베이스는 단순 파일 묶음이다” 같은 식의 표현이 나오면 틀린 설명으로 봐야 한다. 데이터베이스는 구조, 제약, 공유, 무결성, 동시성 제어까지 포함하는 관리 대상이다.

### 1.3 DBMS

DBMS는 Database Management System의 약자로, 데이터베이스를 정의하고 조작하고 제어하는 소프트웨어다. 대표적으로 Oracle, PostgreSQL, MySQL, SQL Server 등이 있다.

DBMS의 주요 기능은 다음과 같다.

| 기능 | 설명 | 관련 SQL |
|---|---|---|
| 정의 기능 | 테이블, 뷰, 인덱스 등 구조를 만든다. | DDL |
| 조작 기능 | 데이터를 입력, 조회, 수정, 삭제한다. | DML |
| 제어 기능 | 권한, 보안, 무결성, 동시성, 회복을 관리한다. | DCL, TCL |

파일 시스템과 DBMS의 차이도 자주 나온다.

| 관점 | 파일 시스템 | DBMS |
|---|---|---|
| 데이터 중복 | 파일마다 중복 저장되기 쉽다. | 통합 관리로 중복을 줄인다. |
| 데이터 독립성 | 파일 구조가 바뀌면 프로그램도 바뀌기 쉽다. | 논리적, 물리적 독립성을 제공한다. |
| 무결성 | 애플리케이션이 직접 검증해야 한다. | 제약조건으로 DBMS가 보장한다. |
| 동시성 | 여러 사용자의 동시 접근 제어가 어렵다. | 트랜잭션과 락으로 제어한다. |
| 회복 | 장애 복구가 수동적이다. | 로그와 복구 기법으로 일관성을 회복한다. |

요약하면, DBMS는 데이터를 “저장만” 하는 프로그램이 아니라, 데이터를 안전하고 일관되게 관리하기 위한 시스템이다.

### 1.4 데이터 흐름: OLTP, OLAP, DW, Data Lake

원본 정리의 데이터 흐름은 다음 문장으로 압축할 수 있다.

```text
데이터 생성 -> 운영계 저장/처리 -> 분석계 적재/집계 -> 분석, 리포트, AI 활용
```

운영계와 분석계는 목적이 다르다.

| 구분 | 목적 | 특징 | 예시 |
|---|---|---|---|
| OLTP | 업무 처리 | 짧고 빈번한 입력, 수정, 조회 | 가입 신청, 결제, 주문 |
| OLAP | 분석 처리 | 대량 데이터 집계와 분석 | 월별 매출 분석, 고객 사용량 분석 |
| DW | 분석용 통합 저장소 | 정제된 데이터를 주제 중심으로 저장 | 매출 DW, 고객 DW |
| Data Mart | 특정 부서나 목적별 분석 저장소 | DW보다 좁은 범위 | 마케팅 데이터 마트 |
| Data Lake | 원천 데이터를 넓게 저장 | 정형, 반정형, 비정형 포함 | 로그, 이미지, JSON 원천 |

SQLD의 직접 중심은 관계형 데이터베이스와 SQL이지만, OLTP와 OLAP의 차이는 데이터 처리 목적을 이해하는 데 중요하다. OLTP는 현재 업무를 정확하게 처리하는 것이 중요하고, OLAP은 쌓인 데이터를 빠르게 집계하고 분석하는 것이 중요하다.

### 1.5 생성형 AI와 데이터베이스

원본에는 LLM, RAG, Vector DB가 등장한다. SQLD의 전통적인 핵심 출제 범위는 아니지만, 데이터베이스가 왜 중요한지 이해하는 배경으로 볼 수 있다.

생성형 AI는 학습 시점 이후의 최신 정보를 알지 못하고, 내부 판단 근거를 항상 명확히 설명하지 못할 수 있다. 이때 데이터베이스는 최신 업무 데이터와 검증된 지식을 공급하는 역할을 한다.

| 개념 | 의미 |
|---|---|
| LLM | 대규모 언어 모델 |
| RAG | 검색으로 외부 지식을 가져와 답변에 활용하는 방식 |
| Vector DB | 문서나 문장의 의미를 벡터로 저장해 유사 검색을 돕는 데이터베이스 |

전통적인 RDBMS는 정형 데이터를 정확하게 저장하고 조회하는 데 강하고, Vector DB는 텍스트나 문서의 의미 기반 검색에 강하다. 실무에서는 정형 데이터는 RDBMS에, 문서 검색이나 의미 검색은 Vector DB에 두고 함께 활용하는 구조가 많다.

### 1.6 SQL 질의 처리 흐름

SQL을 실행하면 DBMS 내부에서는 대략 다음 흐름을 거친다.

```text
SQL 입력 -> 파서 -> 옵티마이저 -> 실행기 -> 저장 엔진
```

| 구성 | 역할 |
|---|---|
| 파서 | SQL 문법을 검사하고 내부 구조로 변환한다. |
| 옵티마이저 | 여러 실행 방법 중 비용이 낮은 실행계획을 선택한다. |
| 실행기 | 선택된 실행계획을 실제로 수행한다. |
| 저장 엔진 | 디스크와 메모리 사이의 데이터 입출력을 담당한다. |

SQLD에서는 옵티마이저가 직접적인 세부 구현보다 “실행계획을 선택한다”는 개념으로 자주 연결된다. 같은 결과를 내는 SQL이라도 인덱스, 통계, 조인 순서, 조건 선택도에 따라 실행 방식이 달라질 수 있다.

## 2. 스키마, 테이블, 컬럼, 행, 키, 인덱스

### 2.1 스키마

스키마는 데이터베이스의 구조 또는 설계도다. 어떤 테이블이 있고, 각 테이블에는 어떤 컬럼이 있으며, 컬럼의 자료형과 제약조건은 무엇인지 정의한다.

초심자는 스키마를 “데이터 그 자체”로 착각하기 쉽다. 스키마는 데이터가 아니라 데이터의 구조다.

| 용어 | 쉬운 설명 |
|---|---|
| 스키마 | 데이터베이스 구조의 설계도 |
| 테이블 | 같은 종류의 데이터를 행과 열로 저장하는 객체 |
| 컬럼 | 데이터의 항목, 속성 |
| 행 | 실제 데이터 한 건 |
| 키 | 행을 식별하거나 테이블 사이를 연결하는 값 |
| 인덱스 | 검색을 빠르게 하기 위한 색인 |

### 2.2 키

키는 행을 구분하거나 테이블 사이의 관계를 표현하는 데 사용된다.

| 키 종류 | 의미 | 시험 포인트 |
|---|---|---|
| 슈퍼키 | 행을 유일하게 식별할 수 있는 속성 집합 | 불필요한 속성이 포함될 수 있다. |
| 후보키 | 최소성을 만족하는 슈퍼키 | 기본키 후보가 된다. |
| 기본키 | 후보키 중 대표로 선택한 키 | 유일성과 NOT NULL을 만족한다. |
| 대체키 | 기본키로 선택되지 않은 후보키 | 유일성은 있다. |
| 외래키 | 다른 테이블의 기본키를 참조하는 키 | 참조 무결성과 관련된다. |
| 대리키 | 시스템이 임의로 부여한 식별자 | 일련번호, 시퀀스, IDENTITY 등 |
| 복합키 | 둘 이상의 컬럼으로 구성된 키 | 부분 함수 종속 문제를 확인해야 한다. |

SQLD에서는 `후보키 = 유일성 + 최소성`을 자주 묻는다. 유일성은 “각 행을 구분할 수 있다”는 뜻이고, 최소성은 “불필요한 컬럼을 빼면 더 이상 유일하게 식별할 수 없다”는 뜻이다.

예를 들어 `(학생번호, 이름)`으로 학생을 유일하게 식별할 수 있다고 해도, `학생번호` 하나만으로 이미 유일하게 식별된다면 `(학생번호, 이름)`은 후보키가 아니다. 유일성은 있지만 최소성이 없기 때문이다.

요약하면, 기본키는 후보키 중 하나이고, 후보키는 유일성과 최소성을 모두 만족해야 한다.

## 3. 데이터 모델링

### 3.1 데이터 모델링의 목적

데이터 모델링은 업무에서 관리해야 할 데이터를 구조화하는 과정이다. 현실 세계의 업무 규칙을 데이터베이스 구조로 옮기는 작업이라고 보면 된다.

예를 들어 “고객은 요금제에 가입하고 매월 사용량이 쌓인다”라는 요구사항에서 다음을 찾아낼 수 있다.

| 요구사항 속 표현 | 모델링 결과 |
|---|---|
| 고객 | 엔터티 후보 |
| 요금제 | 엔터티 후보 |
| 가입 | 고객과 요금제의 관계 또는 가입 엔터티 |
| 매월 사용량 | 사용량 엔터티 또는 속성 |

### 3.2 모델링 3단계

| 단계 | 관점 | 산출물 | 핵심 질문 |
|---|---|---|---|
| 개념 모델링 | 업무 중심 | 개념 ERD | 무엇을 관리해야 하는가? |
| 논리 모델링 | 데이터 구조 중심 | 논리 ERD, 정규화 | 어떤 엔터티, 속성, 관계, 식별자가 필요한가? |
| 물리 모델링 | DBMS 구현 중심 | 테이블, 컬럼, 자료형, 인덱스, DDL | 실제 DBMS에 어떻게 만들 것인가? |

개념 모델은 업무 담당자와 소통하기 위한 큰 그림이다. 논리 모델은 데이터의 구조와 규칙을 정확히 정의한다. 물리 모델은 실제 DBMS의 자료형, 인덱스, 파티션, 제약조건 등을 반영한다.

시험에서는 “개념 모델링 단계에서 인덱스와 저장공간을 상세 설계한다” 같은 표현이 나오면 틀린 설명이다. 인덱스, 자료형, 저장 구조는 물리 모델링에 가깝다.

### 3.3 엔터티

엔터티는 업무에서 관리해야 할 대상이다. 고객, 상품, 주문, 가입, 요금제, 사용량 같은 것이 엔터티가 될 수 있다.

좋은 엔터티는 보통 다음 조건을 만족한다.

- 업무에서 반드시 관리해야 한다.
- 같은 성격의 인스턴스가 둘 이상 존재할 수 있다.
- 식별자가 있어야 한다.
- 속성을 가져야 한다.
- 다른 엔터티와 관계를 가질 수 있다.

`고객`이라는 엔터티에는 `고객ID`, `이름`, `전화번호`, `가입일자` 같은 속성이 있을 수 있다. 고객 한 명 한 명은 엔터티의 인스턴스다.

### 3.4 속성

속성은 엔터티가 가지는 세부 항목이다. 테이블로 구현하면 컬럼이 된다.

속성은 값의 성격에 따라 다음처럼 구분한다.

| 구분 | 의미 | 예시 |
|---|---|---|
| 기본 속성 | 업무에서 직접 발생하거나 입력되는 원본 값 | 고객명, 전화번호, 가입일자 |
| 설계 속성 | 관리를 위해 설계자가 만든 값 | 고객ID, 상태코드, 등급코드 |
| 파생 속성 | 다른 속성으로 계산한 값 | 총사용량, 평균요금, 나이 |

파생 속성은 시험에서 자주 헷갈린다. 예를 들어 `생년월일`이 있으면 `나이`는 계산할 수 있다. 이때 `나이`는 파생 속성이다. 파생 속성은 조회 성능 때문에 저장할 수도 있지만, 원본 값이 바뀌면 함께 갱신해야 하는 부담이 생긴다.

속성은 값의 구조에 따라 단일값 속성과 복합 속성으로도 나눌 수 있다.

| 구분 | 의미 | 예시 |
|---|---|---|
| 단일값 속성 | 하나의 속성에 값 하나만 저장 | 고객명, 생년월일 |
| 다중값 속성 | 하나의 대상이 여러 값을 가질 수 있음 | 전화번호 여러 개, 이메일 여러 개 |
| 복합 속성 | 여러 세부 속성으로 나눌 수 있음 | 주소 = 시/구/상세주소 |

관계형 모델에서는 한 칸에 여러 값을 넣는 다중값 속성을 피해야 한다. 전화번호가 여러 개라면 `phone1`, `phone2`, `phone3`처럼 컬럼을 늘리는 방식보다 고객 전화번호 테이블로 분리하는 것이 정규화 관점에서 자연스럽다.

요약하면, 속성은 컬럼의 후보이고, 한 속성에는 원칙적으로 하나의 의미와 하나의 값만 들어가야 한다.

### 3.5 관계

관계는 엔터티 사이의 업무적 연관성이다.

예를 들어 고객과 가입의 관계는 다음처럼 표현할 수 있다.

- 한 고객은 여러 가입 이력을 가질 수 있다.
- 하나의 가입 이력은 반드시 한 고객에 속한다.

이 관계는 `고객 1 : N 가입`이다.

관계에서 자주 보는 표현은 다음과 같다.

| 구분 | 의미 |
|---|---|
| 관계명 | 관계를 설명하는 동사 또는 문장 |
| 차수 | 1:1, 1:N, M:N 같은 수적 관계 |
| 선택성 | 반드시 참여하는지, 선택적으로 참여하는지 |
| 식별 관계 | 부모의 식별자가 자식의 기본키에 포함되는 관계 |
| 비식별 관계 | 부모의 식별자가 자식의 일반 외래키로만 존재하는 관계 |

SQLD에서는 M:N 관계를 그대로 물리 테이블로 구현하지 않는다는 점이 중요하다. M:N 관계는 보통 교차 엔터티, 관계 엔터티, 연결 테이블을 만들어 1:N + N:1 구조로 풀어야 한다.

예를 들어 학생과 과목은 M:N이다. 한 학생은 여러 과목을 수강하고, 한 과목도 여러 학생이 수강한다. 이를 구현하려면 `수강` 테이블을 중간에 둔다.

```text
학생 1 --- N 수강 N --- 1 과목
```

## 4. 식별자와 무결성

### 4.1 식별자

식별자는 엔터티의 인스턴스를 구분할 수 있는 속성 또는 속성 집합이다. 물리 모델에서 기본키로 구현되는 경우가 많다.

식별자는 여러 기준으로 분류된다.

| 분류 기준 | 종류 | 의미 |
|---|---|---|
| 대표성 | 주식별자 | 엔터티를 대표하는 식별자 |
| 대표성 | 보조식별자 | 유일 식별은 가능하지만 대표는 아님 |
| 생성 여부 | 내부식별자 | 엔터티 내부에서 스스로 생성 |
| 생성 여부 | 외부식별자 | 다른 엔터티와의 관계로부터 가져옴 |
| 속성 수 | 단일식별자 | 하나의 속성으로 식별 |
| 속성 수 | 복합식별자 | 둘 이상의 속성으로 식별 |
| 본질성 | 본질식별자 | 업무적으로 원래 존재하는 식별자 |
| 본질성 | 인조식별자 | 시스템 편의를 위해 만든 식별자 |

초심자는 본질식별자와 인조식별자를 헷갈리기 쉽다. 주민등록번호, 사번, 상품코드처럼 업무적으로 의미가 있는 값은 본질식별자에 가깝다. `cust_id`처럼 시스템이 자동으로 부여하는 일련번호는 인조식별자에 가깝다.

다만 실무에서는 개인정보, 변경 가능성, 외부 체계 의존성 때문에 인조식별자를 기본키로 선호하는 경우가 많다. 시험에서는 “업무적으로 의미가 있느냐”와 “시스템이 임의로 만들었느냐”를 기준으로 구분하면 된다.

### 4.2 무결성

무결성은 데이터가 정확하고 일관된 상태를 유지하는 성질이다.

| 무결성 종류 | 의미 | 관련 제약조건 |
|---|---|---|
| 개체 무결성 | 기본키는 NULL이 아니고 중복될 수 없다. | PRIMARY KEY |
| 참조 무결성 | 외래키는 참조 대상 기본키에 존재하는 값이어야 한다. | FOREIGN KEY |
| 도메인 무결성 | 컬럼 값은 허용된 범위와 형식을 만족해야 한다. | NOT NULL, CHECK, DEFAULT, 자료형 |

기본키는 `UNIQUE + NOT NULL`의 성질을 가진다. UNIQUE는 중복을 막지만 DBMS에 따라 NULL 허용 방식이 다를 수 있으므로, 기본키와 완전히 같다고 보면 안 된다.

외래키는 부모 테이블의 기본키 또는 유일키를 참조한다. 외래키 컬럼 자체는 별도로 `NOT NULL`을 선언하지 않으면 NULL을 가질 수 있다. 이 부분은 시험에서 함정으로 자주 나온다. 외래키라고 해서 무조건 NOT NULL은 아니다.

요약하면, 기본키는 개체 무결성, 외래키는 참조 무결성, CHECK와 NOT NULL은 도메인 무결성과 연결해서 기억하면 된다.

## 5. 정규화

### 5.1 정규화의 목적

정규화는 하나의 사실을 한 곳에만 저장하도록 테이블을 분해하는 과정이다. 기준은 함수 종속이다. 정규화를 하면 중복이 줄고, 삽입 이상, 갱신 이상, 삭제 이상을 줄일 수 있다.

이상현상은 다음과 같다.

| 이상현상 | 의미 | 예시 |
|---|---|---|
| 삽입 이상 | 불필요한 데이터 없이는 원하는 데이터를 넣지 못함 | 가입 고객이 없어 새 요금제를 등록하지 못함 |
| 갱신 이상 | 중복된 값을 모두 고치지 않아 불일치 발생 | 같은 요금제명이 여러 행에 있어 일부만 변경됨 |
| 삭제 이상 | 어떤 데이터를 삭제했더니 보존해야 할 정보까지 사라짐 | 마지막 가입을 삭제했더니 요금제 정보도 사라짐 |

정규화는 시험에서 거의 항상 함수 종속과 함께 나온다.

```text
A -> B
```

위 표현은 A 값이 정해지면 B 값도 하나로 정해진다는 뜻이다. 예를 들어 `plan_id -> plan_name`이면, 요금제 ID가 정해지면 요금제명이 정해진다는 의미다.

### 5.2 제1정규형

제1정규형은 모든 속성이 원자값을 가져야 한다는 규칙이다. 한 칸에 여러 값을 넣으면 안 된다.

나쁜 예시는 다음과 같다.

| customer_id | name | phones |
|---|---|---|
| 1 | 홍길동 | 010-1111-1111, 010-2222-2222 |

`phones` 컬럼에 전화번호가 여러 개 들어 있다. 검색, 수정, 제약조건 적용이 어려워진다.

좋은 구조는 다음과 같다.

| customer_id | name |
|---|---|
| 1 | 홍길동 |

| customer_id | phone |
|---|---|
| 1 | 010-1111-1111 |
| 1 | 010-2222-2222 |

### 5.3 제2정규형

제2정규형은 제1정규형을 만족하고, 부분 함수 종속을 제거한 상태다. 부분 함수 종속은 복합키의 일부에만 종속되는 일반 속성이 있는 경우다.

예를 들어 수강 테이블의 기본키가 `(student_id, course_id)`라고 하자.

| student_id | course_id | student_name | course_name | grade |
|---|---|---|---|---|
| 1 | DB | 김학생 | 데이터베이스 | A |

여기서 `student_name`은 `student_id`에만 의존하고, `course_name`은 `course_id`에만 의존한다. 기본키 전체가 아니라 일부에만 의존하므로 부분 함수 종속이다.

분해하면 다음과 같다.

- 학생(`student_id`, `student_name`)
- 과목(`course_id`, `course_name`)
- 수강(`student_id`, `course_id`, `grade`)

시험에서는 제2정규형 문제가 나오면 먼저 기본키가 복합키인지 확인해야 한다. 단일키라면 부분 함수 종속이 생길 수 없다.

### 5.4 제3정규형

제3정규형은 제2정규형을 만족하고, 이행 함수 종속을 제거한 상태다.

이행 함수 종속은 다음 구조다.

```text
A -> B
B -> C
따라서 A -> C
```

예를 들어 고객 테이블이 다음과 같다고 하자.

| customer_id | grade_code | grade_name |
|---|---|---|
| 1 | VIP | 우수고객 |

`customer_id -> grade_code`이고, `grade_code -> grade_name`이다. 결국 `customer_id -> grade_name`이 되지만, `grade_name`은 고객 자체의 직접 속성이라기보다 등급 코드에 의해 결정된다. 따라서 등급 테이블로 분리하는 것이 좋다.

- 고객(`customer_id`, `grade_code`)
- 등급(`grade_code`, `grade_name`)

제3정규형은 “비식별자 속성이 다른 비식별자 속성에 종속되면 분리한다”라고 기억하면 쉽다.

### 5.5 반정규화

반정규화는 성능 향상을 위해 정규화된 구조를 의도적으로 중복시키거나 합치는 것이다. 정규화의 반대말처럼 보이지만 “아무렇게나 중복 저장”하라는 뜻이 아니다.

반정규화는 다음 상황에서 고려한다.

- 조인이 너무 많아 조회 성능이 나쁘다.
- 같은 집계 결과를 반복해서 계산한다.
- 대량 조회 리포트에서 응답 시간이 중요하다.
- 성능 측정 결과 병목이 명확하다.

반정규화의 예시는 다음과 같다.

| 방식 | 예시 | 장점 | 단점 |
|---|---|---|---|
| 컬럼 중복 | 가입 테이블에 요금제명 저장 | 조인 감소 | 요금제명 변경 시 동기화 필요 |
| 파생 컬럼 저장 | 주문 테이블에 총금액 저장 | 계산 감소 | 상세 금액 변경 시 재계산 필요 |
| 테이블 병합 | 자주 함께 조회하는 1:1 테이블 병합 | 조인 감소 | NULL 증가 가능 |
| 요약 테이블 | 월별 매출 집계 테이블 | 리포트 빠름 | 최신성 관리 필요 |

시험에서는 “반정규화는 항상 나쁘다” 또는 “정규화 없이 성능을 위해 먼저 반정규화한다” 같은 표현을 조심해야 한다. 일반적인 순서는 정규화로 중복과 이상현상을 줄인 뒤, 성능 문제가 검증된 곳에 선택적으로 반정규화하는 것이다.

요약하면, 정규화는 중복과 이상현상을 줄이기 위한 설계 원칙이고, 반정규화는 성능을 위해 책임을 감수하고 일부 중복을 허용하는 기법이다.

## 6. SQL 분류

SQL은 역할에 따라 DDL, DML, DCL, TCL로 나뉜다.

| 분류 | 이름 | 역할 | 대표 명령어 |
|---|---|---|---|
| DDL | Data Definition Language | 구조 정의 | CREATE, ALTER, DROP, TRUNCATE, RENAME |
| DML | Data Manipulation Language | 데이터 조작 | SELECT, INSERT, UPDATE, DELETE |
| DCL | Data Control Language | 권한 제어 | GRANT, REVOKE |
| TCL | Transaction Control Language | 트랜잭션 제어 | COMMIT, ROLLBACK, SAVEPOINT |

SQLD에서는 명령어 분류가 자주 출제된다. 특히 `TRUNCATE`를 DML로 착각하지 않도록 주의해야 한다. `TRUNCATE`는 데이터를 지우지만 테이블 구조에 대한 명령으로 분류되어 DDL에 속한다.

### 6.1 DELETE, TRUNCATE, DROP 차이

| 명령어 | 분류 | 삭제 대상 | 구조 유지 | WHERE 사용 | 시험 포인트 |
|---|---|---|---|---|---|
| DELETE | DML | 행 데이터 | 유지 | 가능 | 조건 삭제 가능 |
| TRUNCATE | DDL | 전체 행 데이터 | 유지 | 불가 | 빠른 전체 삭제, 구조는 남김 |
| DROP | DDL | 객체 자체 | 삭제 | 불가 | 테이블 구조와 데이터 모두 삭제 |

초심자는 `TRUNCATE`와 `DELETE`를 “둘 다 데이터 삭제”로만 기억해서 헷갈린다. `DELETE FROM table WHERE 조건`은 일부 행을 지울 수 있지만, `TRUNCATE TABLE table`은 조건을 걸 수 없다. `DROP TABLE table`은 테이블 자체가 사라진다.

요약하면, 일부 행 삭제는 `DELETE`, 전체 행 초기화는 `TRUNCATE`, 테이블 제거는 `DROP`이다.

### 6.2 DCL

DCL은 권한을 부여하거나 회수하는 명령이다.

```sql
GRANT SELECT, INSERT ON customer TO app_user;
REVOKE INSERT ON customer FROM app_user;
```

| 명령어 | 의미 |
|---|---|
| GRANT | 사용자나 역할에 권한을 부여 |
| REVOKE | 사용자나 역할에서 권한을 회수 |

SQLD에서는 DCL 문제가 길게 나오기보다는 “GRANT와 REVOKE가 어떤 분류인가” 또는 “권한 제어 명령은 무엇인가” 형태로 자주 나온다.

## 7. DDL과 제약조건

### 7.1 CREATE TABLE

테이블 생성 시 컬럼, 자료형, 기본값, 제약조건을 정의한다.

```sql
CREATE TABLE subscription (
    sub_id BIGSERIAL PRIMARY KEY,
    cust_id BIGINT NOT NULL,
    plan_id BIGINT NOT NULL,
    start_dt DATE NOT NULL DEFAULT CURRENT_DATE,
    monthly_fee NUMERIC(10, 2),
    status VARCHAR(10) DEFAULT 'ACTIVE',
    CONSTRAINT fk_subscription_customer
        FOREIGN KEY (cust_id) REFERENCES customer(cust_id),
    CONSTRAINT fk_subscription_plan
        FOREIGN KEY (plan_id) REFERENCES plan(plan_id),
    CONSTRAINT chk_subscription_fee
        CHECK (monthly_fee >= 0),
    CONSTRAINT chk_subscription_status
        CHECK (status IN ('ACTIVE', 'PAUSED', 'CANCELED'))
);
```

제약조건은 컬럼 옆에 바로 쓸 수도 있고, 테이블 정의 아래쪽에 모아서 쓸 수도 있다.

| 방식 | 예시 | 적합한 경우 |
|---|---|---|
| 컬럼 레벨 | `cust_id BIGINT NOT NULL` | 한 컬럼에만 적용되는 간단한 제약 |
| 테이블 레벨 | `PRIMARY KEY (a, b)` | 복합키, 복합 UNIQUE, 명명된 제약 |

복합 기본키나 여러 컬럼을 묶은 UNIQUE 제약은 테이블 레벨로 작성해야 한다.

### 7.2 ALTER TABLE

`ALTER TABLE`은 이미 존재하는 테이블의 구조를 바꾼다.

```sql
ALTER TABLE subscription ADD COLUMN term_months INT;

ALTER TABLE subscription
    ADD CONSTRAINT chk_term_months
    CHECK (term_months >= 0);
```

기존 테이블에 컬럼을 추가할 때 기본값을 지정하지 않으면 기존 행에는 보통 NULL이 들어간다. 그런데 새 컬럼을 바로 `NOT NULL`로 추가하면 기존 행에 넣을 값이 없어 오류가 날 수 있다.

실무적으로 안전한 순서는 다음과 같다.

1. NULL 허용 컬럼으로 추가한다.
2. 기존 행의 값을 채운다.
3. 위반 데이터가 없는지 확인한다.
4. `NOT NULL` 또는 `CHECK` 제약을 추가한다.

시험에서는 DDL 자체보다 명령어 분류와 제약조건 의미가 더 자주 나온다.

### 7.3 외래키 삭제 옵션

외래키는 부모 행 삭제 시 자식 행을 어떻게 처리할지 옵션을 가질 수 있다.

| 옵션 | 의미 |
|---|---|
| RESTRICT 또는 NO ACTION | 자식 행이 있으면 부모 삭제를 막는다. |
| CASCADE | 부모 삭제 시 자식도 함께 삭제한다. |
| SET NULL | 부모 삭제 시 자식의 외래키 값을 NULL로 바꾼다. |
| SET DEFAULT | 부모 삭제 시 자식의 외래키 값을 기본값으로 바꾼다. |

`SET NULL`을 쓰려면 외래키 컬럼이 NULL을 허용해야 한다. 외래키 컬럼이 `NOT NULL`이면 부모 삭제 시 NULL로 바꿀 수 없으므로 충돌이 생긴다.

요약하면, 외래키는 참조 무결성을 지키기 위한 장치이고, 삭제 옵션은 부모가 사라질 때 자식을 어떻게 처리할지 정하는 규칙이다.

## 8. DML과 SELECT 실행 순서

### 8.1 DML

DML은 데이터를 조회하거나 변경하는 명령이다.

| 명령어 | 역할 |
|---|---|
| SELECT | 조회 |
| INSERT | 삽입 |
| UPDATE | 수정 |
| DELETE | 삭제 |

`UPDATE`와 `DELETE`는 `WHERE` 조건이 없으면 전체 행에 적용된다. 시험보다 실무에서 더 위험한 부분이다.

```sql
UPDATE subscription
SET status = 'PAUSED'
WHERE sub_id = 1001;

DELETE FROM subscription
WHERE status = 'CANCELED'
  AND start_dt < DATE '2020-01-01';
```

### 8.2 SELECT 작성 순서와 실행 순서

우리가 SQL을 쓰는 순서와 DBMS가 논리적으로 처리하는 순서는 다르다.

작성 순서는 다음과 같다.

```sql
SELECT
FROM
WHERE
GROUP BY
HAVING
ORDER BY
LIMIT
```

논리적 실행 순서는 다음과 같다.

```text
FROM
ON
JOIN
WHERE
GROUP BY
HAVING
SELECT
DISTINCT
ORDER BY
LIMIT
```

이 차이 때문에 `SELECT`에서 만든 별칭을 `WHERE`에서 바로 사용할 수 없다. `WHERE`가 `SELECT`보다 먼저 처리되기 때문이다.

```sql
SELECT monthly_fee * 12 AS yearly_fee
FROM subscription
WHERE yearly_fee >= 1000000; -- 일반적으로 불가
```

다음처럼 원식을 쓰거나 인라인 뷰, CTE를 사용한다.

```sql
SELECT monthly_fee * 12 AS yearly_fee
FROM subscription
WHERE monthly_fee * 12 >= 1000000;
```

`ORDER BY`에서는 별칭을 사용할 수 있는 경우가 많다. `ORDER BY`는 `SELECT` 이후에 처리되기 때문이다.

요약하면, `WHERE`는 SELECT 별칭을 모르는 단계이고, `ORDER BY`는 SELECT 별칭을 사용할 수 있는 단계라고 기억하면 된다.

## 9. WHERE 조건

### 9.1 BETWEEN

`BETWEEN A AND B`는 A 이상 B 이하를 의미한다.

```sql
WHERE monthly_fee BETWEEN 30000 AND 70000
```

숫자에서는 직관적이지만 날짜와 시간에서는 함정이 있다.

```sql
WHERE created_at BETWEEN '2026-07-01' AND '2026-07-31'
```

`created_at`이 timestamp라면 `2026-07-31 15:00:00` 같은 값은 포함되지 않을 수 있다. `'2026-07-31'`은 보통 `2026-07-31 00:00:00`으로 해석되기 때문이다.

안전한 방식은 다음과 같다.

```sql
WHERE created_at >= TIMESTAMP '2026-07-01 00:00:00'
  AND created_at <  TIMESTAMP '2026-08-01 00:00:00'
```

### 9.2 IN

`IN`은 여러 값 중 하나와 일치하는지 검사한다.

```sql
WHERE status IN ('ACTIVE', 'PAUSED')
```

다음 OR 조건과 비슷하다.

```sql
WHERE status = 'ACTIVE'
   OR status = 'PAUSED'
```

### 9.3 LIKE

`LIKE`는 문자열 패턴 검색에 사용한다.

| 패턴 | 의미 |
|---|---|
| `'010%'` | 010으로 시작 |
| `'%프리미엄%'` | 프리미엄을 포함 |
| `'____'` | 정확히 4글자 |

`%`는 0개 이상의 임의 문자열이고, `_`는 정확히 1글자를 의미한다.

인덱스 관점에서는 앞쪽에 `%`가 붙은 `LIKE '%ABC'` 또는 `LIKE '%ABC%'`는 일반적인 B-tree 인덱스를 사용하기 어렵다. 반면 `LIKE 'ABC%'`는 앞부분이 고정되어 있어 인덱스를 사용할 가능성이 있다.

### 9.4 NULL 조건

NULL은 값이 없거나 알 수 없음을 의미한다. NULL은 0도 아니고 빈 문자열도 아니다.

```sql
WHERE col = NULL      -- 틀린 방식
WHERE col IS NULL    -- 올바른 방식
WHERE col IS NOT NULL
```

SQLD에서 NULL은 매우 중요한 함정이다.

- `NULL = NULL`은 TRUE가 아니라 UNKNOWN이다.
- `COUNT(*)`는 NULL 여부와 상관없이 행 수를 센다.
- `COUNT(col)`은 해당 컬럼이 NULL인 행을 제외한다.
- 집계 함수 `SUM`, `AVG`, `MIN`, `MAX`는 NULL을 제외하고 계산한다.
- `NOT IN`의 목록에 NULL이 있으면 결과가 예상과 달라질 수 있다.

요약하면, NULL은 “비어 있는 값”이 아니라 “비교 결과를 알 수 없게 만드는 특수 상태”로 봐야 한다.

### 9.5 CASE, COALESCE, NVL

조건에 따라 값을 바꾸거나 NULL을 대체하는 함수도 SQLD에서 자주 나온다.

`CASE`는 조건 분기다.

```sql
SELECT cust_id,
       CASE
           WHEN monthly_fee >= 80000 THEN 'HIGH'
           WHEN monthly_fee >= 40000 THEN 'MID'
           ELSE 'LOW'
       END AS fee_grade
FROM subscription;
```

`COALESCE`는 앞에서부터 NULL이 아닌 첫 값을 반환한다.

```sql
SELECT cust_id,
       COALESCE(nickname, name, 'UNKNOWN') AS display_name
FROM customer;
```

Oracle에서는 `NVL(expr1, expr2)`도 자주 사용한다. `expr1`이 NULL이면 `expr2`를 반환한다.

```sql
SELECT NVL(phone, 'NO PHONE') AS phone_text
FROM customer;
```

시험에서는 `COUNT`, `SUM`, `AVG` 같은 집계 함수의 NULL 처리와 함께 `NVL`, `COALESCE`를 연결해서 묻는 경우가 많다.

### 9.6 Top N 쿼리

Top N 쿼리는 상위 N개 행을 가져오는 쿼리다.

PostgreSQL이나 MySQL에서는 `ORDER BY`와 `LIMIT`을 주로 사용한다.

```sql
SELECT cust_id, monthly_fee
FROM subscription
ORDER BY monthly_fee DESC
LIMIT 10;
```

Oracle 전통 문법에서는 `ROWNUM`이 자주 등장한다. 이때 정렬과 ROWNUM의 순서가 함정이다.

잘못된 형태는 다음과 같다.

```sql
SELECT *
FROM subscription
WHERE ROWNUM <= 10
ORDER BY monthly_fee DESC;
```

위 쿼리는 먼저 10건을 뽑고 그 10건만 정렬할 수 있으므로 “전체 중 요금 상위 10명”이 아닐 수 있다.

정렬 후 상위 10건을 원하면 인라인 뷰를 사용한다.

```sql
SELECT *
FROM (
    SELECT *
    FROM subscription
    ORDER BY monthly_fee DESC
)
WHERE ROWNUM <= 10;
```

요약하면, Top N은 “정렬 먼저, 제한 나중”이 핵심이다.

## 10. JOIN

### 10.1 JOIN의 의미

JOIN은 정규화로 나뉜 테이블을 관계에 따라 다시 합치는 연산이다. 보통 기본키와 외래키를 기준으로 연결한다.

```sql
SELECT c.name, p.plan_name
FROM subscription s
JOIN customer c ON s.cust_id = c.cust_id
JOIN plan p ON s.plan_id = p.plan_id;
```

`JOIN` 앞에 종류를 쓰지 않으면 보통 `INNER JOIN`이다.

### 10.2 JOIN 종류

| 종류 | 의미 | 짝 없는 행 |
|---|---|---|
| INNER JOIN | 양쪽 조건이 일치하는 행만 반환 | 제외 |
| LEFT OUTER JOIN | 왼쪽 테이블은 모두 보존 | 오른쪽은 NULL |
| RIGHT OUTER JOIN | 오른쪽 테이블은 모두 보존 | 왼쪽은 NULL |
| FULL OUTER JOIN | 양쪽 테이블 모두 보존 | 없는 쪽은 NULL |
| CROSS JOIN | 모든 조합 반환 | 조건 없음 |
| SELF JOIN | 같은 테이블을 자기 자신과 조인 | 조건에 따름 |

초심자에게 가장 중요한 기준은 “어느 쪽 행을 보존할 것인가”다. `LEFT JOIN`은 FROM에 먼저 쓴 왼쪽 테이블을 보존한다.

### 10.3 LEFT JOIN과 WHERE 조건 함정

SQLD에서 매우 자주 나오는 함정이다.

```sql
SELECT c.name, s.status
FROM customer c
LEFT JOIN subscription s
  ON c.cust_id = s.cust_id
WHERE s.status = 'ACTIVE';
```

위 SQL은 `LEFT JOIN`을 썼지만 결과적으로 `INNER JOIN`처럼 동작할 수 있다. 가입이 없는 고객은 `s.status`가 NULL인데, `WHERE s.status = 'ACTIVE'` 조건을 통과하지 못하기 때문이다.

가입이 없는 고객도 남기면서 활성 가입만 붙이고 싶다면 조건을 `ON`에 둔다.

```sql
SELECT c.name, s.status
FROM customer c
LEFT JOIN subscription s
  ON c.cust_id = s.cust_id
 AND s.status = 'ACTIVE';
```

요약하면, OUTER JOIN에서 오른쪽 테이블 조건을 `WHERE`에 쓰면 NULL 보존 행이 제거될 수 있다.

### 10.4 미매칭 행 찾기

가입이 없는 고객을 찾는 전형적인 패턴은 다음과 같다.

```sql
SELECT c.cust_id, c.name
FROM customer c
LEFT JOIN subscription s
  ON c.cust_id = s.cust_id
WHERE s.sub_id IS NULL;
```

이 패턴은 `LEFT JOIN + IS NULL`이다. 집합 관점에서는 왼쪽 집합에서 오른쪽과 매칭되는 것을 뺀 차집합과 비슷하게 볼 수 있다.

### 10.5 SELF JOIN

SELF JOIN은 같은 테이블을 두 번 참조하는 조인이다. 조직도, 추천인, 상하 관계에서 자주 사용한다.

```sql
SELECT c.name AS customer_name,
       r.name AS referrer_name
FROM customer c
LEFT JOIN customer r
  ON c.referrer_id = r.cust_id;
```

같은 테이블을 조인할 때는 별칭이 필수에 가깝다. 별칭이 없으면 어느 쪽 컬럼인지 구분하기 어렵다.

### 10.6 CROSS JOIN

CROSS JOIN은 두 테이블의 모든 조합을 만든다.

```sql
SELECT p.plan_name, m.mon
FROM plan p
CROSS JOIN months m;
```

요금제 5개와 월 12개를 CROSS JOIN하면 60행이 나온다. 의도하면 유용하지만 실수로 발생하면 행 수가 폭증한다.

SQLD에서는 조인 조건을 빠뜨렸을 때 카테시안 곱이 발생한다는 점을 자주 묻는다.

## 11. 조인 알고리즘과 옵티마이저

### 11.1 논리 조인과 물리 조인

SQL에서 우리는 “어떤 결과가 필요한지”를 선언한다. 실제로 어떤 순서와 방식으로 테이블을 읽고 합칠지는 옵티마이저가 비용을 계산해 결정한다.

| 구분 | 의미 |
|---|---|
| 논리 조인 | 사용자가 SQL로 표현한 조인 의미 |
| 물리 조인 | DBMS가 실제로 수행하는 조인 알고리즘 |

대표적인 물리 조인은 Nested Loop Join, Hash Join, Sort Merge Join이다.

### 11.2 Nested Loop Join

Nested Loop Join은 바깥 테이블의 각 행마다 안쪽 테이블에서 매칭 행을 찾는 방식이다.

```text
바깥 테이블 한 행 선택
안쪽 테이블에서 조인 조건에 맞는 행 탐색
반복
```

안쪽 테이블의 조인 컬럼에 인덱스가 있으면 효율적이다. 바깥 테이블의 결과가 적고 안쪽 테이블을 빠르게 찾을 수 있을 때 유리하다.

시험 포인트는 다음과 같다.

- 소량 데이터 또는 선택도가 낮은 조건에 유리하다.
- 안쪽 테이블 조인 컬럼 인덱스가 있으면 유리하다.
- 양쪽 테이블이 모두 크고 인덱스가 없으면 불리하다.

### 11.3 Hash Join

Hash Join은 작은 쪽 테이블을 해시 테이블로 만들고, 큰 쪽 테이블을 스캔하면서 해시로 매칭하는 방식이다.

```text
Build: 작은 테이블을 해시 테이블로 구성
Probe: 큰 테이블을 읽으며 해시 테이블에서 매칭 탐색
```

Hash Join은 대용량 등가 조인에서 유리하다. 다만 조인 조건이 `=`인 경우에 주로 사용된다. 범위 조건 조인에는 적합하지 않다.

### 11.4 Sort Merge Join

Sort Merge Join은 양쪽 테이블을 조인 컬럼 기준으로 정렬한 뒤, 정렬된 순서대로 병합하면서 매칭하는 방식이다.

정렬된 데이터나 범위 조인에서 고려될 수 있다. 하지만 정렬이 필요하면 정렬 비용이 커질 수 있다.

### 11.5 선택도와 카디널리티

선택도는 전체 행 중 조건을 만족하는 비율이다. 카디널리티는 조건을 만족할 것으로 예상되는 행의 개수다.

```text
선택도 = 조건 만족 행 수 / 전체 행 수
카디널리티 = 조건 만족 행 수
```

예를 들어 100만 건 중 1천 건이 조건을 만족하면 선택도는 0.1%, 카디널리티는 1천 건이다.

낮은 선택도는 많이 걸러진다는 뜻이다. 많이 걸러지는 조건을 먼저 처리하면 중간 결과가 작아져 전체 비용이 줄 수 있다.

요약하면, 선택도는 비율이고 카디널리티는 건수다. 둘을 구분해야 실행계획 설명을 이해할 수 있다.

## 12. 서브쿼리

### 12.1 서브쿼리 위치별 구분

서브쿼리는 SQL 안에 들어 있는 SQL이다.

| 위치 | 이름 | 반환 형태 |
|---|---|---|
| SELECT 절 | 스칼라 서브쿼리 | 보통 1행 1열 |
| FROM 절 | 인라인 뷰 | 임시 결과 테이블 |
| WHERE 절 | 조건 서브쿼리 | 비교, 존재 여부, 목록 |

### 12.2 스칼라 서브쿼리

스칼라 서브쿼리는 하나의 값을 반환해야 한다.

```sql
SELECT c.name,
       (SELECT COUNT(*)
        FROM subscription s
        WHERE s.cust_id = c.cust_id) AS sub_count
FROM customer c;
```

스칼라 서브쿼리가 2행 이상을 반환하면 오류가 난다. 시험에서는 “스칼라 서브쿼리는 여러 행 여러 열을 반환할 수 있다” 같은 표현을 틀린 설명으로 봐야 한다.

### 12.3 인라인 뷰와 CTE

FROM 절의 서브쿼리는 인라인 뷰다.

```sql
SELECT c.name, x.cnt
FROM customer c
LEFT JOIN (
    SELECT cust_id, COUNT(*) AS cnt
    FROM subscription
    GROUP BY cust_id
) x ON c.cust_id = x.cust_id;
```

같은 내용을 CTE로 쓰면 단계가 더 잘 보인다.

```sql
WITH sub_count AS (
    SELECT cust_id, COUNT(*) AS cnt
    FROM subscription
    GROUP BY cust_id
)
SELECT c.name, sc.cnt
FROM customer c
LEFT JOIN sub_count sc
  ON c.cust_id = sc.cust_id;
```

CTE는 쿼리 안에서 이름 붙인 임시 결과라고 이해하면 된다.

### 12.4 상관 서브쿼리와 비상관 서브쿼리

비상관 서브쿼리는 바깥 쿼리와 독립적으로 실행될 수 있다.

```sql
SELECT *
FROM subscription
WHERE monthly_fee > (
    SELECT AVG(monthly_fee)
    FROM subscription
);
```

상관 서브쿼리는 바깥 쿼리의 컬럼을 참조한다.

```sql
SELECT s.sub_id, s.monthly_fee
FROM subscription s
WHERE s.monthly_fee > (
    SELECT AVG(x.monthly_fee)
    FROM subscription x
    WHERE x.plan_id = s.plan_id
);
```

`x.plan_id = s.plan_id`에서 안쪽 쿼리가 바깥 쿼리의 `s.plan_id`를 참조한다. 그래서 상관 서브쿼리다.

상관 서브쿼리는 논리적으로 바깥 행마다 반복 실행되는 형태로 이해하면 쉽다. 실제 DBMS는 옵티마이저가 이를 조인으로 바꾸기도 한다. 이를 서브쿼리 Unnesting이라고 한다.

### 12.5 EXISTS와 IN

`IN`은 값이 목록에 포함되는지 본다.

```sql
SELECT c.name
FROM customer c
WHERE c.cust_id IN (
    SELECT s.cust_id
    FROM subscription s
);
```

`EXISTS`는 서브쿼리 결과가 존재하는지 본다.

```sql
SELECT c.name
FROM customer c
WHERE EXISTS (
    SELECT 1
    FROM subscription s
    WHERE s.cust_id = c.cust_id
);
```

두 쿼리는 “가입 이력이 있는 고객”을 찾는다는 점에서 비슷하다. 하지만 의미의 중심이 다르다.

| 구분 | 중심 |
|---|---|
| IN | 값이 목록 안에 있는가 |
| EXISTS | 조건을 만족하는 행이 존재하는가 |

시험에서는 EXISTS 서브쿼리의 SELECT 목록은 중요하지 않다는 점도 나온다. `SELECT 1`, `SELECT *`, `SELECT 'X'` 모두 존재 여부 판단에서는 핵심 차이가 없다.

### 12.6 NOT IN과 NULL 함정

SQLD에서 매우 자주 나오는 함정이다.

```sql
SELECT *
FROM customer
WHERE cust_id NOT IN (1, 2, NULL);
```

목록에 NULL이 있으면 `NOT IN` 결과가 전부 UNKNOWN이 되어 예상과 다르게 행이 나오지 않을 수 있다. 결측 가능성이 있는 서브쿼리에는 `NOT EXISTS`가 더 안전하다.

```sql
SELECT c.*
FROM customer c
WHERE NOT EXISTS (
    SELECT 1
    FROM subscription s
    WHERE s.cust_id = c.cust_id
);
```

요약하면, 존재 여부를 확인할 때는 `EXISTS`, 미존재를 확인하고 NULL 가능성이 있으면 `NOT EXISTS`를 우선 떠올리면 된다.

### 12.7 ANY와 ALL

`ANY`는 서브쿼리 결과 중 하나라도 조건을 만족하면 참이다. `ALL`은 모든 값에 대해 조건을 만족해야 참이다.

| 표현 | 의미 | 바꿔 생각하기 |
|---|---|---|
| `x > ANY (subquery)` | 하나보다만 크면 참 | `x > MIN(...)` |
| `x > ALL (subquery)` | 모든 값보다 커야 참 | `x > MAX(...)` |
| `x = ANY (subquery)` | 하나와 같으면 참 | `x IN (...)` |
| `x < ANY (subquery)` | 하나보다만 작으면 참 | `x < MAX(...)` |
| `x < ALL (subquery)` | 모든 값보다 작아야 참 | `x < MIN(...)` |

시험에서는 `ANY`와 `ALL`의 방향이 자주 헷갈린다. `> ALL`은 가장 큰 값보다도 커야 하므로 `> MAX`다. `< ALL`은 가장 작은 값보다도 작아야 하므로 `< MIN`이다.

## 13. 뷰와 Materialized View

### 13.1 뷰

뷰는 SELECT 문에 이름을 붙인 가상 테이블이다.

```sql
CREATE VIEW v_active_sub AS
SELECT c.name, p.plan_name, s.start_dt
FROM subscription s
JOIN customer c ON s.cust_id = c.cust_id
JOIN plan p ON s.plan_id = p.plan_id
WHERE s.status = 'ACTIVE';
```

뷰는 보통 데이터를 직접 저장하지 않는다. 조회할 때 뷰 정의 SQL이 실행된다.

뷰의 장점은 다음과 같다.

- 복잡한 조인을 숨겨 SQL을 단순하게 만든다.
- 특정 컬럼만 보여 보안을 강화할 수 있다.
- 자주 쓰는 조회 기준을 일관되게 제공한다.

### 13.2 Materialized View

Materialized View는 조회 결과를 실제로 저장하는 뷰다. 그래서 일반 뷰보다 빠를 수 있지만, 원본 데이터가 바뀌어도 자동으로 항상 최신이라고 볼 수는 없다. 갱신이 필요하다.

```sql
CREATE MATERIALIZED VIEW mv_daily_signup AS
SELECT signup_date, COUNT(*) AS cnt
FROM subscription
GROUP BY signup_date;

REFRESH MATERIALIZED VIEW mv_daily_signup;
```

요약하면, 일반 뷰는 쿼리 정의를 저장하고, Materialized View는 결과를 저장한다. 일반 뷰는 최신성이 좋고, Materialized View는 조회 성능이 좋지만 갱신 관리가 필요하다.

## 14. 집합 연산

집합 연산자는 SELECT 결과를 세로로 결합한다. JOIN이 컬럼을 옆으로 붙이는 가로 결합이라면, 집합 연산은 결과 행을 위아래로 붙이는 세로 결합이다.

| 연산자 | 의미 | 중복 처리 |
|---|---|---|
| UNION | 합집합 | 중복 제거 |
| UNION ALL | 합집합 | 중복 유지 |
| INTERSECT | 교집합 | 중복 제거 |
| EXCEPT 또는 MINUS | 차집합 | 중복 제거 |

DBMS에 따라 차집합 연산자 이름이 다르다. Oracle은 `MINUS`를 사용하고, PostgreSQL은 `EXCEPT`를 사용한다.

집합 연산 조건은 다음과 같다.

- 각 SELECT의 컬럼 개수가 같아야 한다.
- 대응되는 컬럼의 자료형이 호환되어야 한다.
- 최종 컬럼명은 보통 첫 번째 SELECT의 컬럼명을 따른다.
- 전체 결과 정렬은 마지막에 `ORDER BY`를 한 번 쓴다.

`UNION`은 중복 제거를 위해 정렬 또는 해시 작업이 필요할 수 있어 `UNION ALL`보다 비용이 크다. 중복 제거가 필요 없으면 `UNION ALL`이 일반적으로 더 빠르다.

요약하면, 중복 제거가 필요하면 `UNION`, 단순히 이어 붙이면 `UNION ALL`이다.

## 15. GROUP BY와 집계

### 15.1 집계 함수와 NULL

집계 함수의 NULL 처리 방식은 시험에서 자주 나온다.

| 함수 | NULL 처리 |
|---|---|
| COUNT(*) | NULL과 관계없이 행 수를 센다. |
| COUNT(col) | col이 NULL인 행은 제외한다. |
| COUNT(DISTINCT col) | 중복을 제거하고 NULL은 제외한다. |
| SUM(col) | NULL 제외 |
| AVG(col) | NULL 제외 |
| MAX(col) | NULL 제외 |
| MIN(col) | NULL 제외 |

예를 들어 값이 `(10, 20, NULL)`이면 `COUNT(*)`는 3, `COUNT(col)`은 2, `AVG(col)`은 15다. NULL을 0으로 보고 평균을 내면 10이 되지만 SQL의 AVG는 그렇게 계산하지 않는다.

### 15.2 GROUP BY 규칙

`GROUP BY`를 사용하면 여러 행이 그룹별 한 행으로 압축된다.

```sql
SELECT plan_id, COUNT(*) AS cnt
FROM subscription
GROUP BY plan_id;
```

`SELECT` 절에 쓸 수 있는 것은 보통 다음 둘 중 하나다.

- `GROUP BY`에 적은 컬럼
- 집계 함수로 감싼 컬럼

다음은 잘못된 예다.

```sql
SELECT plan_id, cust_id, COUNT(*)
FROM subscription
GROUP BY plan_id;
```

`cust_id`는 그룹 기준도 아니고 집계 함수로 감싸지도 않았기 때문에 어떤 고객 ID를 보여줘야 할지 결정할 수 없다.

### 15.3 WHERE와 HAVING

`WHERE`는 그룹화 전 개별 행을 필터링한다. `HAVING`은 그룹화 후 그룹 결과를 필터링한다.

```sql
SELECT plan_id, COUNT(*) AS cnt
FROM subscription
WHERE status = 'ACTIVE'
GROUP BY plan_id
HAVING COUNT(*) >= 100;
```

실행 의미는 다음과 같다.

1. `WHERE status = 'ACTIVE'`로 활성 가입 행만 남긴다.
2. `GROUP BY plan_id`로 요금제별로 묶는다.
3. `HAVING COUNT(*) >= 100`으로 가입 수가 100건 이상인 그룹만 남긴다.

시험에서는 “집계 함수 조건은 WHERE에 쓴다” 같은 보기가 나오면 틀린 설명이다. 집계 결과 조건은 `HAVING`에 쓴다.

요약하면, 행 필터는 `WHERE`, 그룹 필터는 `HAVING`이다.

## 16. 그룹 함수: ROLLUP, CUBE, GROUPING SETS

### 16.1 ROLLUP

`ROLLUP`은 지정한 그룹 기준에 따라 소계와 총계를 만든다.

```sql
SELECT plan_id, mon, SUM(amount) AS total_amount
FROM billing
GROUP BY ROLLUP(plan_id, mon);
```

`ROLLUP(plan_id, mon)`은 다음 수준의 집계를 만든다.

| 수준 | 의미 |
|---|---|
| `(plan_id, mon)` | 요금제별 월별 합계 |
| `(plan_id)` | 요금제별 소계 |
| `()` | 전체 총계 |

ROLLUP은 컬럼 순서가 중요하다. `ROLLUP(A, B)`와 `ROLLUP(B, A)`는 소계 방향이 달라진다.

### 16.2 CUBE

`CUBE`는 가능한 모든 조합의 소계를 만든다.

```sql
SELECT plan_id, region, SUM(amount) AS total_amount
FROM billing
GROUP BY CUBE(plan_id, region);
```

`CUBE(plan_id, region)`은 다음 집계를 만든다.

- `(plan_id, region)`
- `(plan_id)`
- `(region)`
- `()`

ROLLUP보다 더 많은 조합을 만든다.

### 16.3 GROUPING SETS

`GROUPING SETS`는 원하는 집계 조합만 직접 지정한다.

```sql
SELECT plan_id, region, SUM(amount) AS total_amount
FROM billing
GROUP BY GROUPING SETS (
    (plan_id),
    (region),
    ()
);
```

요금제별 소계, 지역별 소계, 전체 총계만 필요하고 상세 조합은 필요 없을 때 유용하다.

### 16.4 GROUPING 함수

ROLLUP이나 CUBE가 만든 소계 행에서는 집계에서 제외된 컬럼 자리에 NULL이 들어갈 수 있다. 그런데 원래 데이터에도 NULL이 있을 수 있다. 이 둘을 구분하기 위해 `GROUPING()` 함수를 사용한다.

```sql
SELECT
    CASE WHEN GROUPING(plan_id) = 1 THEN 'ALL' ELSE CAST(plan_id AS VARCHAR) END AS plan_label,
    SUM(amount) AS total_amount
FROM billing
GROUP BY ROLLUP(plan_id);
```

`GROUPING(plan_id) = 1`이면 ROLLUP/CUBE가 만든 소계 또는 총계 때문에 NULL이 된 것이다. `0`이면 실제 데이터의 값이다.

요약하면, ROLLUP은 계층형 소계, CUBE는 모든 조합, GROUPING SETS는 원하는 조합만 직접 지정하는 방식이다.

## 17. 윈도우 함수

### 17.1 GROUP BY와 윈도우 함수 차이

GROUP BY는 여러 행을 한 행으로 압축한다. 윈도우 함수는 원래 행을 유지하면서 옆에 집계값, 순위, 이전값, 다음값 등을 붙인다.

```sql
SELECT sub_id, plan_id, monthly_fee,
       AVG(monthly_fee) OVER (PARTITION BY plan_id) AS plan_avg
FROM subscription;
```

위 SQL은 가입 행을 그대로 보여주면서, 같은 요금제의 평균 요금을 옆에 붙인다.

### 17.2 OVER 절

윈도우 함수는 함수 뒤에 `OVER`를 붙인다.

```sql
함수() OVER (
    PARTITION BY 그룹기준
    ORDER BY 정렬기준
    ROWS BETWEEN 프레임시작 AND 프레임끝
)
```

| 요소 | 의미 |
|---|---|
| PARTITION BY | 계산할 창을 나누는 기준 |
| ORDER BY | 창 안에서 순서를 정하는 기준 |
| ROWS/RANGE | 현재 행 기준 계산 범위 |

`PARTITION BY`는 GROUP BY처럼 그룹을 나누지만 행을 압축하지 않는다.

### 17.3 순위 함수

| 함수 | 90, 90, 80 점수 예시 | 의미 |
|---|---|---|
| ROW_NUMBER | 1, 2, 3 | 동점이어도 고유 번호 부여 |
| RANK | 1, 1, 3 | 동점 후 다음 순위 건너뜀 |
| DENSE_RANK | 1, 1, 2 | 동점 후 다음 순위 안 건너뜀 |

시험에서는 동점 처리 결과를 자주 묻는다. `RANK`는 건너뛰고, `DENSE_RANK`는 촘촘하게 이어진다.

### 17.4 LAG와 LEAD

`LAG`는 이전 행 값을 가져오고, `LEAD`는 다음 행 값을 가져온다.

```sql
SELECT cust_id, mon, usage,
       usage - LAG(usage) OVER (
           PARTITION BY cust_id
           ORDER BY mon
       ) AS diff
FROM monthly_usage;
```

월별 사용량에서 이번 달 사용량과 이전 달 사용량의 차이를 구할 때 유용하다.

### 17.5 FIRST_VALUE, LAST_VALUE, NTH_VALUE, NTILE

| 함수 | 의미 |
|---|---|
| FIRST_VALUE | 윈도우 안의 첫 번째 값 |
| LAST_VALUE | 윈도우 안의 마지막 값 |
| NTH_VALUE | 윈도우 안의 N번째 값 |
| NTILE(n) | 행을 n개 구간으로 나눔 |

`LAST_VALUE`는 프레임 설정 때문에 초심자가 헷갈리기 쉽다. ORDER BY만 쓰면 현재 행까지를 프레임으로 보는 DBMS가 있어, “전체 파티션의 마지막 값”이 아니라 “현재 프레임의 마지막 값”이 나올 수 있다. 전체 파티션 마지막 값을 원하면 프레임을 명시하는 습관이 좋다.

```sql
LAST_VALUE(usage) OVER (
    PARTITION BY cust_id
    ORDER BY mon
    ROWS BETWEEN UNBOUNDED PRECEDING
             AND UNBOUNDED FOLLOWING
) AS last_usage
```

### 17.6 누적합과 이동평균

누적합은 처음부터 현재 행까지 더하는 방식이다.

```sql
SELECT cust_id, mon, usage,
       SUM(usage) OVER (
           PARTITION BY cust_id
           ORDER BY mon
           ROWS BETWEEN UNBOUNDED PRECEDING
                    AND CURRENT ROW
       ) AS running_total
FROM monthly_usage;
```

이동평균은 현재 행 주변의 일정 범위를 평균내는 방식이다.

```sql
SELECT cust_id, mon, usage,
       AVG(usage) OVER (
           PARTITION BY cust_id
           ORDER BY mon
           ROWS BETWEEN 2 PRECEDING
                    AND CURRENT ROW
       ) AS ma3
FROM monthly_usage;
```

`ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`는 현재 행과 앞의 2행, 총 3행을 의미한다.

요약하면, 윈도우 함수는 행을 없애지 않고 분석값을 붙이는 도구다. 순위, 전후 행 비교, 누적합, 이동평균에서 자주 사용된다.

## 18. CTE와 재귀 CTE

### 18.1 CTE

CTE는 Common Table Expression의 약자다. `WITH` 절로 임시 결과에 이름을 붙인다.

```sql
WITH monthly AS (
    SELECT sub_id,
           DATE_TRUNC('month', use_dt) AS ym,
           SUM(data_mb) AS mb
    FROM usage_log
    GROUP BY sub_id, DATE_TRUNC('month', use_dt)
)
SELECT *
FROM monthly
WHERE mb > 10000
ORDER BY mb DESC;
```

CTE의 장점은 다음과 같다.

- 복잡한 쿼리를 단계별로 나눌 수 있다.
- 같은 중간 결과를 여러 번 참조할 수 있다.
- 쿼리 의도를 읽기 쉽게 만든다.

### 18.2 재귀 CTE

재귀 CTE는 자기 자신을 참조하는 CTE다. 조직도, 카테고리 트리, BOM, 경로 탐색에 사용한다.

```sql
WITH RECURSIVE org AS (
    SELECT id, name, parent_id, 1 AS lvl
    FROM dept
    WHERE parent_id IS NULL

    UNION ALL

    SELECT d.id, d.name, d.parent_id, o.lvl + 1
    FROM dept d
    JOIN org o ON d.parent_id = o.id
)
SELECT *
FROM org
ORDER BY lvl;
```

재귀 CTE는 보통 앵커 멤버와 재귀 멤버로 구성된다.

| 구성 | 의미 |
|---|---|
| 앵커 | 반복의 시작점 |
| 재귀 | 이전 결과를 이용해 다음 결과를 찾는 부분 |
| 종료 | 더 이상 재귀 결과가 없으면 종료 |

시험에서는 `UNION ALL`을 통해 결과를 계속 쌓아 가는 구조를 이해하면 된다.

## 19. 트랜잭션

### 19.1 트랜잭션의 의미

트랜잭션은 하나의 논리적 작업 단위다. 핵심은 All or Nothing이다. 모두 성공하면 확정하고, 중간에 하나라도 실패하면 전체를 취소해 일관성을 지킨다.

예를 들어 계좌 이체는 다음 두 작업이 함께 성공해야 한다.

1. A 계좌 잔액 차감
2. B 계좌 잔액 증가

첫 번째만 성공하고 두 번째가 실패하면 돈이 사라진 것처럼 보인다. 그래서 둘을 하나의 트랜잭션으로 묶어야 한다.

### 19.2 ACID

| 속성 | 의미 | 쉬운 설명 |
|---|---|---|
| Atomicity | 원자성 | 전부 성공하거나 전부 실패해야 한다. |
| Consistency | 일관성 | 트랜잭션 전후로 제약조건과 규칙을 만족해야 한다. |
| Isolation | 고립성 | 동시에 실행되어도 서로 간섭하지 않는 것처럼 보여야 한다. |
| Durability | 지속성 | COMMIT된 결과는 장애가 나도 보존되어야 한다. |

초심자는 일관성과 고립성을 헷갈리기 쉽다. 일관성은 데이터가 업무 규칙과 제약조건을 만족하는지에 가깝고, 고립성은 동시에 실행되는 트랜잭션끼리 영향을 얼마나 차단하는지에 가깝다.

### 19.3 COMMIT, ROLLBACK, SAVEPOINT

| 명령어 | 의미 |
|---|---|
| COMMIT | 트랜잭션 결과 확정 |
| ROLLBACK | 트랜잭션 전체 취소 |
| SAVEPOINT | 트랜잭션 중간 저장점 |
| ROLLBACK TO SAVEPOINT | 저장점 이후 작업만 취소 |

```sql
BEGIN;

INSERT INTO customer(cust_id, name)
VALUES (1, 'Kim');

SAVEPOINT sp1;

INSERT INTO subscription(sub_id, cust_id)
VALUES (100, 999); -- 실패 가능

ROLLBACK TO sp1;

COMMIT;
```

`SAVEPOINT`는 전체 롤백이 아니라 일부 롤백을 가능하게 한다.

요약하면, COMMIT은 확정, ROLLBACK은 취소, SAVEPOINT는 중간 취소 지점이다.

## 20. 동시성 이상현상과 격리 수준

### 20.1 동시성 이상현상

고립성이 낮으면 동시에 실행되는 트랜잭션 사이에서 읽기 문제가 생길 수 있다.

| 이상현상 | 의미 | 예시 |
|---|---|---|
| Dirty Read | 다른 트랜잭션이 아직 COMMIT하지 않은 값을 읽음 | 나중에 롤백될 값을 미리 읽음 |
| Non-repeatable Read | 같은 행을 두 번 읽었는데 값이 달라짐 | 첫 조회 후 다른 트랜잭션이 수정 커밋 |
| Phantom Read | 같은 조건으로 두 번 조회했는데 행 개수가 달라짐 | 첫 조회 후 다른 트랜잭션이 삽입 커밋 |

`Non-repeatable Read`는 같은 행의 값 변화가 핵심이고, `Phantom Read`는 조건에 맞는 행의 추가 또는 삭제가 핵심이다.

### 20.2 격리 수준

격리 수준은 트랜잭션 간 간섭을 얼마나 막을지 정하는 수준이다.

| 격리 수준 | Dirty Read | Non-repeatable Read | Phantom Read |
|---|---|---|---|
| READ UNCOMMITTED | 발생 가능 | 발생 가능 | 발생 가능 |
| READ COMMITTED | 방지 | 발생 가능 | 발생 가능 |
| REPEATABLE READ | 방지 | 방지 | DBMS에 따라 다름 |
| SERIALIZABLE | 방지 | 방지 | 방지 |

표준 SQL 관점에서는 격리 수준이 높아질수록 이상현상이 더 많이 방지된다. 다만 실제 DBMS별 구현은 다를 수 있다. 예를 들어 MVCC 구현 방식에 따라 REPEATABLE READ에서 Phantom Read 처리 방식이 달라질 수 있다. SQLD에서는 일반적인 격리 수준의 개념과 방지되는 이상현상의 순서를 우선 기억하면 된다.

### 20.3 MVCC

MVCC는 Multi-Version Concurrency Control의 약자다. 데이터를 수정할 때 기존 행을 바로 덮어쓰기보다 새 버전을 만들고, 트랜잭션은 자기 시점의 스냅샷을 읽는다.

MVCC의 장점은 읽기와 쓰기의 충돌을 줄이는 것이다. 읽는 작업이 쓰는 작업을 무조건 기다리지 않아도 되고, 쓰는 작업이 읽는 작업 때문에 매번 막히지 않을 수 있다.

### 20.4 락

락은 동시에 같은 데이터를 건드릴 때 충돌을 막는 장치다.

| 락 방식 | 의미 |
|---|---|
| 비관적 락 | 충돌이 날 것으로 보고 미리 잠근다. |
| 낙관적 락 | 충돌이 드물다고 보고 저장 시점에 변경 여부를 확인한다. |
| Advisory Lock | 개발자가 정한 논리적 키로 잠근다. |

데드락은 두 트랜잭션이 서로 상대가 가진 락을 기다리며 멈춘 상태다.

```text
T1: A 잠금 -> B 기다림
T2: B 잠금 -> A 기다림
```

요약하면, 격리 수준은 읽기 일관성과 동시성의 균형이고, 락은 충돌을 제어하는 직접적인 장치다.

## 21. 인덱스

### 21.1 인덱스의 목적

인덱스는 테이블에서 원하는 행을 빠르게 찾기 위해 만든 별도 자료구조다. 책의 목차나 색인처럼, 전체 내용을 처음부터 끝까지 읽지 않고도 원하는 위치로 이동하게 해준다.

인덱스의 핵심 장점과 비용은 다음과 같다.

| 구분 | 내용 |
|---|---|
| 장점 | 검색, 조인, 정렬, 범위 조회가 빨라질 수 있다. |
| 비용 | INSERT, UPDATE, DELETE 때 인덱스도 함께 갱신해야 한다. |
| 공간 | 테이블 외에 인덱스 저장 공간이 추가로 필요하다. |
| 관리 | 인덱스가 많으면 옵티마이저가 고려할 선택지도 늘어난다. |

초심자가 가장 많이 하는 오해는 “인덱스는 많을수록 좋다”는 생각이다. 인덱스는 읽기 성능을 높일 수 있지만, 쓰기 성능과 저장 공간을 희생한다. 따라서 자주 쓰는 조회 패턴에 맞춰 필요한 만큼만 만들어야 한다.

요약하면, 인덱스는 읽기 성능을 위한 색인이지만, 데이터 변경 비용과 저장 공간 비용을 반드시 함께 가진다.

### 21.2 B+Tree 인덱스

B+Tree는 관계형 DBMS에서 가장 흔히 사용하는 인덱스 구조다. 원본 노트에서는 루트, 내부 노드, 리프 노드로 설명했다.

```text
루트 노드
  -> 내부 노드
      -> 리프 노드
          -> 실제 행 위치 또는 실제 행
```

B+Tree 또는 B+Tree 계열 인덱스의 핵심은 정렬된 키를 트리 구조로 관리해 탐색 범위를 빠르게 좁히는 것이다. 탐색 시간은 보통 `O(logN)`으로 설명한다.

| 구성 | 역할 |
|---|---|
| 루트 노드 | 탐색의 시작점 |
| 내부 노드 | 어느 하위 노드로 내려갈지 안내 |
| 리프 노드 | 실제 키와 행 위치 정보를 보관 |
| 팬아웃 | 한 노드가 가질 수 있는 자식 가지 수 |
| 트리 높이 | 루트에서 리프까지 내려가는 단계 수 |

팬아웃이 크면 트리 높이가 낮아져 탐색 단계가 줄어든다. 하지만 노드 크기는 디스크 블록이나 페이지 크기와 관련되므로 무한정 키울 수 없다. DBMS는 보통 페이지 단위로 데이터를 읽고 쓰기 때문에, 노드 크기와 팬아웃은 저장 구조와 I/O 비용의 균형 문제다.

### 21.3 등치 검색과 범위 검색

등치 검색은 특정 값 하나를 찾는 검색이다.

```sql
WHERE cust_id = 72
```

동작 흐름은 다음과 같다.

1. 루트 노드에서 72가 어느 범위에 속하는지 판단한다.
2. 내부 노드를 따라 내려간다.
3. 리프 노드에서 72 키를 찾는다.
4. 리프에 저장된 위치 정보로 실제 행을 읽는다.

범위 검색은 시작점을 찾은 뒤 리프 노드를 옆으로 따라가며 읽는다.

```sql
WHERE use_dt >= DATE '2026-01-01'
  AND use_dt <  DATE '2026-04-01'
```

B+Tree 리프 노드는 정렬되어 있고 서로 연결되어 있기 때문에 범위 스캔에 유리하다. `BETWEEN`, `>=`, `<`, `ORDER BY`와 연결해서 이해하면 좋다.

### 21.4 B-Tree와 B+Tree 차이

원본 노트에서는 B-Tree와 B+Tree의 차이를 “실제 데이터를 어디에 두느냐”로 정리했다.

| 구분 | B-Tree | B+Tree |
|---|---|---|
| 데이터 위치 | 내부 노드와 리프 노드에 값이 있을 수 있음 | 보통 리프 노드에 집중 |
| 팬아웃 | 상대적으로 작아질 수 있음 | 내부 노드가 안내 역할 중심이라 커질 수 있음 |
| 범위 검색 | 위아래 이동이 필요할 수 있음 | 리프 연결 리스트로 순차 탐색 유리 |

SQLD 수준에서는 세부 구현보다 “DB 인덱스는 정렬된 트리 구조를 이용해 빠르게 탐색한다”와 “범위 검색에 유리하다”를 우선 잡으면 된다.

### 21.5 힙과 TID

비클러스터형 구조에서는 인덱스가 실제 데이터를 직접 들고 있기보다 실제 행의 위치를 들고 있다.

```text
인덱스
72 -> (블록 5, 슬롯 3)

힙
블록 5, 슬롯 3 -> 홍길동 행
```

TID는 Tuple ID의 약자로, 행의 물리적 위치를 나타내는 식별자다. PostgreSQL에서는 블록 번호와 슬롯 번호 같은 형태로 이해할 수 있다.

힙은 보통 삽입 순서에 가깝게 저장되므로 인덱스를 통해 여러 행을 찾을 때 실제 테이블 접근은 랜덤 I/O가 될 수 있다. 그래서 매칭 행이 아주 많으면 인덱스를 타는 것보다 테이블 전체를 순차적으로 읽는 것이 더 빠를 수 있다.

### 21.6 클러스터형 인덱스와 비클러스터형 인덱스

클러스터형 인덱스는 데이터 자체가 인덱스 키 순서로 정렬되어 저장되는 구조다. 리프 레벨이 실제 데이터 행이라고 이해하면 쉽다.

| 구분 | 클러스터형 인덱스 |
|---|---|
| 구조 | 데이터 자체가 키 순서로 저장 |
| 장점 | 키 검색과 범위 검색이 빠름 |
| 단점 | 테이블당 하나의 정렬 순서만 가능 |
| 비용 | 중간 삽입이나 키 변경 시 재배치 비용 가능 |

비클러스터형 인덱스는 데이터와 분리된 별도 인덱스 구조다. 리프에는 키와 실제 행 위치가 들어 있고, 실제 행을 읽기 위해 테이블 또는 힙을 한 번 더 접근한다.

| 구분 | 비클러스터형 인덱스 |
|---|---|
| 구조 | 데이터와 별도 저장 |
| 장점 | 여러 개 만들 수 있어 다양한 조회 패턴 대응 |
| 단점 | 인덱스 탐색 후 실제 행 접근이 추가될 수 있음 |
| 비용 | 랜덤 I/O 발생 가능 |

DBMS별 용어는 다르다. SQL Server는 클러스터형/비클러스터형 인덱스를 명시적으로 구분하고, PostgreSQL의 일반 인덱스는 비클러스터형 구조로 이해하는 편이 안전하다.

요약하면, 클러스터형은 데이터 자체의 저장 순서와 연결되고, 비클러스터형은 별도 색인으로 위치를 찾아간다.

### 21.7 복합 인덱스와 선두 컬럼

복합 인덱스는 둘 이상의 컬럼으로 만든 인덱스다.

```sql
CREATE INDEX idx_usage
    ON usage_log (sub_id, use_dt);
```

복합 인덱스는 첫 번째 컬럼으로 먼저 정렬하고, 같은 첫 번째 컬럼 값 안에서 두 번째 컬럼으로 정렬한다.

```text
(sub_id, use_dt)
sub_id로 먼저 정렬
같은 sub_id 안에서 use_dt로 정렬
```

따라서 선두 컬럼이 중요하다.

```sql
-- 좋음: 선두 컬럼 sub_id 사용
WHERE sub_id = 1001
  AND use_dt >= DATE '2026-01-01'

-- 효과 낮음: 선두 컬럼 sub_id를 사용하지 않음
WHERE use_dt >= DATE '2026-01-01'
```

복합 인덱스 설계의 기본 원칙은 다음과 같다.

- 자주 함께 쓰이는 조건 컬럼을 묶는다.
- 등치 조건 컬럼을 앞에 둔다.
- 범위 조건 컬럼은 뒤에 두는 경우가 많다.
- 선두 컬럼을 쓰지 않으면 인덱스 효과가 크게 줄 수 있다.

`(sub_id, use_dt)` 인덱스는 `sub_id = 1001 AND use_dt >= ...`에는 잘 맞지만, `use_dt >= ...`만 있는 조건에는 덜 맞는다.

### 21.8 커버링 인덱스와 Index-Only Scan

쿼리에 필요한 컬럼이 모두 인덱스에 있으면 실제 테이블을 읽지 않고 인덱스만으로 결과를 만들 수 있다. 이를 커버링 인덱스 또는 Index-Only Scan과 연결해서 이해한다.

```sql
CREATE INDEX idx_usage_cover
    ON usage_log (sub_id, use_dt)
    INCLUDE (bytes);

SELECT use_dt, bytes
FROM usage_log
WHERE sub_id = 1001;
```

위 쿼리는 검색 조건에 `sub_id`를 쓰고, 결과로 `use_dt`, `bytes`를 요구한다. 인덱스에 이 정보가 모두 있으면 힙 접근을 줄일 수 있다.

단, 인덱스에 컬럼을 많이 포함하면 인덱스 크기가 커진다. 인덱스가 커지면 캐시에 덜 올라가고, 쓰기 비용도 증가한다. 따라서 커버링 인덱스도 조회 패턴이 명확할 때 사용해야 한다.

### 21.9 선택도와 인덱스 대상 컬럼

선택도는 조건을 통과하는 행의 비율이다.

```text
선택도 = 조건을 만족하는 행 수 / 전체 행 수
```

선택도가 낮다는 말은 결과가 적게 나온다는 뜻이다. 예를 들어 100만 명 중 전화번호 하나로 1명을 찾으면 선택도가 매우 낮다. 이런 조건은 인덱스에 유리하다.

선택도가 높다는 말은 결과가 많이 나온다는 뜻이다. 예를 들어 전체 회원 중 `status = 'ACTIVE'`가 90%라면 대부분의 행을 읽어야 한다. 이 경우 인덱스를 타고 수많은 행을 랜덤으로 접근하는 것보다 테이블을 순차적으로 읽는 편이 나을 수 있다.

| 컬럼 예시 | 선택도 | 인덱스 효과 |
|---|---|---|
| 이메일, 전화번호, 고객ID | 낮음 | 좋음 |
| 성별, Y/N 여부, 대부분이 같은 상태값 | 높음 | 제한적 |
| 날짜 | 조건 범위에 따라 다름 | 기간 조회 패턴에 따라 유용 |

원본 노트에는 “높은 선택도(좋음)”이라고 적혀 있지만, 문맥상 “값의 종류가 다양하고 결과를 크게 좁힐 수 있는 컬럼”을 의미한다. SQL 튜닝에서 일반적으로는 `조건 선택도는 낮을수록 인덱스에 유리하다`고 정리하는 편이 덜 헷갈린다.

요약하면, 인덱스는 많이 걸러지는 조건, 자주 쓰는 조인 조건, 정렬과 범위 조회에 맞춰 설계한다.

## 22. 실행 계획 분석

### 22.1 실행 계획의 의미

실행 계획은 옵티마이저가 SQL을 어떻게 실행할지 세운 작업 지도다.

```sql
EXPLAIN
SELECT *
FROM subscription
WHERE status = 'ACTIVE';
```

예상 출력은 다음과 비슷하다.

```text
Seq Scan on subscription
  (cost=0.00..1850.00 rows=9800 width=64)
  Filter: (status = 'ACTIVE')
```

| 항목 | 의미 |
|---|---|
| Seq Scan | 테이블 전체를 순차적으로 읽음 |
| cost | 옵티마이저가 계산한 상대 비용 |
| rows | 예상 행 수 |
| width | 예상 행 크기 |
| Filter | 읽은 행 중 조건으로 거르는 작업 |

### 22.2 EXPLAIN과 EXPLAIN ANALYZE

| 명령 | 실행 여부 | 보여주는 것 |
|---|---|---|
| EXPLAIN | 실제 실행하지 않음 | 예상 실행 계획 |
| EXPLAIN ANALYZE | 실제 실행함 | 예상 + 실제 시간과 실제 행 수 |

`EXPLAIN ANALYZE`는 실제로 쿼리를 실행한다. SELECT는 조회라 부담이 상대적으로 작지만, INSERT, UPDATE, DELETE에 붙이면 실제 변경이 일어날 수 있으므로 주의해야 한다. 변경 쿼리를 분석할 때는 트랜잭션으로 감싸고 롤백하는 식의 안전장치가 필요하다.

예상 rows와 실제 rows가 크게 다르면 통계 정보가 낡았거나 조건의 분포를 옵티마이저가 잘못 추정했을 가능성이 있다.

### 22.3 실행 계획 트리 읽기

실행 계획은 트리 형태다. 보통 안쪽 또는 들여쓰기가 깊은 노드가 먼저 실행되고, 그 결과가 위쪽 노드로 전달된다.

```text
Hash Join
  -> Seq Scan on subscription
  -> Hash
       -> Index Scan on customer
```

읽는 순서는 대략 다음과 같다.

1. `customer`를 인덱스로 읽는다.
2. 읽은 결과로 해시 테이블을 만든다.
3. `subscription`을 순차 스캔한다.
4. 두 결과를 Hash Join으로 결합한다.

### 22.4 cost 해석

`cost=0.00..1850.00`에서 앞 숫자는 시작 비용이고, 뒤 숫자는 전체 비용이다. cost는 초 단위 시간이 아니라 옵티마이저 내부의 상대 점수다.

중요한 것은 절대값보다 상대 비교다. 같은 SQL을 여러 방식으로 실행할 수 있을 때 옵티마이저는 비용이 낮다고 판단한 계획을 선택한다.

초심자는 cost를 “실제 실행 시간”으로 착각하기 쉽다. cost는 예측값이고, 실제 시간은 `EXPLAIN ANALYZE`를 봐야 한다.

### 22.5 Buffers

`EXPLAIN (ANALYZE, BUFFERS)`를 사용하면 각 노드가 읽은 블록 수를 볼 수 있다.

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM usage_log
WHERE sub_id = 1001;
```

```text
Buffers: shared hit=120 read=8500
```

| 항목 | 의미 |
|---|---|
| shared hit | 메모리 캐시에서 읽은 블록 |
| shared read | 디스크에서 읽은 블록 |

디스크 read가 많으면 I/O 비용이 크다는 뜻이다. 실행 시간이 매번 환경에 따라 흔들릴 수 있으므로, 튜닝에서는 시간뿐 아니라 읽은 블록 수를 함께 보는 것이 좋다.

### 22.6 스캔 방식

| 스캔 방식 | 의미 | 유리한 상황 |
|---|---|---|
| Seq Scan | 테이블 전체 순차 읽기 | 작은 테이블, 대부분 행 필요 |
| Index Scan | 인덱스로 위치 찾고 테이블 접근 | 소수 행 조회 |
| Index-Only Scan | 인덱스만 읽고 결과 반환 | 필요한 컬럼이 인덱스에 모두 있음 |
| Bitmap Scan | 조건에 맞는 위치를 모아 블록 단위로 읽음 | 중간 규모 결과 |

Seq Scan은 무조건 나쁜 것이 아니다. 테이블 대부분을 읽어야 한다면 전체를 순차적으로 읽는 것이 더 빠를 수 있다. 반대로 결과가 소수인데 Seq Scan이 나온다면 인덱스 부재, 조건 작성 문제, 통계 문제를 의심할 수 있다.

### 22.7 느린 쿼리 식별

PostgreSQL에서는 `pg_stat_statements` 같은 확장을 사용해 자주 실행되고 오래 걸리는 쿼리를 찾을 수 있다.

```sql
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

| 컬럼 | 의미 |
|---|---|
| calls | 호출 횟수 |
| mean_exec_time | 평균 실행 시간 |
| total_exec_time | 총 실행 시간 |

튜닝 우선순위는 평균 시간이 긴 쿼리만 보면 안 된다. 평균은 짧아도 호출이 매우 많아 전체 시간을 많이 쓰는 쿼리가 더 중요할 수 있다.

### 22.8 병목 진단 체크리스트

| 질문 | 가능한 원인 | 대응 |
|---|---|---|
| 풀스캔이 발생하는가? | 인덱스 부재, 인덱스 미사용 | 인덱스 설계, 조건 수정 |
| 예상 rows와 실제 rows 차이가 큰가? | 통계 정보 문제 | ANALYZE로 통계 갱신 |
| 정렬이나 해시가 디스크로 넘치는가? | 메모리 부족, 대량 정렬 | work_mem 조정, 인덱스 정렬 활용 |
| 많이 읽고 나중에 버리는가? | 필터 적용이 늦음 | 조건을 앞 단계에서 적용 |
| 조인 방식이 부적절한가? | 행 수 추정 오류, 인덱스 부재 | 통계, 인덱스, SQL 구조 점검 |

요약하면, 실행계획은 “왜 느린지”를 추측이 아니라 근거로 확인하기 위한 도구다.

## 23. 쿼리 리라이팅과 튜닝

### 23.1 쿼리 리라이팅의 의미

쿼리 리라이팅은 같은 결과를 내면서 옵티마이저가 더 좋은 실행계획을 선택할 수 있도록 SQL을 다시 쓰는 작업이다.

리라이팅의 목적은 다음과 같다.

- 인덱스를 사용할 수 있는 조건으로 바꾼다.
- 읽는 행과 컬럼을 줄인다.
- 불필요한 정렬, 중복 제거, 서브쿼리를 없앤다.
- 행별 반복 처리를 집합 처리로 바꾼다.

### 23.2 SARGable 조건

SARGable은 Search ARGument able의 줄임말이다. 인덱스 검색 조건으로 사용할 수 있는 형태라는 뜻이다.

나쁜 예시는 컬럼에 함수나 연산을 씌우는 것이다.

```sql
WHERE EXTRACT(YEAR FROM use_dt) = 2026
```

`use_dt` 컬럼 값마다 연도를 뽑아 비교해야 하므로 일반적인 인덱스 범위 탐색이 어려워질 수 있다.

좋은 형태는 컬럼 자체를 그대로 두고 비교값을 바꾸는 것이다.

```sql
WHERE use_dt >= DATE '2026-01-01'
  AND use_dt <  DATE '2027-01-01'
```

다른 예시는 다음과 같다.

```sql
-- 나쁜 형태
WHERE fee * 1.1 > 100000

-- 좋은 형태
WHERE fee > 100000 / 1.1
```

핵심은 인덱스 컬럼을 가공하지 않는 것이다.

### 23.3 필요한 컬럼과 행만 읽기

`SELECT *`는 편하지만 튜닝 관점에서는 불리할 수 있다. 필요 없는 컬럼까지 읽으면 I/O와 네트워크 전송량이 늘고, Index-Only Scan 가능성도 낮아진다.

```sql
-- 불필요한 컬럼까지 모두 조회
SELECT *
FROM usage_log
WHERE sub_id = 1001;

-- 필요한 컬럼만 조회
SELECT use_dt, bytes
FROM usage_log
WHERE sub_id = 1001
ORDER BY use_dt
LIMIT 100;
```

필터 조건은 가능하면 일찍 적용해 중간 결과를 줄이는 것이 좋다. 집계가 필요하다면 먼저 작은 단위로 집계한 뒤 조인하는 방식도 자주 사용한다.

### 23.4 불필요한 연산 제거

다음 연산은 필요할 때만 사용해야 한다.

| 연산 | 비용 |
|---|---|
| DISTINCT | 중복 제거를 위한 정렬 또는 해시 비용 |
| ORDER BY | 정렬 비용 |
| UNION | 중복 제거 비용 |
| 깊은 중첩 서브쿼리 | 가독성과 최적화 부담 |

중복이 없거나 중복을 허용해도 되면 `UNION`보다 `UNION ALL`이 낫다. 정렬이 필요 없는 화면이나 중간 단계라면 `ORDER BY`를 제거할 수 있다.

### 23.5 집합적 사고

SQL은 절차형 언어가 아니라 선언형, 집합 지향 언어다. 한 행씩 반복 처리하는 방식보다 한 번에 집합으로 처리하는 방식이 일반적으로 더 적합하다.

나쁜 패턴은 N+1 조회다.

```text
고객 1명 조회
각 고객마다 가입 조회를 1번씩 반복
```

좋은 패턴은 조인이나 IN/EXISTS를 사용해 한 번에 처리하는 것이다.

```sql
SELECT c.name, s.sub_id
FROM customer c
LEFT JOIN subscription s
  ON c.cust_id = s.cust_id;
```

행별 UPDATE도 조건 기반 일괄 UPDATE로 바꿀 수 있다.

```sql
UPDATE subscription
SET status = 'PAUSED'
WHERE last_payment_dt < CURRENT_DATE - INTERVAL '30 days';
```

### 23.6 서브쿼리 리라이팅

SELECT 절의 무거운 상관 스칼라 서브쿼리는 행마다 반복 계산될 수 있다.

```sql
SELECT c.name,
       (SELECT COUNT(*)
        FROM subscription s
        WHERE s.cust_id = c.cust_id) AS cnt
FROM customer c;
```

고객이 N명이면 논리적으로 COUNT가 N번 수행되는 구조다. 이를 먼저 집계한 뒤 조인하는 형태로 바꿀 수 있다.

```sql
WITH sub_count AS (
    SELECT cust_id, COUNT(*) AS cnt
    FROM subscription
    GROUP BY cust_id
)
SELECT c.name, sc.cnt
FROM customer c
LEFT JOIN sub_count sc
  ON c.cust_id = sc.cust_id;
```

이 방식은 가입 테이블을 한 번 집계하고 고객 테이블과 조인하므로 대량 데이터에서 더 안정적일 수 있다.

### 23.7 페이지네이션

페이지네이션은 큰 목록을 일정 개수씩 끊어 조회하는 방식이다.

```sql
SELECT *
FROM usage_log
ORDER BY use_dt DESC
OFFSET 10000
LIMIT 20;
```

OFFSET이 커질수록 앞의 10000건을 건너뛰기 위해 많은 행을 읽어야 할 수 있다. 깊은 페이지에서는 마지막으로 본 키를 기준으로 다음 페이지를 가져오는 키셋 페이지네이션이 더 유리할 수 있다.

```sql
SELECT *
FROM usage_log
WHERE use_dt < TIMESTAMP '2026-07-01 10:00:00'
ORDER BY use_dt DESC
LIMIT 20;
```

SQLD에서 깊게 다루는 주제는 아니지만, `ORDER BY + LIMIT/OFFSET`의 비용을 이해하는 데 도움이 된다.

### 23.8 집계 튜닝

집계 튜닝은 반복되는 집계 계산을 줄이거나, 집계에 필요한 읽기 비용을 낮추는 것이다.

| 방식 | 설명 | 적합한 상황 |
|---|---|---|
| Materialized View | 집계 결과를 저장 | 실시간성이 덜 중요한 리포트 |
| 집계 테이블 | 배치로 요약 데이터 적재 | 대시보드, 통계 화면 |
| Index-Only Scan | 인덱스만으로 집계 | 필요한 컬럼이 인덱스에 있음 |
| 근사치 사용 | 정확한 COUNT 대신 통계값 사용 | 빠른 추정이 필요한 경우 |

정확한 실시간 결과가 반드시 필요하면 매번 원본을 집계해야 할 수 있다. 반대로 대시보드처럼 몇 분 전 데이터도 허용된다면 사전 집계가 효과적이다.

### 23.9 정렬 튜닝

`ORDER BY`는 정렬 비용을 만든다. 하지만 인덱스가 이미 원하는 순서로 정렬되어 있다면 DBMS가 별도 정렬을 줄일 수 있다.

```sql
CREATE INDEX idx_usage_sub_dt
    ON usage_log (sub_id, use_dt DESC);

SELECT use_dt, bytes
FROM usage_log
WHERE sub_id = 1001
ORDER BY use_dt DESC
LIMIT 100;
```

위 쿼리는 `sub_id`로 범위를 좁히고, 그 안에서 `use_dt DESC` 순서로 바로 읽을 가능성이 있다.

요약하면, 리라이팅의 핵심은 인덱스가 일할 수 있는 조건을 만들고, DBMS가 읽고 정렬하고 중복 제거해야 하는 양을 줄이는 것이다.

## 24. 파티셔닝

### 24.1 파티셔닝의 의미

파티셔닝은 큰 테이블을 논리적으로 하나의 테이블처럼 사용하면서, 물리적으로는 여러 조각으로 나누어 저장하는 기법이다.

예를 들어 `usage_log`가 수년 치 사용량 로그를 담고 있다면 월별로 파티션을 나눌 수 있다.

```text
usage_log
  -> usage_2026_01
  -> usage_2026_02
  -> usage_2026_03
```

사용자는 `usage_log`를 조회하지만, DBMS는 조건에 맞는 파티션만 읽을 수 있다.

### 24.2 RANGE 파티셔닝

날짜 기준 파티셔닝은 보통 RANGE 파티셔닝으로 설명한다.

```sql
CREATE TABLE usage_log (
    sub_id BIGINT,
    use_dt DATE,
    bytes BIGINT
)
PARTITION BY RANGE (use_dt);

CREATE TABLE usage_2026_02
PARTITION OF usage_log
FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
```

PostgreSQL RANGE 파티션의 `FROM`은 포함, `TO`는 제외다.

```text
FROM ('2026-02-01') TO ('2026-03-01')
= 2026-02-01 이상, 2026-03-01 미만
```

이 방식은 말일이 28일인지 29일인지 30일인지 31일인지 신경 쓰지 않아도 되므로 날짜 범위 설계에 안전하다.

### 24.3 파티션 프루닝

파티션 프루닝은 조건에 맞지 않는 파티션을 읽지 않는 최적화다.

```sql
SELECT *
FROM usage_log
WHERE use_dt >= DATE '2026-02-01'
  AND use_dt <  DATE '2026-03-01';
```

위 조건이 있으면 DBMS는 2026년 2월 파티션만 읽으면 된다고 판단할 수 있다. 반대로 파티션 키인 `use_dt` 조건이 없으면 여러 파티션을 모두 읽어야 할 수 있다.

### 24.4 파티셔닝의 장단점

| 구분 | 내용 |
|---|---|
| 장점 | 필요한 파티션만 읽어 대량 조회를 줄일 수 있다. |
| 장점 | 오래된 파티션 삭제나 보관이 쉬워진다. |
| 장점 | 파티션 단위 관리와 백업이 가능하다. |
| 단점 | 설계와 운영이 복잡해진다. |
| 단점 | 파티션 키가 조건에 없으면 효과가 줄어든다. |
| 단점 | 너무 많은 파티션은 관리 비용을 늘린다. |

요약하면, 파티셔닝은 큰 테이블을 잘라 관리하고 필요한 조각만 읽게 하는 기법이다. 날짜 조건이 자주 들어가는 대용량 로그 테이블에서 특히 자주 사용된다.

## 25. SQLD 기출 유형 기반 헷갈리는 포인트

### 25.1 모델링 파트

| 자주 나오는 유형 | 헷갈리는 보기 | 판단 기준 |
|---|---|---|
| 후보키 조건 | 유일하기만 하면 후보키다 | 후보키는 유일성 + 최소성 |
| 기본키 특징 | 기본키는 NULL 가능 | 기본키는 NOT NULL |
| 외래키 특징 | 외래키는 항상 NOT NULL | 별도 제약 없으면 NULL 가능 |
| M:N 관계 | M:N을 그대로 테이블 하나의 FK로 구현 | 교차 엔터티로 해소 |
| 제2정규형 | 모든 함수 종속 제거 | 부분 함수 종속 제거 |
| 제3정규형 | 복합키 일부 종속 제거 | 이행 함수 종속 제거 |
| 반정규화 | 무조건 나쁜 설계 | 성능 목적이면 선택적으로 가능 |

### 25.2 SQL 기본 파트

| 자주 나오는 유형 | 헷갈리는 보기 | 판단 기준 |
|---|---|---|
| SQL 분류 | TRUNCATE는 DML | TRUNCATE는 DDL |
| DELETE/TRUNCATE/DROP | 셋 다 같은 삭제 | 행 일부 삭제, 전체 초기화, 객체 삭제 |
| SELECT 실행 순서 | WHERE에서 SELECT 별칭 사용 가능 | WHERE가 SELECT보다 먼저 |
| NULL 비교 | `col = NULL` | `IS NULL` 사용 |
| COUNT | COUNT(col)은 NULL 포함 | COUNT(col)은 NULL 제외 |
| BETWEEN | 양 끝 제외 | 양 끝 포함 |
| LIKE `_` | 여러 글자 | 정확히 한 글자 |

### 25.3 조인 파트

| 자주 나오는 유형 | 헷갈리는 보기 | 판단 기준 |
|---|---|---|
| INNER JOIN | 한쪽만 있어도 출력 | 양쪽 매칭될 때만 출력 |
| LEFT JOIN | 오른쪽 조건을 WHERE에 둬도 왼쪽 모두 보존 | WHERE 조건으로 NULL 행 제거 가능 |
| CROSS JOIN | 조인 조건이 필요 | 모든 조합이므로 조건 없음 |
| SELF JOIN | 특별한 테이블만 가능 | 같은 테이블을 별칭으로 두 번 참조 |
| 카테시안 곱 | 행 수 감소 | 두 집합의 모든 조합으로 증가 |

### 25.4 서브쿼리 파트

| 자주 나오는 유형 | 헷갈리는 보기 | 판단 기준 |
|---|---|---|
| 스칼라 서브쿼리 | 여러 행 반환 가능 | 1행 1열이어야 함 |
| EXISTS | SELECT 컬럼 값이 중요 | 존재 여부만 중요 |
| IN vs EXISTS | 항상 완전히 동일 | NULL, 중복, 최적화 맥락 주의 |
| NOT IN | NULL 있어도 안전 | NULL 있으면 결과가 비정상적으로 비어질 수 있음 |
| ANY/ALL | `> ANY`는 `> MAX` | `> ANY`는 `> MIN`, `> ALL`은 `> MAX` |

### 25.5 집계와 윈도우 함수 파트

| 자주 나오는 유형 | 헷갈리는 보기 | 판단 기준 |
|---|---|---|
| GROUP BY | 개별 행 유지 | 그룹별로 행 압축 |
| 윈도우 함수 | 행 압축 | 행 유지 |
| WHERE/HAVING | 집계 조건은 WHERE | 집계 조건은 HAVING |
| RANK | 동점 후 순위 안 건너뜀 | RANK는 건너뜀 |
| DENSE_RANK | 동점 후 순위 건너뜀 | DENSE_RANK는 안 건너뜀 |
| ROW_NUMBER | 동점 같은 번호 | 항상 고유 번호 |
| ROLLUP | 모든 조합 소계 | 계층적 소계 |
| CUBE | 일부 조합만 | 모든 조합 |

### 25.6 트랜잭션 파트

| 자주 나오는 유형 | 헷갈리는 보기 | 판단 기준 |
|---|---|---|
| 원자성 | 제약조건 만족 | 전부 성공 또는 전부 실패 |
| 일관성 | 동시 실행 차단 | 제약과 규칙 만족 |
| 고립성 | 커밋 결과 보존 | 동시성 간섭 차단 |
| 지속성 | 중간 저장점 | 커밋 결과 영구 보존 |
| Dirty Read | 커밋된 값 재조회 변화 | 커밋 안 된 값 읽기 |
| Non-repeatable Read | 행 수 변화 | 같은 행 값 변화 |
| Phantom Read | 같은 행 값 변화 | 조건 결과 행 수 변화 |

### 25.7 인덱스와 실행계획 파트

| 자주 나오는 유형 | 헷갈리는 보기 | 판단 기준 |
|---|---|---|
| 인덱스 효과 | 인덱스는 항상 빠름 | 결과가 많으면 Seq Scan이 나을 수 있음 |
| 인덱스 개수 | 많을수록 좋음 | 쓰기 비용과 공간 비용 증가 |
| 복합 인덱스 | 뒤 컬럼만 써도 항상 효율적 | 선두 컬럼 사용 여부가 중요 |
| 선택도 | 많이 조회될수록 인덱스 유리 | 결과가 적게 남을수록 인덱스 유리 |
| SARGable | 컬럼에 함수 적용해도 인덱스 동일 | 컬럼 가공은 인덱스 사용을 방해할 수 있음 |
| EXPLAIN | 실제 실행 결과 | 예상 실행 계획 |
| EXPLAIN ANALYZE | 실행하지 않음 | 실제 실행하고 실제 행 수와 시간 표시 |
| cost | 초 단위 시간 | 옵티마이저의 상대 비용 |
| Seq Scan | 항상 나쁜 계획 | 대부분 행을 읽으면 정상일 수 있음 |
| Index-Only Scan | 항상 가능 | 필요한 컬럼이 인덱스에 있어야 함 |
| 파티션 프루닝 | 모든 조건에서 발생 | 파티션 키 조건이 중요 |

## 26. 초심자용 암기 문장

- 데이터베이스는 데이터를 그냥 모아 둔 파일이 아니라, 구조와 규칙을 가진 공유 저장소다.
- DBMS는 데이터 정의, 조작, 제어, 회복, 동시성을 담당한다.
- 스키마는 데이터가 아니라 데이터 구조다.
- 후보키는 유일성과 최소성을 모두 만족한다.
- 기본키는 NULL이 될 수 없고 중복될 수 없다.
- 외래키는 참조 무결성을 위한 키이며, 별도 NOT NULL이 없으면 NULL 가능하다.
- 제1정규형은 한 칸에 값 하나다.
- 제2정규형은 복합키의 일부에만 의존하는 속성을 제거한다.
- 제3정규형은 비키 속성끼리의 의존을 제거한다.
- 반정규화는 성능을 위한 선택이지 정규화를 몰라도 된다는 뜻이 아니다.
- DELETE는 행 삭제, TRUNCATE는 전체 행 초기화, DROP은 객체 삭제다.
- WHERE는 그룹 전, HAVING은 그룹 후다.
- SELECT 별칭은 WHERE에서 일반적으로 사용할 수 없다.
- INNER JOIN은 양쪽 매칭만, LEFT JOIN은 왼쪽 보존이다.
- LEFT JOIN 후 오른쪽 테이블 조건을 WHERE에 두면 왼쪽 보존 행이 사라질 수 있다.
- CROSS JOIN은 모든 조합이다.
- 스칼라 서브쿼리는 1행 1열이어야 한다.
- EXISTS는 행 존재 여부만 본다.
- NOT IN은 NULL이 섞이면 위험하다.
- GROUP BY는 행을 압축하고, 윈도우 함수는 행을 유지한다.
- RANK는 순위를 건너뛰고, DENSE_RANK는 건너뛰지 않는다.
- COMMIT은 확정, ROLLBACK은 취소, SAVEPOINT는 부분 취소 지점이다.
- Dirty Read는 커밋 안 된 값 읽기다.
- Non-repeatable Read는 같은 행 값이 바뀌는 것이다.
- Phantom Read는 같은 조건의 행 수가 바뀌는 것이다.
- 인덱스는 읽기를 빠르게 할 수 있지만 쓰기와 저장 공간 비용을 만든다.
- 복합 인덱스는 선두 컬럼이 중요하다.
- 조건 선택도는 낮을수록 인덱스에 유리하다.
- 컬럼에 함수나 연산을 씌우면 인덱스 사용이 어려워질 수 있다.
- EXPLAIN은 예상 계획이고, EXPLAIN ANALYZE는 실제 실행 결과까지 보여준다.
- Seq Scan은 항상 나쁜 것이 아니라 많이 읽어야 할 때 정상 선택일 수 있다.
- 파티셔닝은 큰 테이블을 나누고 파티션 키 조건으로 필요한 조각만 읽게 하는 기법이다.

## 27. 학습 순서 추천

1. `day1.md`의 DBMS, 모델링, 키, 정규화, DDL/DML을 먼저 익힌다.
2. `day2.md`의 JOIN을 그림 없이도 말로 설명할 수 있게 만든다.
3. LEFT JOIN의 `ON`과 `WHERE` 차이를 직접 예제로 확인한다.
4. NULL 처리, COUNT, NOT IN 함정을 따로 암기한다.
5. GROUP BY와 HAVING 문제를 풀어 SELECT 실행 순서를 체화한다.
6. 윈도우 함수는 `PARTITION BY`, `ORDER BY`, `ROWS BETWEEN` 순서로 나눠 이해한다.
7. 트랜잭션은 ACID와 동시성 이상현상을 표로 암기한 뒤 예시로 구분한다.
8. `day3.md`의 인덱스는 “선택도, 복합 인덱스 선두 컬럼, SARGable 조건” 순서로 익힌다.
9. 실행계획은 `Seq Scan`, `Index Scan`, `Index-Only Scan`, `Hash Join`, `Nested Loop` 이름을 보고 왜 선택됐는지 말해 본다.
10. 튜닝은 추측으로 하지 말고 `EXPLAIN`, `EXPLAIN ANALYZE`, `BUFFERS`, 예상 rows와 실제 rows 차이를 근거로 판단한다.

## 28. 참고 출처

- 한국데이터산업진흥원 데이터자격시험 SQLD 자격소개 및 출제범위: https://www.dataq.or.kr/www/sub/a_04.do
