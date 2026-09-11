
## Spring AI 이해

기업에서는 Spring 기반 서비스가 잘 돌아가고 있음, Spring AI를 기존 애필리케이션에 자연스럽게 확장 가능

1. 기존 스프링 비즈니스 애플리케이션을 그대로 AI로 확장
2. 엔터프라이즈 기능을 AI Application에도 그대로 적용
3. 기존 도메인/데이터/서비스를 AI Agenet와 쉽게 결합

### 기존 스프링 개발자가 LLM 도입 시 겪는 문제

| 문제       | 설명                                          |
| -------- | ------------------------------------------- |
| API 파편화  | 모델마다 API·인증·요청/응답 방식이 다름                    |
| 모델 종속성   | 모델 변경 시 애플리케이션 코드 수정 필요                     |
| 반복 구현    | Prompt·Streaming·Structured Output 등을 직접 구현 |
| AI 패턴 부재 | RAG·Memory·Tool Calling을 개별 설계·구현           |
| 통합 복잡성   | 기존 Spring 서비스·데이터를 AI와 연결하는 코드 증가           |
| 운영 복잡성   | AI 호출의 Metric·Tracing·Token 사용량 등을 별도 구성    |
### 스프링 AI의 목적

- Spring 애플리케이션에서 LLM, Embedding Model, Vector Database, RAG, Tool Calling, MCP 등의 생성형 AI 기능을 일관된 Spring 방식으로 사용할 수 있도록 제공하는 AI 애플리케이션 프레임워크
- Spring Data가 JPA/MongoDB/Redis를 Repository 인터페이스로 추상화했듯, 
  Spring AI는 OpenAI/Anthropic/Gemini 등을 `ChatModel` 인터페이스로 추상화

### 스프링 AI의 핵심 설계 철학

![[000_spring-ai-integration-diagram-3.svg]]

> 기업 DATA, 기업 API를 AI 모델에 연결하는 것.

### 스프링 AI의 특징

| 특징                 | 의미                                   |
| ------------------ | ------------------------------------ |
| AI Model 추상화       | 다양한 LLM/Embedding Model을 일관된 API로 사용 |
| Spring IoC/DI      | AI 구성 요소를 Bean으로 관리하고 DI             |
| Auto Configuration | Spring Boot 기반 자동 설정                 |
| ChatClient         | Fluent API를 통한 편리한 LLM 호출            |
| Advisor            | Memory, RAG 등 AI 요청 처리 기능 확장         |
| RAG                | Document, Embedding, VectorStore 추상화 |
| Tool Calling       | Java Method와 LLM을 연결하여 Action 수행     |
| MCP                | 외부 Tool/Resource 생태계와 연동             |
| Spring 생태계 통합      | MVC/WebFlux, Security, Data 등과 결합    |
| Enterprise 친화성     | 기존 Spring 업무 시스템에 AI 기능을 자연스럽게 통합    |
- 생성은 AI Chat Model(OpenAI, Anthropic)이 생성하고 나(Spring 개발자)는 Chat Model만 알고 사용. 이는 우리가 소스코드 내부에서 new를 하지 않아서, 프레임워크랑 의존성이 사라짐.
### 스프링 AI 주요 기능

| 모듈 영역             | 역할                                                     |
| ----------------- | ------------------------------------------------------ |
| Models            | ChatModel, EmbeddingModel, ImageModel 등 모델 추상화         |
| Prompts           | Prompt, Message㏖System/User/Assistant㏗, PromptTemplate |
| Structured Output | BeanOutputConverter 등 응답을 Java 객체로 변환                  |
| RAG               | DocumentReader, Splitter, VectorStore, Advisor         |
| Tool Calling      | @Tool, ToolCallback, MethodToolCallbackProvider        |
| MCP               | MCP Client/Server 통합                                   |
| Observability     | Micrometer 기반 트레이싱/메트릭                                 |

## ChatClient API

### ChatModel

- 다양한 LLM과의 요청, 응답 방식을 일관된 방식으로 사용할 수 있도록 추상화한 인터페이스

![[001_chat-model-conversions.png]]

### ChatClient

- ChatModel 위에서 프롬프트, 어드바이저, 툴, 응답 처리를 편리하게 조합할 수 있도록 추상화한 API
- 모델 호출을 직접 다루기보다 프롬프트 구성 -> 옵션 설정 -> Advisor/Tool/Memory 적용 -> 호출 -> 결과 파싱 흐름으로 연결

![[002_chat-client.png]]

```Java
@RestController
class MyController {

    private final ChatClient chatClient;

    public MyController(ChatClient.Builder chatClientBuilder) {
        this.chatClient = chatClientBuilder.build();
    }

    @GetMapping("/ai")
    String generation(String userInput) {
        return this.chatClient.prompt()
            .user(userInput)
            .call()
            .content();
    }
}
```

### ChatOption

- LLM 종류와 상관없이 LLM과 대화할 때 사용할 수 있는 공통 옵션들을 정의

#### 속성

| 구문            | 타입            | 설명                           | 비고               |
| ------------- | ------------- | ---------------------------- | ---------------- |
| model         | String        | 호출할 AI 모델 식별자                | e.g. gpt-4o-mini |
| temperature   | Double        | 토큰 선택의 무작위성 조절               | 낮을수록 일관성 높음      |
| maxTokens     | Integer       | 모델이 생성할 최대 토큰 수              | 출력 길이 제한         |
| topP          | Double        | 누적 확률 기반 Sampling 범위         | e.g. 0.9         |
| topK          | Integer       | 확률 상위 K개 토큰을 Sampling 후보로 제한 | 모델에 따라 미지원       |
| stopSequences | List\<String> | 특정 문자열 생성 시 응답 생성을 중단        | 모델에 따라 동작 차이     |

