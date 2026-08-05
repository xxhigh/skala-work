# 데이터 분석을 위한 파이썬의 이해
데이터 시각화

결측치: 데이터의 내용이 비어있거나, 항목과 다른 내용이 있는 경우
이상치: 평균의 데이터 범주는 벗어나는 값을 가진 경우
EDA: 탐색적 데이터 분석(Exploratory Data Analysis) - 본격적으로 기계학습(머신러닝) 모델을 만들거나 통계적 검정을 하기 전에, "이 데이터가 어떻게 생겼는지 손으로 만져보고 눈으로 확인하며 파악하는 모든 과정"
귀무가설: 차이 혹은 효과가 없을 가정하고, 보통 이 가정이 거짓임을 기대하며 분석을 시작
대립가설: 귀무가설과 대립하며, 기존 생각과 다른 주장의 차이가 존재를 있다고 가정, 귀무가설을 무너뜨리고 최종적으로 채택하고 싶어하는 주인공 가설
t-test: 두 집단 간에 진짜 차이가 있는지, 아니면 단순 우연인지 검사, 데이터가 숫자형일 경우 사용 (예: 남녀의 키 분포도)
카이제곱: 두 집단 간에 진짜 차이가 있는지, 아니면 단순 우연인지 검사, 데이터가 범주형일 경우 사용 (예: 남녀에 따라 선호하는 스마트폰 브랜드 연관성)

## Pandas

Series: 1차원 레이블 배열 - DataFrame의 한 컬럼, 정렬 조인이 강점 (Numpy + 인덱스)
DataFrame: 2차원 레이블 표 - 내부는 NumPy 배열

**언제 사용?**
- 수백만 행 이하 EDA,탐색
- 시각화 라이브러리
- 주피터 탐색 위주

기초 확인 (가장 먼저 해야할 것)
.shape() # (행수, 열수)
.info() # 타입, 결측, 메모리
.describe(); # 수치 기술통계
.describe(include='all') # 범주형 포함 통계

유용한 함수(행 샘플 확인)
head
tail
sample

결측치 처리 방법
- 이전 행의 데이터를 덮어쓰기
- 이전, 다음 열의 데이터 덮어쓰기
- 삭제
- 새로 작성

결측치를 처리해야하는 이유 - 잘못된 값으로 통계처리에 대한 오류를 예방하기 위해

### 결측치,이상치 탐지 및 처리
isna().sum() 함수로 컬럼별 결측치 수 탐지

MCAR - 데이터는 있지만 제대로 돌아가지 않음
MAR - 대상별로 데이터가 다름
MNAR - 의도적으로 데이터가 다름

사분위 범위로 이상치 탐지, 제거
```python
# IQR 이상치 탐지
Q1 = df['amount'].quantile(0.25)
Q3 = df['amount'].quantile(0.75)
IQR = Q3 - Q1
lo, hi = Q1 - 1.5*IQR, Q3 + 1.5*IQR
df_clean = df[df['amount'].between(lo, hi)]
print(f'이상치 {(~df["amount"].between(lo,hi)).sum()}건
제거')
```

### 집계와 결합

groupby + agg(): 다중 집계 한 번에
named aggregation: 결과 컬럼명 지정 - 기준 데이터를 컬럼명을 지정해서 새로운 데이터집합을 만들어 사용하기도 함

merge: SQL JOIN
join: 인덱스 기준 결합

merge vs join 차이
merge: 컬럼 기준 | join: 인덱스 기준

### Copy on Write

원본 데이터를 수정할 수 없도록 경고와 오류를 출력 -> 명시적 copy() 또는 assign() 사용

```python
# Pandas 2.x에서 ChainedAssignmentError
df_seoul = df[df['region'] =='서울']
df_seoul['amount'] = df_seoul['amount'] * 1.1 # 경고!

# 방법 1: .copy() 명시
df_seoul = df[df['region'] == '서울'].copy()
df_seoul['amount'] *= 1.1

# 방법 2: .loc 직접 수정
df.loc[df['region'] =='서울', 'amount'] *= 1.1
```

### apply vs vectorized 연산

apply - 행/열 단위 Python 함수를 적용(Python 루프) # df['upper'] = df['name'].apply(lambda x: x.upper())
벡터화 연산 - NumPy 수준 속도 # df['upper'] = df['name'].str.upper()

-> apply 는 편하지만 느림

## Polars + DuckDB

**Pandas의 한계**
1. 싱글스레드
2. 수백만 행 이상에서 속도 저하
3. 메모리 사용량이 원본 데이터의 5~10배
4. CoW 전까지 복사 많음

**Polars - Rust + Arrow**
- 멀티 스레드 활용
- Lazy API로 쿼리 최적화
- Pandas 대비 5~20배 빠름
- Apache Arrow 기반

