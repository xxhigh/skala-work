---
aliases:
  - SpringAI
tags:
  - SpringAI
  - Skala
---
[[Day 1 - Spring AI]] 이어서 계속

### VectorStore Interface

- 다양한 벡터 저장소를 일관된 방식으로 사용할 수 있도록 VectorStore 인터페이스 제공
- VectorStore 구현체는 SpringBoot Auto-Configuration으로 Bean 자동 생성

```java
public interface VectorStore extends DocumentWriter, VectorStoreRetriever { 
	default String getName() {…} 
	void add(List documents);
	void delete(List idList);
	void delete(Filter.Expression filterExpression);
	List similaritySearch(String query);
	List similaritySearch(SearchRequest request);
}

--application.yaml
vectorstore:
  pgvector:
      initialize-schema: true
```

### Document Class

- 비정형/정형 데이터를 수집, 가공하여 VectorStore에 저장하고 검색할 때, \[본문 텍스트 + 메타데이터 + 임베딩 벡터]를 하나로 묶어 다루는 Spring AI의 표준 데이터 객체(DTO)
- https://docs.spring.io/spring-ai/docs/current/api/org/springframework/ai/document/Document.html

## RAG

- 대규모 언어모델은 훌륭하지만, 최신 정보나 기업의 비공개 내부 데이터에 대해서는 알지 못함.
- Vector DB로부터 검색(Retrieval)해서 사용자 질문을 보강(Augment)하고 LLM을 통해 답을 생성(Generation)

### 파이프라인

![[004_rag.png]]

- 문서를 임베딩후 벡터DB에 저장
- 사용자 질문과 의미적으로 유사한 문서를 검색 LLM의 컨텍스트에 포함시켜 답변을 생성
- ETL 과정이 중요함. 어떤 기준으로 청크를 나누고 임베딩 할 것인지!

RAG는 크게 보면 2개의 파이프라인으로 나누는데, Offline(ETL)과 Runtime(RAG)이다.
Offline에서는 데이터를 구성하는 역할을 하고 Runtime에서는 구성된 데이터를 가지고 프롬프트를 보강하는 역할을 한다.

### ETL Offline

- Extract Transform Load
- 외부 데이터 소스에서 관련 정보를 검색해서 이를 컨텍스트로 LLM 프롬프트에 추가하는 기술

1. DocumentReader
	- 원시 데이터를 객체로 추출 (Extract)
2. DocumentTransformer
	- 추출된 데이터를 AI모델에 최적화된 형태로 변환(Transform)
3. DocumentWriter
	- 변환된 데이터를 VectorStore와 같은 목적지에 적재(Load)

### RAG Runtime

- 사용자 질문과 관련된 외부 지식을 VectorStore에서 찾은 뒤, 그 정보를 프롬프트에 덧붙여 LLM이 답변하도록 만드는 패턴

#### 구현체

- SpringAI가 기본 제공하는 RAG Advisor
- QuestionAnswerAdvisor(기본)
	- VectorStore 기반 RAG 빠르게 구현
	- 단순 Q&A, Rapid Prototyping
	- VectorStore + SearchRequest 간단 결합
- RetrievalAugmentationAdvisors
#### RetrievalAugmentationAdvisors

1. Pre-Retrieval: 사전검색, 사용자 쿼리를 변환하여 검색 품질을 극대화
2. Retrieval: VectorStore에서 문서를 가져옴
3. Post-Retrieval: 사후검색, 검색된 문서를 재정렬하거나 필터링하여 노이즈 감소
4. Generation: 검색 결과를 프롬프트에 증강하고 LLM 호출하여 답변 생성

사용하기 위해서는 `spring-ai-rag` 의존성 주입 필요

### ChatMemory

- 저장, 관리, 재구성하여 지속적인 대화 맥락을 유지해 주는 메모리 관리 컴포넌트
- 대화 저장 및 조회
- 토큰/메시지 수 제한
- 영속화 지원

## Tool Calling

- AI 모델이 외부 시스템의 기능을 호출해서 자신의 능력을 확장하기 위한 기술

### 동작 흐름

![[005_tool.png]]

### Tool 정의

@Tool 어노테이션:
- name
- description

@ToolParam 어노테이션:
- description
- required

```java
@Tool(description = "도시 이름으로 현재 날씨를 조회합니다. 예: Seoul")

public String getCurrentWeather(

@ToolParam(description = "도시 이름 (예: Seoul)", required = true) String city) {
```

## MCP

- 자연어로 동작하는 AI와 API, DB, 업무 시스템처럼 구조화된 인터페이스로 동작하는 시스템 사이를 연결하는 표준 중간 계층

### MCP Client

MCP Client의 역할 
- tool/list 요청으로 사용 가능한 도구 목록을 로딩 
- tool/call 요청으로 특정 도구 실행
- LLM이 필요할 때 MCP Server의 도구 호출을 자동 오케스트레이션
- SSE/STDIO/Streamable HTTP 같은 전송 방식 제공

### MCP Server