#### Temperature

- LLM이 다음 토큰을 선택할 때 확률 분포를 얼마나 보수적으로 또는 다양하게 사용할 지를 조절하는 값
- 0에 가까울 수록 일관된 응답 1에 가까울 수록 창의성 및 다양성 답변 1.5는 무작위성이 매우 증가

#### TopK, TopP

- Top-K (Top-K Sampling)
	- 확률이 높은 상위 K개의 토큰만 후보로 남겨 그 안에서 다음 토큰을 선택
- Top-P (Nucleus Sampling)
	- 확률이 높은 토큰부터 누적하여 지정한 확률 P에 도달하는 최수 후보 집합에서 다음 토큰을 선택


### Prompt

- Context
- Instruction
- Input Data
- Output Indicator

```
### 1. Context (배경 및 역할) 
- 당신은 Kubernetes 기반 Spring Boot 3.x MSA 환경을 운영하는 시니어 백엔드 SRE 엔지니어입니다.
- 현재 무중단 배포(Rolling Update) 중 특정 파드에서 메모리 누수 의심 장애가 발생했습니다. 
  
### 2. Instruction (작업 지시 및 추론 규칙)
1. 주어진 Input Data(로그/메트릭)를 분석하여 장애의 근본 원인을 단계별(Step-by-step)로 추론하세요.
2. 해결을 위한 Spring Boot 설정 변경점 또는 K8s 매니페스트 수정 가이드를 1개 이상 도출하세요.
3. [주의] 제공된 근거 자료에 없는 내용은 절대 추측하여 지어내지 말고 "근거 부족"으로 명시하세요.

### 3. Input Data (분석 대상) [RAG 검색 지식 베이스]
- JVM MaxDirectMemorySize 기본값 및 Netty 메모리 누수 가이드 문서 발췌본 [시스템 로그 / 메트릭]
- 2026-08-16T10:50:00.123Z [ERROR]io.netty.util.internal.OutOfDirectMemoryError: failed to allocate 16777216 byte(s) of direct memory 

### 4. Output Indicator (출력 규격)
반드시 부가적인 인사말 없이 아래 JSON 스키마 규격으로만 응답하세요:
{ "root_cause": "장애 근본 원인 분석 요약", "reasoning_steps": ["추론 1단계", "추론 2단계", "추론 3단계"], "recommended_action": "권장 해결 방안 (코드/설정)", "confidence_score": 0.95 }
```

## Structured Prompt

- LLM 대형 언어 모델은 기본적으로 자유 형식의 텍스트 Unstructured Text를 생성하도록 설계
- 기업의 애플리케이션은 구조화된 출력 (JSON, XML, Java 객체 등) 처럼 정해진 스키마(규격)을 필요로 함

#### StructuredOutputConverter

- LLM에게 원하는 출력 형식을 지시하고, 생성된 문자열 응답을 원하는 JAVA 타입으로 변환하는 인터페이스

![[003_structured_output.png]]

## Advisor

- ChatClient의 요청과 응답 처리 과정에 개입하여 Prompt를 가공하거나 부가 기능을 적용하는 Interceptor 형태의 컴포넌트
- 모듈화
	- RAG, Chat Memory 등 반복적인 AI 패턴을 재사용 가능한 컴포넌트로 캡슐화
- 데이터 변환
	- LLM으로 보내는 요청과 오는 응답을 동적으로 수정하거나 보강할 수 있음
- 이식성
	- 특정 로직을 Advisor로 분리하여 여러 AI 모델이나 다양한 유스케이스에 쉽게 적용

## Embedding

- 텍스트, 이미지, 음성 등의 데이터가 가진 의미적 특징을 수치 벡터로 표현
- 의미가 유사한 데이터가 벡터 공간에서 유사한 방향/위치에 표현

### Vector DB

- 고차원 임베딩 벡터를 저장, 인덱싱 및 검색하기 위해 최적화된 데이터베이스
- 의미 및 맥락의 유사성 기반 유사도 검색
- 기존 DB는 정확한 일치를 찾지만, 벡터DB는 쿼리 벡터와 유사한 벡터들을 반환

#### 종류

| 제품       | 유형              | 특징                | 장점            | 적합한 경우                 | 엔터프라이즈 사용 |
| -------- | --------------- | ----------------- | ------------- | ---------------------- | --------- |
| pgVector | PostgreSQL 확장   | 기존 RDB에 벡터 타입 추가  | SQL 그대로 사용    | 엔터프라이즈급 데이터 안정성과 복구 체계 | 매우 높음     |
| Qdrant   | 전용 벡터 DB        | Rust 기반, HNSW 최적화 | 빠른 검색, 필터링 강함 | 대규모 RAG, SaaS          | 매우 높음     |
| Chroma   | 경량 Vector Store | Python 친화적        | 개발 간편         | PoC, 로컬 개발             | 제한적       |
| Mlvus    | 대규모 분산형         | 고성능 ANN, GPU 지원   | 초대규모 처리       | AI 플랫폼                 | 높음        |
| Weavlate | Graph + Vector  | 하이브리드 검색 강점       | 메타데이터 + 벡터 통합 | 지식 그래프 결합              | 증가 중      |
| Pinecone | Saas            | 완전 관리형            | 운영 부담 없음      | 클라우드 기반 서비스            | 매우 많음     |

[[Day 2 - Spring AI]] 이어서 계속