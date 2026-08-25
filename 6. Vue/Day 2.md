---
tags:
  - Vue
  - Skala
aliases:
  - SKALA_VUE
---
[[6. Vue/Day 1]] 이어서 작성.

## v-on
- DOM 요소에 이벤트 리스너를 연결하여 이벤트를 감지하고 처리
```html
<!-- 축약형 없이 사용-->
<button v-on:click="doSomething">클릭</button>

<!-- 축약형 (@) 사용-->
<button @click="doSomething">클릭</button>
```
- Inline Handler
- Method Handler
	- 함수 참조 전달 방식
	- 내부적으로 `button.addEventListener('click', handleClick)` 와 같이 처리

### 주요 이벤트 목록(Event)

| 이벤트이름      | 설명                 |
| ---------- | ------------------ |
| click      | 클릭 이벤트             |
| submit     | 폼 제출 이벤트           |
| keyup      | 키보드 키를 뗐을 때        |
| keydown    | 키보드를 눌렀을 때         |
| input      | 입력 필드 변경 시         |
| change     | 입력 값 변경 후 포커스 아웃 시 |
| mouseenter | 마우스가 요소 위로 올라올 때   |
| mouseleave | 마우스가 요소에서 벗어날 때    |
### 이벤트 오브젝트(Event Object)
- 브라우저가 넘겨주는 객체
#### 프로퍼티

| 분류  | 속성명                   | 데이터 타입      | 설명 및 활용처                                                                        |
| --- | --------------------- | ----------- | ------------------------------------------------------------------------------- |
| 공통  | e.target              | HTMLElement | **이벤트를 발생시킨 HTML 태그** e.target.value (입력값), e.target.tageName (BUTTON, INPUT..) |
|     | e.currentTarget       | HTMLElement | **이벤트 리스너가 걸려있는 HTML 태그 **(부모 태그에 이벤트를 걸었을 때 e.target과 달라짐)                     |
|     | e.type                | String      | **발생한 이벤트의 종류** (예: click, keyup, submit 등)                                     |
|     | e.timeStamp           | Number      | 웹페이지가 로드된 후 이벤트를 실행하기까지 걸린 시간(ms)                                               |
| 마우스 | e.clientX / e.clientY | Number      | 브라우저 화면(Viewport) 기준 마우스 커서의 X, Y 좌표                                            |
|     | e.pageX / e.pageY     | Number      | 전체 HTML 문서(Document) 기준 마우스 커서의 X, Y 좌표                                         |
|     | e.screenX / e.screenY | Number      | 사용자의 모니터 모니터 화면 기준 마우스 커서의 X, Y 좌표                                              |
|     | e.button              | Number      | 클릭한 마우스 버튼 번호 (0: 왼쪽, 1: 휠/가운데, 2: 오른쪽)                                         |
| 키보드 | e.key                 | String      | 사용자가 누른 키의 실제 문자 값 (예: Enter, ArrowUp, a, A, Escape)                            |
|     | e.code                | String      | 사용자가 누른 물리적인 키보드 자판의 위치 값 (예: Enter, KeyA, Digit1, Escape)                      |
|     | e.shiftKey            | Boolean     | 이벤트를 유발할 때 Shift 키를 같이 누르고 있었는지 여부 (true/false)                                 |
|     | e.ctrlKey / e.altKey  | Boolean     | 이벤트를 유발할 때 **Ctrl** 또는 **Alt** 키를 같이 누르고 있었는지 여부                                |
#### 메소드
| Method                       | 주요 역할 및 기능                                        | 실무 핵심 활용처 (예시)                                                                          |
| ---------------------------- | ------------------------------------------------- | --------------------------------------------------------------------------------------- |
| e.preventDefault()           | 브라우저가 특정 태그에 대해 가지는 기본 고유 동작을 강제로 중단시킨다.          | * `<a>`태그를 눌렀을 때 페이지가 링크로 이동하는 것을 방지<br>* `<form>`의 submit 버튼을 눌렀을 때 페이지가 새로 고침되는 것을 방지 |
| e.stopPropagation()          | 이벤트가 부모 태그로 타고 올라가는 이벤트 버블링(Bubbling)을 완전히 차단한다.  | * 팝업창(자식) 내부를 클릭했을 때, 팝업창 뒤편의 배경(부모) 닫기 이벤트까지 동시에 실행되는 버블 버그 방지                         |
| e.stopImmediatePropagation() | 현재 태그에 걸려있는 다른 이벤트 리스너들의 실행까지 전부 중단시키고, 버블링도 막는다. | * 하나의 버튼에 여러 개의 클릭 함수가 중복으로 엮여 있을 때, 첫 번째 함수만 실행하고 뒤는 싹 다 마비시키고 싶을 때                    |
- Vue에서 이벤트 오브젝트를 받는 2가지 방법
	- @click="handleEvent" -> const handleEvent = (e) => { ... }
	- @click="handleEvent('홍길동', `$event`)"

