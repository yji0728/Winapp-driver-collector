# WinAppDriver Automation Framework Specifications

## 개요 (Overview)

이 프레임워크는 Microsoft WinAppDriver를 활용한 Windows 애플리케이션 자동화 도구입니다.
GUI 및 CLI 두 가지 인터페이스를 제공하여 다양한 사용자 요구사항을 충족합니다.

This framework is a Windows application automation tool utilizing Microsoft WinAppDriver.
It provides both GUI and CLI interfaces to meet various user requirements.

## 주요 기능 (Key Features)

### 1. 핵심 자동화 기능 (Core Automation Features)
- **요소 탐색 (Element Discovery)**: UI 요소 자동 탐색 및 식별
- **액션 수행 (Action Execution)**: 클릭, 입력, 드래그 등 다양한 액션
- **검증 (Validation)**: 요소 상태 및 속성 검증
- **대기 및 동기화 (Wait & Synchronization)**: 명시적/암묵적 대기 지원
- **스크린샷 (Screenshot)**: 자동 스크린샷 캡처

### 2. CLI 기능 (CLI Features)
- **스크립트 실행**: 명령줄에서 자동화 스크립트 실행
- **배치 처리**: 여러 테스트 시나리오 순차 실행
- **결과 출력**: 상세한 실행 결과 로그
- **CI/CD 통합**: Jenkins, GitHub Actions 등과 통합 가능

### 3. GUI 기능 (GUI Features)
- **시각적 스크립트 편집기**: 드래그 앤 드롭으로 스크립트 작성
- **실시간 실행 모니터링**: 실행 중 상태 실시간 확인
- **요소 인스펙터**: UI 요소 탐색 및 속성 확인 도구
- **결과 대시보드**: 실행 결과 시각화

## 아키텍처 (Architecture)

### 구성 요소 (Components)

```
┌─────────────────────────────────────────┐
│           User Interface Layer          │
│  ┌──────────────┐    ┌──────────────┐  │
│  │   CLI Tool   │    │   GUI Tool   │  │
│  └──────────────┘    └──────────────┘  │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│         Core Automation Layer           │
│  ┌──────────────────────────────────┐  │
│  │   WinAppDriver Controller        │  │
│  │   - Session Manager              │  │
│  │   - Element Finder               │  │
│  │   - Action Executor              │  │
│  │   - Validator                    │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│       WinAppDriver (External)           │
│     Windows Application Under Test      │
└─────────────────────────────────────────┘
```

## 기술 스택 (Technology Stack)

- **Language**: Python 3.8+
- **WinAppDriver Client**: Appium-Python-Client
- **GUI Framework**: Tkinter (표준 라이브러리)
- **CLI Framework**: Click
- **Configuration**: YAML
- **Logging**: Python logging module
- **Testing**: pytest (선택적)

## 사용 사례 (Use Cases)

### CLI 사용 예제 (CLI Usage Example)

```bash
# 단일 스크립트 실행
python src/cli/main.py run --script examples/calculator_test.yaml

# 여러 스크립트 실행
python src/cli/main.py run --script examples/*.yaml

# 설정 파일 사용
python src/cli/main.py run --script test.yaml --config config/default.yaml

# 요소 탐색 모드
python src/cli/main.py inspect --app-path "C:\\Windows\\System32\\calc.exe"
```

### GUI 사용 예제 (GUI Usage Example)

```bash
# GUI 실행
python src/gui/main.py

# GUI에서:
# 1. 애플리케이션 경로 설정
# 2. 스크립트 작성 또는 불러오기
# 3. 실행 버튼 클릭
# 4. 결과 확인
```

## 스크립트 형식 (Script Format)

YAML 형식의 테스트 시나리오:

