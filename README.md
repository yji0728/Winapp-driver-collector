# WinAppDriver Automation Framework

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Microsoft WinAppDriver를 활용한 Windows 애플리케이션 자동화 프레임워크입니다. GUI와 CLI 두 가지 인터페이스를 제공합니다.

A comprehensive automation framework for Windows applications using Microsoft WinAppDriver. Provides both GUI and CLI interfaces.

## 🎯 주요 기능 (Key Features)

### Core Automation
- ✨ **UI 요소 자동 탐색**: 자동으로 UI 요소 식별 및 상호작용
- 🎬 **다양한 액션 지원**: 클릭, 입력, 드래그, 스크롤 등
- ✅ **검증 기능**: 요소 상태 및 속성 검증
- ⏱️ **스마트 대기**: 명시적/암묵적 대기 지원
- 📸 **자동 스크린샷**: 실행 과정 자동 캡처

### CLI Interface
- 🖥️ **명령줄 실행**: 터미널에서 스크립트 실행
- 📦 **배치 처리**: 여러 스크립트 순차 실행
- 🔍 **인스펙터 모드**: UI 요소 탐색 도구
- 🔄 **CI/CD 통합**: Jenkins, GitHub Actions 등과 통합

### GUI Interface
- 🎨 **시각적 편집기**: 드래그 앤 드롭 스크립트 작성
- 📊 **실시간 모니터링**: 실행 상태 실시간 확인
- 🔧 **요소 인스펙터**: UI 요소 속성 확인
- 📈 **결과 대시보드**: 실행 결과 시각화

## 📋 사전 요구사항 (Prerequisites)

1. **Windows 10 or later**
2. **Python 3.8 or later**
3. **WinAppDriver** - [다운로드](https://github.com/microsoft/WinAppDriver/releases)
4. **Developer Mode** enabled in Windows Settings

## 🚀 설치 (Installation)

### 1. 저장소 클론 (Clone Repository)
```bash
git clone https://github.com/yji0728/Winapp-driver-collector.git
cd Winapp-driver-collector
```

### 2. 의존성 설치 (Install Dependencies)
```bash
pip install -r requirements.txt
```

### 3. WinAppDriver 설치 및 실행 (Install and Run WinAppDriver)
1. [WinAppDriver 다운로드](https://github.com/microsoft/WinAppDriver/releases)
2. 설치 후 `WinAppDriver.exe` 실행
3. 기본적으로 `http://127.0.0.1:4723`에서 실행됨

### 4. Developer Mode 활성화 (Enable Developer Mode)
- Windows Settings → Update & Security → For developers → Developer Mode

## 📖 사용법 (Usage)

### CLI 사용 (CLI Usage)

#### 단일 스크립트 실행 (Run Single Script)
```bash
python src/cli/main.py run --script examples/calculator_test.yaml
```

#### 설정 파일 사용 (Use Configuration File)
```bash
python src/cli/main.py run --script examples/calculator_test.yaml --config config/default.yaml
```

#### 배치 실행 (Batch Execution)
```bash
python src/cli/main.py batch --scripts-dir examples
```

#### 인스펙터 모드 (Inspector Mode)
```bash
python src/cli/main.py inspect --app-path "C:\Windows\System32\calc.exe"
```

#### 버전 정보 (Version Info)
```bash
python src/cli/main.py version
```

### GUI 사용 (GUI Usage)

```bash
python src/gui/main.py
```

GUI에서:
1. **Execute Script** 탭에서 스크립트 선택
2. **▶ Run Script** 버튼 클릭
3. **Results** 탭에서 실행 결과 확인
4. **Script Editor** 탭에서 스크립트 작성/편집

## 📝 스크립트 작성 (Writing Scripts)

스크립트는 YAML 형식으로 작성됩니다:

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
    
  - action: "screenshot"
    filename: "result.png"
```

### 지원되는 액션 (Supported Actions)

- `click`: 요소 클릭
- `double_click`: 더블 클릭
- `send_keys`: 텍스트 입력
- `clear`: 입력 필드 지우기
- `verify`: 요소 검증
- `wait`: 대기
- `screenshot`: 스크린샷 캡처

### 요소 선택자 (Element Selectors)

- `Name`: 요소 이름
- `AutomationId`: 자동화 ID
- `ClassName`: 클래스 이름
- `XPath`: XPath 표현식
- `AccessibilityId`: 접근성 ID

## 📁 프로젝트 구조 (Project Structure)

```
Winapp-driver-collector/
├── src/
│   ├── core/              # 핵심 자동화 엔진
│   │   ├── controller.py  # WinAppDriver 컨트롤러
│   │   └── executor.py    # 스크립트 실행기
│   ├── cli/               # CLI 인터페이스
│   │   └── main.py        # CLI 메인
│   └── gui/               # GUI 인터페이스
│       └── main.py        # GUI 메인
├── examples/              # 예제 스크립트
│   ├── calculator_test.yaml
│   └── notepad_test.yaml
├── config/                # 설정 파일
│   └── default.yaml
├── docs/                  # 문서
│   └── SPECIFICATIONS.md  # 상세 스펙
├── screenshots/           # 스크린샷 저장소
├── logs/                  # 로그 파일
└── requirements.txt       # Python 의존성
```

## 🔧 설정 (Configuration)

`config/default.yaml` 파일에서 설정을 변경할 수 있습니다:

```yaml
winappdriver:
  server_url: "http://127.0.0.1:4723"
  implicit_wait: 10

logging:
  level: "INFO"
  file: "logs/automation.log"

screenshots:
  enabled: true
  directory: "screenshots"
```

## 📚 문서 (Documentation)

- [상세 스펙 문서](docs/SPECIFICATIONS.md) - 전체 기능 및 API 레퍼런스
- [예제 스크립트](examples/) - 다양한 사용 예제

## 🤝 기여 (Contributing)

버그 리포트, 기능 제안, Pull Request를 환영합니다!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스 (License)

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 참고 자료 (References)

- [Microsoft WinAppDriver](https://github.com/microsoft/WinAppDriver)
- [Appium Python Client](https://github.com/appium/python-client)
- [Windows UI Automation](https://docs.microsoft.com/en-us/windows/win32/winauto/entry-uiauto-win32)

## 📧 문의 (Contact)

질문이나 제안사항이 있으시면 Issue를 생성해주세요.

---

Made with ❤️ for Windows Automation