### 이벤트 수식어(Event Modifier)
- 이벤트 리스너의 기본 동작을 보완하거나 제어하는데 사용되는 특수 접미어

```text
v-on:submit.prvent="onSubmit"
(name):(argument).(modifier)="(value)"
```

| 타입  | 수식어            | 실제 동작/기능                     | 실무 활용 예시                                         |
| --- | -------------- | ---------------------------- | ------------------------------------------------ |
| 공통  | .prevent       | e.preventDefault()           | Form 제출 시 페이지 새로고침 방지, 링크 이동 방지                  |
|     | .stop          | e.stopPropagation()          | 자식 버튼 클릭 시 부모 박스로 이벤트가 퍼지는 버블링 차단                |
|     | .once          | 이벤트 리스너 실행 후 자동 제거           | 좋아요 버튼 중복 클릭 방지, 설문조사 단 1회 제출                    |
|     | .self          | e.target === e.currentTarget | 회색 배경막(Dim)을 직접 클릭했을 때만 팝업창 닫기 구현                |
|     | .capture       | 캡처링 단계에서 이벤트 감지              | 버블링과 반대로 부모 이벤트가 자식보다 먼저 터지게 설정                  |
|     | .passive       | scroll 성능 최적화                | 모바일 화면에서 무거운 스크롤/터치 이벤트 부드럽게 처리                  |
| 키보드 | .enter         | Enter  키                     | 로그인, 댓글 입력 후 엔터 쳤을 때 즉시 전송                       |
|     | .tab           | Tab 키                        | 다음 입력 칸으로 포커스가 넘어갈 때 사전 유효성 검사                   |
|     | .delete        | Delete or Backspace 키        | 텍스트 칩(Tag)을 선택하고 지우기 키를 눌러 삭제할 때                 |
|     | .esc           | Escape 키                     | 팝업창이나 모달 열린 상태에서 Esc 누르면 창 닫기                    |
|     | .space         | Space 키                      | 체크박스 형태의 UI에서 스페이스바 누르면 토글 처리                    |
|     | .up / .down    | Arrow Up / Down 키            | 자동완성 검색어 목록에서 화살표로 리스트 이동할 때                     |
|     | .left / .right | Arrow Left / Right 키         | 이미지 슬라이더(캐러셀)에서 화살표 키로 사진 넘기기                    |
| 시스템 | .ctrl          | Ctrl 키                       | Ctrl + 클릭으로 링크를 새 탭에서 열 때 전용 로직 처리               |
|     | .alt           | Alt 키                        | 일반 클릭과 Alt + 클릭의 동작을 다르게 분기할 때                   |
|     | .shift         | Shift 키                      | Shift + Enter를 누르면 전송되지 않고 인풋창 줄바꿈 처리            |
|     | .meta          | 윈도우 키 / 커맨드 키                | OS 전용 시스템 단축키 조합을 웹앱에 이식할 때                      |
|     | .exact         | 오직 지정한 키만 눌렸을 때 지정           | @click.ctrl.exact: 다른 키 안 섞이고 쌩 Ctrl만 누르고 클릭해야 함 |
| 마우스 | .left          | 마우스 왼쪽 버튼(기본값)               | 일반적인 버튼 클릭 처리                                    |
|     | .right         | 마우스 오른쪽 버튼                   | 웹페이지 순정 메뉴 대신 개발자가 만든 '커스텀 우클릭 컨텍스트 메뉴'를 띄울 때    |
|     | .middle        | 마우스 휠(가운데 버튼)                | 마우스 휠 클릭으로 빠른 탭 닫기나 특수 스크롤 기능을 넣을 때              |
## v-model
- HTML의 입력 요소의 값과 JS 데이터(Ref)를 묶어, 한쪽이 바뀌면 다른 한쪽도 실시간으로 똑같이 바뀌게 만드는 양방향 바인딩 제공 장치

