---
aliases:
  - DL
tags:
  - Skala
  - DL
---
[[Day 2 - 머신러닝]] 이어서 계속.

## 딥러닝 학습 최적화 전략

### Gradient Vanishing
기울기 소실

- 역전파는 출력층에서 입력층 방향으로 각 층의 기울기를 계속 곱하며 기울기를 계산하게 됨
- 대부분 활성함수에 의해 기울기가 1보다 작기 때문에 앞쪽으로 갈수록 기울기가 작아짐.
- 입력에 가까운 층 가중치가 거의 업데이트되지 않는 현상
- **해결 방법**
	- ReLU 사용: 양수 구간에서 기울기 1을 유지
	- Batch Normalization: 입력값 분포를 정규화
	- He Initialization: 적절한 가중치 초기화
	- Residual Connection: 순전파 시 입력값을 여러 층 거치지 않고 출력에 직접 더해주는 구조

### Batch 처리

- 전체 데이터를 작은 그룹으로 나눠서 학습
- 배치 처리 이유: 메모리 부족, 계산 속도 느림, 업데이트가 너무 늦음

| 이름                                | 방식        | 비유            | 특징         |
| --------------------------------- | --------- | ------------- | ---------- |
| Batch Gradient Descent            | 전체 데이터 사용 | 모두 모여 신중하게 탐험 | 안정적이지만 느림  |
| Stochastic Gradient Descent (SGD) | 1개씩 사용    | 혼자 빠르게 탐험     | 빠르지만 불안정   |
| Mini-batch                        | 일부 묶음 사용  | 팀 단위 탐험       | 안정성과 속도 균형 |

### 에포크와 이터레이션

- 전체 데이터셋을 한 번 완전히 학습하는 것 = 1 에포크
- 여러 번 반복해야 제대로 학습됨
- 학습 중간중간 성능 검증(Validation) 진행

![[018_epoch.png]]

- overfitting 과 속도 느려짐을 주의

### 검증
제대로 가고 있는지 확인

- 에포크 단위로 중간중간 모델 성능 검증
- 데이터 분할로 학습 및 검증을 반복함
	- Training Set + Validation Set
	- Test Set: 최종 평가용으로 학습 완료 후 단 한 번만
- 학습 진행 중 과적합이 발생하면 -> Early Stopping

### Early Stopping
더 이상 좋아지지 않으면 멈추기

- 검증 손실이 개선되지 않으면 학습 중단
- 효과: 시간 낭비 방지 + 과적합 방지
- 또 다른 과적합 방지 방법: Dropout
- patience 설정을 통해 Early Stopping을 설정

![[019_EarlyStopping.png]]


### Dropout
랜덤하게 뉴런 끄기

- 학습 과정에서 신경망의 일부 뉴런을 무작위로 비활성화해서 학습하는 방법
- 효과
	- 특정 뉴런에만 의존하지 않음 (과적합 방지)
	- 학습할때마다 다른 구조 신경망을 학습 (앙상블 효과)

## 딥러닝 모델 평가

### 평가

- 검증은 학습 중 여러 번
- 평가는 학습 후 한번 만 진행
- 분류 문제 평가 지표: Accuracy, F1
- 회귀 문제 평가 지표: MAPE, MSE

### 딥러닝 전체 프로세스

![[020_DL_Process.png]]


## Linear Regression with DL

### 회귀분석에 대한 개념

> y = Wx + b

W: 회귀계수(ML), 가중치(DL)
b: 절편, Bias

선형 모델에서 알고 싶은 것?
- 알고 있는 것 (데이터 수집을 통해 DB에 저장된 값)
	- x: 독립변수(Feature)는 모델을 만들기 위해 입력되는 값
	- y: 종속변수(Target). 결과값으로 모델 예측값과 비교
- 알고 싶은 것
	- W: 가중치
	- b: 절편
	- 가중치와 절편은 파라미터라고 하고, 알고 있는 데이터(x,y)를 학습시켜 결정

### 회귀분석에서 파라미터 구하는 과정

1. 데이터 정의(x,y)
2. 선형 모델 정의(가설수립)
3. 오차 평가(최소제곱법)
4. 오차 최소화(Least Sqaures Method)
5. 파라미터 계산

### 딥러닝에서 파라미터 구하는 과정

1. 데이터 정의(Feature, Target)
2. 선형 모델 정의(가설수립)
3. 오차 평가, 손실 함수 정의(MSE)
4. 오차 최소화(경사하강법)
5. 파라미터 계산

### 선형회귀 vs 딥러닝

![[021_LRvsDL.png]]