```yaml
name: "Calculator Test"
description: "Basic calculator operations"
app:
  path: "C:\\Windows\\System32\\calc.exe"
  arguments: ""

steps:
  - action: "wait"
    duration: 2
    
  - action: "click"
    element:
      type: "Name"
      value: "One"
    
  - action: "click"
    element:
      type: "Name"
      value: "Plus"
    
  - action: "click"
    element:
      type: "Name"
      value: "Two"
    
  - action: "click"
    element:
      type: "Name"
      value: "Equals"
    
  - action: "verify"
    element:
      type: "AutomationId"
      value: "CalculatorResults"
    expected: "3"
    
  - action: "screenshot"
    filename: "result.png"
```

## API 레퍼런스 (API Reference)

### Core Classes

#### WinAppDriverController
```python
class WinAppDriverController:
    def __init__(self, server_url="http://127.0.0.1:4723"):
        """WinAppDriver 서버에 연결"""
        
    def start_app(self, app_path, app_arguments=""):
        """애플리케이션 시작"""
        
    def stop_app(self):
        """애플리케이션 종료"""
        
    def find_element(self, by, value):
        """요소 찾기"""
        
    def click(self, element):
        """요소 클릭"""
        
    def send_keys(self, element, keys):
        """텍스트 입력"""
        
    def get_text(self, element):
        """요소의 텍스트 가져오기"""
        
    def screenshot(self, filename):
        """스크린샷 저장"""
```

### 지원되는 액션 (Supported Actions)

- `click`: 요소 클릭
- `double_click`: 요소 더블 클릭
- `right_click`: 요소 우클릭
- `send_keys`: 텍스트 입력
- `clear`: 입력 필드 지우기
- `verify`: 요소 검증
- `wait`: 대기
- `screenshot`: 스크린샷
- `scroll`: 스크롤
- `drag`: 드래그 앤 드롭

### 요소 선택자 (Element Selectors)

- `Name`: 요소 이름
- `AutomationId`: 자동화 ID
- `ClassName`: 클래스 이름
- `XPath`: XPath 표현식
- `AccessibilityId`: 접근성 ID

## 설치 및 설정 (Installation & Setup)

### 사전 요구사항 (Prerequisites)

1. Windows 10 or later
2. Python 3.8 or later
3. WinAppDriver installed and running
4. Developer Mode enabled in Windows

### 설치 단계 (Installation Steps)

```bash
# 1. 저장소 클론
git clone https://github.com/yji0728/Winapp-driver-collector.git
cd Winapp-driver-collector

# 2. 의존성 설치
pip install -r requirements.txt

# 3. WinAppDriver 다운로드 및 실행
# https://github.com/microsoft/WinAppDriver/releases
# WinAppDriver.exe 실행

# 4. 테스트 실행
python src/cli/main.py run --script examples/calculator_test.yaml
```

## 설정 파일 (Configuration File)

`config/default.yaml`:

```yaml
winappdriver:
  server_url: "http://127.0.0.1:4723"
  implicit_wait: 10
  connection_timeout: 30

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "logs/automation.log"

screenshots:
  enabled: true
  on_error: true
  directory: "screenshots"

reporting:
  format: "html"
  directory: "reports"
```

## 확장성 (Extensibility)

프레임워크는 다음과 같은 방식으로 확장 가능합니다:

1. **커스텀 액션**: 새로운 액션 클래스 추가
2. **커스텀 검증**: 검증 로직 확장
3. **플러그인**: 플러그인 시스템을 통한 기능 추가
4. **리포터**: 다양한 형식의 리포트 생성

## 제한사항 (Limitations)

1. Windows 플랫폼에서만 동작
2. WinAppDriver가 지원하는 애플리케이션만 자동화 가능
3. 일부 네이티브 Win32 컨트롤은 제한적 지원

## 라이선스 (License)

이 프로젝트는 오픈소스이며, 적절한 라이선스 하에 배포됩니다.

## 기여 (Contributing)

버그 리포트, 기능 제안, 풀 리퀘스트를 환영합니다.

## 참고 자료 (References)

- [WinAppDriver GitHub](https://github.com/microsoft/WinAppDriver)
- [Appium Python Client](https://github.com/appium/python-client)
- [Windows UI Automation](https://docs.microsoft.com/en-us/windows/win32/winauto/entry-uiauto-win32)