### Form 요소별 매핑 규칙
- 양방향 바인딩을 할 때는 HTML 요소의 특정 및 동작 방식과 일치하도록 ref 초기값을 선언해야 함

| Form 태그 종류                    | 연결된 ref 변수의 초기값 타입 | v-model이 변수에 담아주는 실제 값           |
| ----------------------------- | ------------------ | -------------------------------- |
| `textarea (장문 입력)`            | ref('') (문자열)      | 사용자가 입력한 장문의 줄바꿈 포함 텍스트          |
| `input[type="checkbox"]` (단일) | ref(false) (불리언)   | 체크하면 true, 해제하면 false            |
| `input[type="checkbox"]` (다중) | ref([]) **(배열)**   | 체크된 항목들의 value 속성 값이 배열에 차곡차곡 쌓임 |
| `input[type="radio"]` (단일 선택) | ref('') (문자열)      | 여러 라디오 중 사용자가 최종 선택한 하나의 value 값 |
| `select` (드롭다운)               | ref('') (문자열)      | 사용자가 선택한 `<option>`의 value 값     |

### v-model modifier
- `v-model modifier`는 입력 요소의 동작 방식이나 수집되는 데이터 형태를 손쉽게 제어할 수 있도록 Vue가 제공하는 편의 기능
- 체이닝 기능도 제공

| 수식어     | 기본 동작 이벤트            | 수식어 적용 후 동작                   | 주요 사용 목적                     |
| ------- | -------------------- | ----------------------------- | ---------------------------- |
| .lazy   | @input (타이핑할 때마다 반영) | @change (포커스를 잃거나 Enter 시 반영) | 불필요한 실시간 상태 업데이트 및 API 요청 방지 |
| .number | String 타입 수집         | Number 타입으로 자동 형변환            | 숫자 데이터 입력 시 자동 타입 변환 처리      |
| .trim   | 입력값 그대로 수집           | 양끝 공백(Whitespace) 제거 후 수집     | 공백 입력으로 인한 Validation 오류 예방  |

## Vue Style

### Scoped Style
- `<style scoped>` 로 작성된 스타일은 현재 컴포넌트 내부에 선언된 HTML 태그에만 적용되고, 다른 컴포넌트에는 영향을 주지 않음
### External Style
- 공통 CSS나, 외부 라이브러리 CSS를 사용하는 방법
- 프로젝트 전체에 적용할 공통 스타일은 src/main.js에 등록한다.
- 특정 컴포넌트에 외부 CSS파일을 적용할 때는 `<style>` 내부에서 자바스크립트의 @import 문법을 사용한다.
---
## Composition API
- Vue3에서 도입된 현대적인 JS 코딩 방식.
- 컴포넌트의 로직을 유연하고 깔끔하게 한 곳에서 조합하여 작성하는 방법을 제공.

### Overview
| 카테고리                | 주요함수                         |
| ------------------- | ---------------------------- |
| Application         | createApp                    |
| Reactive State      | ref, reactive                |
| Computed & Watchers | computed, watch, watchEffect |

**ref**
- 원시 타입이나 참조 자료형 모든 값을 반응형 상태로 만든다.
- `<script setup>` 에서는 .value로 접근하고, `<template>`에서는 .value 없이 사용
**reactive**
- 참조 자료형(객체, 배열, Map, Set)데이터를 반응형 상태로 만드는 함수
- `<script setup>` 에서는 .value없이 접근하고, `<template>`에서도 일반 객체처럼 사용
- 반응형 객체를 교체하거나, 구조를 분해해야 할당하면 반응성 연결이 끊어짐
```js
let state = reactive({ count: 0 })

// ❌ 통째로 새 객체를 갈아끼우면 반응성 연결이 끊어진다.
state = { count: 5 }

// 🟢 내부의 알맹이 속성만 조심스럽게 변경해야 한다.
state.count = 5
```