## DL Architecture

### 용어 정리

**Model**
- 데이터를 입력받아 예측, 분류 등의 작업을 수행하는 학습된 프로그램
- 학습을 통해 X와 y의 관계를 표현하는 정보를 저장하고 있음.

**Algorithm**
- 문제를 해결하기 위한 절차나 계산 방법
- 딥러닝에서는 학습 방법, 최적화 절차, 또는 데이터 처리 방법 등을 알고리즘이라고 함
- ML에서는 학습 방법을 알고리즘이라고도 함

**Architecture**
- 딥러닝 신경망의 구조적 설계 방식
- Layer 구성, 층 간의 연결 방식, 데이터 흐름 등을 정의 (CNN, RNN, Transformer 등)

### 신경망 Architecture

1. Node: 신경망 계산이 이루어지는 최소 단위
2. Link: 노드와 노드 사이의 관계 (가중치)
3. Layer: 크게 3개 레이어로 구성 - 입력, 은닉, 출력
4. Network: 앞 선 노드, 링크, 레이어로 이루어진 전체 관계

### CNN

- 이미지 데이터 특징
	- 이미지는 픽셀의 집합으로 구성, 인접한 픽셀들은 서로 연관성이 높음

이미지처럼 공간 구조가 중요한 데이터에는 공간 정보를 유지하는 모델이 필요 => CNN

- CNN의 핵심은 합성곱(Convolution) 연산
- 합성곱 연산은 입력 데이터에 필터를 적용하여 특징을 추출하는 연산
- 이미지처럼 공간적 구조를 가진 데이터를 잘 처리하도록 설계된 신경망

![[022_cnn.png]]

#### 필터
이미지에서 특정 패턴을 감지하는 '탐지기' 역할

- 각 필터는 서로 다른 특징을 학습: 세로선 필터, 가로선 필터 등
- 필터 개수만큼 피처가 만들어짐
- 필터의 가중치값은 학습과정에서 손실을 줄이는 방향으로 자동 조정
- 각 필터가 만든 출력을 Feature Map 이라 함.

#### ReLU 활성화 함수

- 합성곱 자체는 선형 연산 -> ReLU로 비선형성 추가
- 합성곱 레이어는 항상 ReLU와 함께 사용
- Conv-ReLU-Pool이 CNN의 기본 블록

#### Pooling
중요한 특징은 유지하면서 노이즈 제거

- Feature Map의 크기를 줄임(다운 샘플링)
- 중요한 정보만 남기고 크기를 줄임
- 과적합 방지 및 계산량 감소, 처리 속도 향상
- Max Pooling
- Average Pooling

![[023_pooling.png]]


#### 평탄화
합성곱 층이 만든 Feature Map을 분류기 입력 형태로 바꿔주는 다리 역할

- 다차원 형태의 Feature Map을 1차원 벡터로 펼치는 작업
- 특징 맵을 신경망 학습을 위한 입력형태로 변환

### CNN 전체 아키텍처

- 전반부 Feature Extraction, 후반부 Classification 로 진행
- Feature Extraction 과정은 Conv-ReLU-Pool 블록 단위로 여러 번 반복

![[024_cnn_arch.webp]]
  
- 정형 데이터는 이런 Feature 추출하는 방법이 없음.
- 비정형은 가능

## RNN

일반 신경망의 한계
- 각 입력을 독립적으로 처리
- 이전 정보 기억 불가
- 순서 정보 손실
따라서 순서를 이해하는 인공지능이 필요함.

### Recurrent Neural Network
이전 정보를 기억하면서 다음 정보를 처리하는 신경망

- 순환 구조: 이전 시점의 출력이 다음 시점의 입력으로 사용
- 은닉 상태(hidden State): 과거 정보를 저장하는 "**기억 장치**"로 다음 연산에 사용
- Cell: 현재 입력과 과거 정보를 합쳐서 새로운 정보를 생성하는 "**연산 장치**"

초기 RNN에서는 tanh 함수를 사용 (-1 ~ 1)까지 처리할 수 있어서.

### RNN 구조

- 입력과 출력의 길이에 따라 다양한 형태로 설계 가능

1. One-To-Many: 하나의 입력에 대해 여러 개의 출력을 내보내는 구조 (텍스트 생성, 생성 모델에 주로 사용)
2. Many-To-One: 여러 개의 입력에 대해 단 한개의 출력을 내보내는 구조 (감정 분석, 분류/회귀 문제에 주로 사용)
3. Many-To-Many: 여러 개의 입력에 대해 여러 개의 출력을 내보내는 구조\[입력 길이 = 출력 길이] (품사 태깅, 개체명인식)

