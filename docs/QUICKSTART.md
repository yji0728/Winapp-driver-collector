# Quick Start Guide - WinAppDriver Automation Framework

이 가이드는 WinAppDriver Automation Framework를 빠르게 시작하는 방법을 설명합니다.

This guide explains how to quickly get started with the WinAppDriver Automation Framework.

## 1. 설치 및 설정 (Installation & Setup)

### Step 1: WinAppDriver 설치 (Install WinAppDriver)

1. [WinAppDriver 릴리스 페이지](https://github.com/microsoft/WinAppDriver/releases)에서 최신 버전 다운로드
2. 다운로드한 MSI 파일 실행하여 설치
3. 설치 후 `C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe` 경로에 설치됨

### Step 2: Developer Mode 활성화 (Enable Developer Mode)

1. Windows Settings 열기 (Win + I)
2. Update & Security → For developers 이동
3. "Developer Mode" 선택

### Step 3: Python 의존성 설치 (Install Python Dependencies)

```bash
cd Winapp-driver-collector
pip install -r requirements.txt
```

## 2. WinAppDriver 실행 (Running WinAppDriver)

### 방법 1: 직접 실행 (Direct Execution)
```bash
"C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe"
```

### 방법 2: 관리자 권한으로 실행 (Run as Administrator)
일부 애플리케이션은 관리자 권한이 필요할 수 있습니다.

실행 후 다음과 같은 메시지가 표시됩니다:
```
Windows Application Driver listening for requests at: http://127.0.0.1:4723/
Press ENTER to exit.
```

## 3. 첫 번째 스크립트 실행 (Running Your First Script)

### CLI로 Calculator 테스트 실행 (Run Calculator Test via CLI)

```bash
python src/cli/main.py run --script examples/calculator_test.yaml
```

출력 예시:
```
Loading script: examples/calculator_test.yaml
Connecting to WinAppDriver at: http://127.0.0.1:4723
Executing script...

============================================================
Script: Calculator Test - Basic Operations
Status: SUCCESS
Duration: 12.34s
Steps: 15 total
  - Success: 15
  - Failed: 0
============================================================
```

### GUI로 실행 (Run via GUI)

```bash
python src/gui/main.py
```

GUI에서:
1. "Execute Script" 탭 선택
2. "Browse..." 버튼 클릭하여 `examples/calculator_test.yaml` 선택
3. "▶ Run Script" 버튼 클릭
4. 실행 과정을 로그에서 확인
5. "Results" 탭에서 결과 확인

## 4. 자신만의 스크립트 작성 (Writing Your Own Script)

### Step 1: UI 요소 탐색 (Exploring UI Elements)

Windows Inspect.exe 도구 사용:
```bash
# Inspect.exe는 Windows SDK에 포함되어 있습니다
# 일반적으로 다음 경로에 있습니다:
"C:\Program Files (x86)\Windows Kits\10\bin\<version>\x64\inspect.exe"
```

또는 CLI 인스펙터 모드 사용:
```bash
python src/cli/main.py inspect --app-path "C:\Windows\System32\calc.exe"
```

### Step 2: 스크립트 템플릿 (Script Template)

`my_test.yaml` 파일 생성:

```yaml
name: "My First Test"
description: "Description of what this test does"
app:
  path: "C:\\Path\\To\\Your\\App.exe"
  arguments: ""  # Optional command line arguments

steps:
  # Wait for app to load
  - action: "wait"
    duration: 2
  
  # Click a button
  - action: "click"
    element:
      type: "Name"  # or AutomationId, ClassName, XPath
      value: "ButtonName"
  
  # Enter text
  - action: "send_keys"
    element:
      type: "AutomationId"
      value: "textBox1"
    keys: "Hello World"
  
  # Take screenshot
  - action: "screenshot"
    filename: "my_screenshot.png"
```

### Step 3: 스크립트 실행 (Run Your Script)

```bash
python src/cli/main.py run --script my_test.yaml
```

## 5. 일반적인 문제 해결 (Common Troubleshooting)

### 문제: WinAppDriver에 연결할 수 없음
**해결책:**
- WinAppDriver.exe가 실행 중인지 확인
- 방화벽이 4723 포트를 차단하지 않는지 확인
- `--server-url` 옵션으로 다른 URL 시도

### 문제: 요소를 찾을 수 없음
**해결책:**
- Inspect.exe로 올바른 속성 사용 확인
- `implicit_wait` 시간 증가
- 명시적 `wait` 단계 추가

### 문제: 애플리케이션이 시작되지 않음
**해결책:**
- 애플리케이션 경로가 정확한지 확인
- 애플리케이션 실행에 관리자 권한이 필요한지 확인
- WinAppDriver를 관리자 권한으로 실행

### 문제: Appium 모듈을 찾을 수 없음
**해결책:**
```bash
pip install Appium-Python-Client selenium
```

## 6. 다음 단계 (Next Steps)

### 더 복잡한 시나리오
- [예제 스크립트](../examples/) 폴더의 다양한 예제 확인
- [상세 스펙 문서](SPECIFICATIONS.md)에서 모든 기능 학습

### GUI 활용
- Script Editor에서 시각적으로 스크립트 편집
- 실시간 실행 모니터링
- 결과 대시보드 활용

### CI/CD 통합
```yaml
# GitHub Actions 예제
- name: Run WinAppDriver Tests
  run: |
    Start-Process "C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe"
    python src/cli/main.py batch --scripts-dir tests/
```

### 배치 실행
여러 테스트를 한 번에 실행:
```bash
python src/cli/main.py batch --scripts-dir examples --output-dir results
```

## 7. 유용한 팁 (Useful Tips)

### 디버깅 (Debugging)
- `--log-level DEBUG` 옵션으로 상세 로그 확인
- 각 단계 후 `screenshot` 액션 추가
- `wait` 액션으로 실행 속도 조절

### 성능 최적화 (Performance Optimization)
- 불필요한 `wait` 시간 최소화
- `implicit_wait` 설정을 적절히 조정
- 요소 선택자를 효율적으로 사용

### 스크립트 재사용 (Script Reusability)
- 공통 설정은 `config/default.yaml`에 저장
- 반복되는 작업은 별도 스크립트로 분리
- 변수와 매개변수화 활용

## 8. 추가 리소스 (Additional Resources)

- **공식 문서**: [WinAppDriver GitHub](https://github.com/microsoft/WinAppDriver)
- **커뮤니티**: [Stack Overflow - winappdriver 태그](https://stackoverflow.com/questions/tagged/winappdriver)
- **예제**: [WinAppDriver Samples](https://github.com/microsoft/WinAppDriver/tree/master/Samples)

## 질문이 있으신가요? (Questions?)

GitHub Issues를 통해 질문하거나 버그를 보고해주세요!

---

Happy Automating! 🚀