**DuckDB - 파일 직접 SQL**
- CSV, Parquet 파일을 로딩 없이 SQL 분석
- 서버 없음
- 로컬 데이터 웨어하우스급 성능
* 데이터 웨어하우스: 일종의 분산 데이터으로 실시간으로 데이터가 쌓이는 라이브 서비스에서 분석을 하기위해 데이터를 얻어올 때 복사를 함.

**Arrow 생태계**
- Polars <> DuckDB <> PyArrow <> Pandas 간 Arrow 포맷으로 제로카피 변환
- 데이터 이동 비용 최소

### Polars - Eager API vs Lazy API

import polars as pl

Eager:즉시 실행함 탐색, 소규모에 적합 | 원본 자체에서 작업

Lazy: scan함수, 실행 계획 수립 후 collect | 원본의 뷰를 뽑아서 작업

```py
# Lazy (실행 계획 최적화)
result = (
pl.scan_csv('large.csv',
schema_overrides={'amount': pl.Float64})
.filter(pl.col('region') ==
'서울')
.filter(pl.col('amount') > 0)
.group_by('category')
.agg([pl.col('amount').sum().alias('total'),
pl.count().alias('cnt')])
.sort('total', descending=True)
.collect()
```

schema_overrides - 컬럼 타입을 명시(성능향상)

## 데이터 시각화

시각화를 했을 때, 텍스트로 보여지는 것보다 설득의 효과가 더 좋음.
-> 의사결정자 설득

히스토그램,박스플롯으로 분포 파악, 상관관계, 히트맵으로 결측치 패턴 확인

### Matplotlib - 기초, 서브
 
### Seaborn - 통계 시각화 특화

### Plotly Express - 인터랙티브 시각화

### Altair - 선언형 시각화

도구 선택 기준
- 보고서 논문: Matplotlib / Seaborn
- 인터랙티브 대시보드: Plotly
- 빠른 EDA: Altair
- 웹공유: Streamlit(소개 수준)

## 기초 통계와 ML 파이프라인 연결

### 기술통계

중심 경향: 평군, 중앙값, 최빈값 차이
산포도: 분산, 표준편차, IQR, 범위
분포 모양: 왜도(skewness), 첨도(kurtosis)
상관 행렬: -1 ~ +1, 
선형 관계 강도: 양의 상관: 1에 가까움 / 음의 상관: -1에 가까움
-- 둘 사이에 상관관계 (예: 기온이 높으면 수영복이 잘 팔린다.)

### 가설 검정 기초

귀무가설(H0) vs 대립가설(H1) 설정
유의수준 a = 0.05: p값 기준
t-test: 두 그룹 평균 차이 검정 (예: 여름에 수박이 매출이 높냐, 아이스크립이 매출이 높냐)
카이제곱: 범주형 변수 독립성 검정 (예: 지역과 구매여부의 독립성)

**p가 0.05 보다 작으면 그 가설(H0)은 기각** (통계적 유의)

### CRISP-DM
기술 중심이 아닌 문제 해결 중심 - 좋은 분석은 올바른 문제 정의에서 시작
업무 이해 -> 데이터 이해 -> 데이터 준비 -> 모델링 -> 평가 -> 배포

### sklearn Pipeline - 전처리 + 모델 통합
전처리 -> 모델을 하나의 객체로

### ML
통계 없이 ML은 블랙박스 - 평균, 분산, 상관계수를 모르면 피처 선택, 이상치 처리, 결과 해석이 불가능
데이터 이해가 먼저

joblib로 pipeline 전체 저장 -> 배포 환경에서 동일한 전처리 + 에측 보장 (MLOps의 기본)

## 분석 자동화와 파이프라인 설계

### schedule + cron
python 내 간단한 스케줄러
매일, 매주, 매시간 등 다양한 주기 설정
오류 발생 시 로깅 + 알림 패턴
macOS launchd / cron으로 os 레벨 스케쥴
subprocess로 외부 스크립트 실행 연동

### 분석 파이프라인 설계 = ETL(Extract, Transform, Load) 구조 원칙

좋은 파이프라인: 각 단계 분리 + 오류 기록 + 재현 가능 + 테스트 기능

```py
def run_pipeline(config: dict) -> dict:
logger.info(f'파이프라인 시작: {config}')
# E: Extract — 수집
raw = extract(config['source']) logger.info(f'수집 완료: {len(raw)}건')
# API / DB / 파일
# V: Validate — 검증 (Pydantic) !! 제일 중요함
validated, errors = validate(raw, schema=SalesRecord)
logger.warning(f'검증 오류: {len(errors)}건') if errors else None
```

## 분석 코드 구조화와 공유

### Jupyter vs .py 스크립트

### 분석 코드 구조화의 핵심 원칙

탐색과 재사용 분리

재현성 = 신뢰성

데이터는 git에 올리지 않는다

점진적 개선