> Many-To-Many 유형 중 입력과 출력 길이가 다른 문제 (번역, 요약)을 효과적으로 해결하기 위해 Seq2Seq 구조가 등장

### LSTM(Long Short-Term Memory)
장기 기억이 가능한 RNN

- RNN의 문제: 문장이 길어질수록 앞의 정보를 잊어버림, 장기 의존성 학습에 한계가 있음
- LSTM은 "기억을 선택적으로 유지"하는 구조로, 장기 기억장치와 단기 기억장치를 분리
- Cell State: 장기 기억 저장 공간
- Hidden State: 다음 시점으로 전달할 단기 기억 저장 공간
- 3개의 Gate
	- Forget Gate: 버릴 정보 결정
	- Input Gate: 저장할 새 정보 결정
	- Output Gate: 출력할 정보 결정

![[025_lstm.png]]

- 그러나 계산량이 많고, RNN 보다 학습 시간이 길어짐
- 여전히 매우매우 긴 시퀀스에서는 한계가 존재

### Seq2Seq 구조
생성 모델의 기초

- 입력 시퀀스를 출력 시퀀스로 변환하는 전체 구조
- 시퀀스: 순서가 있는 데이터 (문장, 시계열 데이터, 음성)
- 전체 큰 구조가 Seq2Seq이고 내부적으로 RNN/LSTM은 그 구조를 구현하는데 사용

1. 입력과 출력의 길이가 다른 시퀀스 변환 문제를 효과적으로 해결한 구조
2. Encoder-Decoder 구조
	- 입력 이해(Encoder) 부분과 생성(Decoder) 부분을 분리하는 구조
	- LSTM 기반: Encoder(LSTM) -> \[context vector] -> Decoder(LSTM)

#### LSTM 기반 구조의 문제

1. Context Vector 병목 현상
	- 입력 문장을 하나의 Context Vector로 압축하여 전달 -> 문장이 길어질수록 중요한 정보가 손실될 위험
	- 개선하기 위해 Attention
2. 순차처리
	- 이전 계산이 끝나야 다음 계산 가능
	- 병렬 처리 불가능(긴 시퀀스 처리 시 학습 시간 증가)
	- GPU 활용 제한
	- 개선하기 위해 Transformer(Self-Attention 기반)

### Seq2Seq + Attention 구조
Decoder가 필요한 정보만 선택적으로 참조

- Encoder의 마지막 상태만 쓰는 게 아닌, Encoder의 모든 hidden state를 활용
- Attention 이전: 전체 문장을 다 읽은 후 "요약 노트 한장"만 보고 번역하는 것
- Attention 이후: 번역할 때마다 원문을 다시 보면서 필요한 부분을 선택적으로 참고하는 것

![[026_seq2attention.png]]

## Transformer

### Self-Attention

- 셀프 어텐션 이전까지는 단어를 순차적으로 처리함
- 셀프 어텐션은 문장 내 모든 단어가 서로를 동시에 참조
- 문장 내 각 단어가 다른 단어들과의 관련성(Attention Weight)을 계산하여 문맥을 이해하는 기술
- 종류
	- Cross-Attention: Decoder가 Encoder의 출력을 참조 -> 서로 다른 두 시퀀스 간의 관계 계산
	- Self-Attention: 같은 시퀀스 내의 단어들이 서로를 참조 -> 같은 시퀀스 내부의 관계 계산
- Self-Attention은 문맥을 계산하는 연산 방식이고, Transformer는 이를 중심으로 설계된 모델 구조

### Transformer

- RNN Seq2Seq + Attention의 한계
- Transformer의 핵심 아이디어
	- RNN 완전 제거
	- Self-Attention을 핵심 연산으로 사용 -> 모든 단어 동시에 처리
	- 단어 순서를 알기 위해 Positional Encoding 추가

![[027_transformer.png]]

### Transformer Attention 종류

- Encoder: Self-Attention
- Decoder: Masked Self-Attention + Cross-Attention 을 같이 사용

| 종류                    | 위치      | 역할                                    |
| --------------------- | ------- | ------------------------------------- |
| Self-Attention        | Encoder | 같은 시퀀스 내에서 모든 토큰이 서로를 양방향으로 참조        |
| Masked Self-Attention | Decoder | 같은 시퀀스 내에서 현재와 과거 토큰만 참조 (미래 차단)      |
| Cross-Attention       | Decoder | Decoder가 Encoder의 출력을 참조 (두 시퀀스 간 연결) |

![[028_transformer_trend.png]]