### Computed
- 의존하는 반응형 데이터가 변경될 때 자동으로 다시 계산된다.
- 계산된 값은 메모리에 캐싱되어 성능에 좋다.
- Computed Ref 객체가 반환

> **Vue Component 재렌더링 동작원리**
> 1. 반응형 변수가 변경되면, Vue 반응형 시스템은 해당 컴포넌트의 DOM을 다시 그려야 할 필요성(Re-rendering)을 감지함.
> 2. 템플릿을 다시 그릴 때는 `<template>` 내부의 모든 표현식과 메서드 호출을 처음부터 끝까지 다시 평가(Execute)한다.
> 3. 템플릿 안에 `괄호()`를 붙여 직접 호출한 일반 함수는, 컴포넌트가 다시 그려질 때마다 조건을 불문하고 무조건 다시 실행된다.

### Watch
- 반응형으로 선언된 데이터의 값이 변경되었을 때, 후속 로직(비동기 통신, 데이터 저장 등)을 수행하도록 Call 함수를 지정
- 콜백 함수의 인자는 "새로 변경된 값"과 "변경되기 전의 값"이 전달됨
#### Single Watch
```js
Import { watch } from‘vue’;

watch(반응형데이터, (newVal, oldVal) => { 실핼할 후속 로직 })
```
#### Multi Watch
- 반응형으로 선언된 여러 데이터를 한꺼번에 감시할 때 쓰는 기법
```js
Import { watch } from‘vue’;

watch([변수1, 변수2], ([새값1, 새값2], [옛값1, 옛값2]) => { 실핼할 후속 로직 })
```
#### Deep Watch
- ref()로 선언된 객체나 배열을 감시할 때 쓰는 기법
- 주소값만 추적하고, 내부 속성의 변경은 감지하지 않아서 값의 변화를 추적하려면 `{ deep:true }`를 명시 해야함
```js
Import { watch } from ‘vue’;

watch(반응형데이터, (newValue) => { 실행할 후속 로직 },{deep:true})
```
#### Array Watch
**기본형 배열의 특정 인덱스의 값 자체를 감시할 때**

- ref 함수로 생성된 반응형 데이터
```js
const members = ref(['Hong', 'Lee', 'Kang'])

watch(() => 배열.value[0], (새값, 이전값) => { ... })
```

- reactive 함수로 생성된 반응형 데이터
```js
const todoList = reactive(['프로젝트 기획', '퍼블리싱', 'Vue 개발'])

watch(() => 배열[0], (새값, 이전값) => { ... })
```

**ref 객체형 배열의 특정 객체 내부 속성을 감시할 때**

 - ref 함수로 생성된 반응형 데이터
```js
const cityWeather = ref([
	{ name: '서울', temp: 25 },
	{ name: '부산', temp: 23 }
])

watch(() => 배열.value[0], (새객체) => { ... }, { deep: true })
```

- reactive 함수로 생성된 반응형 데이터
```js
const cityWeather = reactive([
	{ name: '서울', temp: 25 },
	{ name: '부산', temp: 23 }
])

watch(() => 배열[0], (새객체) => { ... }, { deep: true })
```
#### WatchEffect
- 감시 대상을 명시하지 않아도 반응형 데이터를 자동으로 추적해서 값이 바뀔 때마다 재실행되는 함수
- 컴포넌트가 처음 생성될 때도 무조건 즉시 실행
- 이전 값은 제공하지 않음
- 함수 내부의 반응형 데이터만 자동으로 감시
```js
watchEffect(() => {
// Vue가 이 내부 코드를 읽고 'username'과 'age'를 자동으로 감시 리스트에 등록합니다.
logMessage.value = `[자동 감지] 이름: ${username.value} / 나이: ${age.value}세`

// 화면이 처음 켜질 때 1등으로 즉시 실행되는 증거를 콘솔에서 확인합니다.
console.log('🤖 watchEffect가 내부 변수 변경을 감지하여 실행되었습니다.')
})
```

[[Day 3]]에 이어서 계속...