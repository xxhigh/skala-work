---
aliases:
  - Container
tags:
  - Skala
  - Container
---
[[Day 1 - Container]] 이어서 계속
### ENTRYPOINT

```Dockerfile
FROM alpine:latest

ENTRYPOINT ["ping"]

CMD ["-c", "3", "skala-fileserver.skala-ai.com"]
```

- ENTRYPOINT가 있을 경우 CMD는 파라미터로 작동한다.
- 그러면 왜 이렇게 했나? -> 이미지를 수정해도 ENTRYPOINT는 무조건 실행하게 하고 싶어!
- --entrypoint 플래그를 통해 강제로 변경 가능하지만, 잘 사용하지 않음

rm: 그냥 삭제
--rm: 실행했다가 죽으면 삭제

### 읽기 전용 레이어를 만드는 명령어

**이미지 레이어 생성 명령**
- RUN: 패키지 설치, 소스코드 빌드, 스크립트 실행 등을 수행
- COPY: 호스트 머신의 파일이나 디렉토리를 이미지 내부 경로로 복사
- ADD: COPY와 유사하게 호스트 파일을 복사하며, 추가로 압축 파일 자동 해제 및 원격 URL 파일 다운로드를 수행

**컨테이너 실행 설정 명령**
`config.json` 이라는 파일이 만들어지고 내부에 아래 명령어가 작성된 것.
- ENTRYPOINT
- CMD
- ENV
- WORKDIR
- EXPOSE
- USER
- VOLUME
- LABEL

## 컨테이너 볼륨

### 컨테이너에 Persistent Volume 연결하기

- 컨테이너는 언제든 삭제될 수 있는 일회성 환경
- 컨테이너가 종료 후 재실행되더라도 기존 데이터를 유지하기 위한 방법 필요

### 볼륨 타입
- **Named Volume**: Docker를 포함한 컨테이너 런타입에서 관리하는 이름 있는 Volume
- **Bind Mount**: 외부 호스트 디렉토리와 컨테이너 내부 디렉토리를 마운트하는 방식
- **Anonymous Volume**: 이름없이 임시 생성 (Dockerfile 내부 VOLUME 명령어로 생성)
![[002_civo-docker-volume-types.svg]]
- Bind Mount를 많이 사용함. -> 개발자가 관리할 수 있기 때문에.

```Dockerfile
# Named Volume
docker run -it --name busybox -v demo:/usr/share busybox

# Bind mount
docker run -it --name busybox -v $(pwd):/usr/share busybox
```

### CMD 명령어 최적화

> **컨테이너 프로세스의 실행 방법**
> 1. 컨테이너가 즉시 종료되지 않고 멈춰 있다 강제 종료되는 문제
> 2. 트래픽을 받고 처리 중 Graceful shutdown 되지 않고 KILL 되는 현상
> 3. 이로인한 트래픽 유실 발생 및 배포 속도 저하
>  
> 이러한 문제는 CMD 한 줄 잘못 사용하는 경우 발생

| 표준 명칭           | 사용 방법                                               | 특징                                                    |
| --------------- | --------------------------------------------------- | ----------------------------------------------------- |
| Exec Form       | CMD \["python3", "webserver.py"]                    | 쉘 없이 앱이 직접 PID 1로 실행 (강력 권고)                          |
| Shell Form      | CMD \["/bin/sh", "-c", "python3 webserver.py"]      | /bin/sh가 PID 1로 실행<br>실행 앱은 자식 프로세스로 분기(비권고)          |
| Shell with Exec | CMD \["/bin/sh", "-c", "exec python3 webserver.py"] | 쉘 환경변수 등을 처리한 뒤 exec로 부모 쉘을 앱(PID 1)으로 치환<br>(조건부 권고) |

## 컨테이너 구조 이해

### Container Feature

- Namespace
- cgroups
- rootfs + OverlayFS
- Netfliter
- Linux Capabilities
- SELinux/AppArmor (보통 특수한 상황아니면 쓰지 않음)