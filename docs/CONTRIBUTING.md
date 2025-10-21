# Contributing to WinAppDriver Automation Framework

Thank you for your interest in contributing to the WinAppDriver Automation Framework! This document provides guidelines for contributing to the project.

## 기여 방법 (How to Contribute)

### 버그 리포트 (Bug Reports)

버그를 발견하셨나요? 다음 정보를 포함하여 Issue를 생성해주세요:

Found a bug? Please create an Issue with the following information:

- **버그 설명 (Bug Description)**: 무엇이 잘못되었는지 명확하게 설명
- **재현 단계 (Steps to Reproduce)**: 버그를 재현하는 단계별 방법
- **예상 동작 (Expected Behavior)**: 어떻게 동작해야 하는지
- **실제 동작 (Actual Behavior)**: 실제로 어떻게 동작하는지
- **환경 정보 (Environment)**:
  - Windows 버전
  - Python 버전
  - WinAppDriver 버전
  - 관련 패키지 버전

### 기능 제안 (Feature Requests)

새로운 기능을 제안하시려면 Issue를 생성하고 다음을 포함해주세요:

To suggest a new feature, create an Issue and include:

- **기능 설명 (Feature Description)**: 제안하는 기능에 대한 상세 설명
- **사용 사례 (Use Case)**: 이 기능이 왜 필요한지
- **제안된 구현 (Proposed Implementation)**: 어떻게 구현할 수 있을지 (선택사항)

## 개발 환경 설정 (Development Setup)

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
git clone https://github.com/YOUR_USERNAME/Winapp-driver-collector.git
cd Winapp-driver-collector
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install -e .  # Install in editable mode
```

### 4. Install Development Dependencies

```bash
pip install pytest pytest-cov black flake8
```

## 코딩 가이드라인 (Coding Guidelines)

### Python Style

- **PEP 8**: Python 코드는 PEP 8 스타일 가이드를 따릅니다
- **Docstrings**: 모든 public 함수와 클래스에 docstring 작성
- **Type Hints**: 가능한 경우 type hints 사용

### Code Formatting

```bash
# Format code with black
black src/

# Check with flake8
flake8 src/
```

### Documentation

- 모든 새로운 기능은 문서화되어야 합니다
- README, API_REFERENCE, SPECIFICATIONS 문서 업데이트
- 예제 스크립트 제공 (필요시)

## Pull Request 프로세스 (Pull Request Process)

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-number
```

### 2. Make Changes

- 작은 단위로 커밋하세요
- 명확한 커밋 메시지 작성
- 테스트 작성 (가능한 경우)

### 3. Test Your Changes

```bash
# Run tests
pytest

# Test CLI
python src/cli/main.py version

# Test GUI (if applicable)
python src/gui/main.py
```

### 4. Update Documentation

- README.md 업데이트 (필요시)
- CHANGELOG.md 업데이트
- API_REFERENCE.md 업데이트 (API 변경시)

### 5. Commit and Push

```bash
git add .
git commit -m "Add feature: description of feature"
git push origin feature/your-feature-name
```

### 6. Create Pull Request

- GitHub에서 Pull Request 생성
- 변경 사항에 대한 명확한 설명 작성
- 관련 Issue 링크

## Pull Request 체크리스트 (Checklist)

PR을 제출하기 전에 다음을 확인하세요:

Before submitting a PR, ensure:

- [ ] 코드가 PEP 8 스타일 가이드를 따름
- [ ] 모든 테스트가 통과함
- [ ] 새로운 기능에 대한 테스트 추가
- [ ] 문서가 업데이트됨
- [ ] 커밋 메시지가 명확함
- [ ] 변경 사항이 기존 기능을 손상시키지 않음

## 커밋 메시지 가이드라인 (Commit Message Guidelines)

좋은 커밋 메시지 형식:

Good commit message format:

```
Type: Brief description (50 chars or less)

More detailed explanation if necessary. Wrap at 72 characters.
Explain what and why, not how.

Fixes #123
```

### Types:

- **feat**: 새로운 기능
- **fix**: 버그 수정
- **docs**: 문서 변경
- **style**: 코드 스타일 변경 (formatting, 세미콜론 등)
- **refactor**: 코드 리팩토링
- **test**: 테스트 추가 또는 수정
- **chore**: 빌드 프로세스 또는 도구 변경

### Examples:

```
feat: Add batch execution mode to CLI

Implement batch mode that allows running multiple scripts
sequentially with aggregated results.

Fixes #45
```

```
fix: Handle timeout exception in element finder

Previously, timeout exceptions were not caught properly,
causing the application to crash.

Fixes #67
```

## 코드 리뷰 프로세스 (Code Review Process)

1. **자동 검사**: CI가 자동으로 테스트와 린트를 실행합니다
2. **리뷰어 할당**: 메인테이너가 리뷰어를 할당합니다
3. **리뷰 및 피드백**: 리뷰어가 코드를 검토하고 피드백을 제공합니다
4. **수정**: 피드백에 따라 코드를 수정합니다
5. **승인 및 머지**: 모든 피드백이 해결되면 PR이 머지됩니다

## 테스트 작성 (Writing Tests)

### Unit Tests

```python
# tests/test_controller.py
import pytest
from core.controller import WinAppDriverController

def test_controller_initialization():
    controller = WinAppDriverController()
    assert controller.server_url == "http://127.0.0.1:4723"
    assert controller.implicit_wait == 10
```

### Integration Tests

```python
# tests/test_integration.py
import pytest
from core.controller import WinAppDriverController
from core.executor import ScriptExecutor

@pytest.mark.integration
def test_execute_calculator_script():
    controller = WinAppDriverController()
    executor = ScriptExecutor(controller)
    result = executor.execute_script_file("examples/calculator_test.yaml")
    assert result['status'] == 'success'
```

## 질문이 있으신가요? (Questions?)

- GitHub Discussions에 질문을 게시하세요
- Issue를 통해 문의하세요
- 또는 프로젝트 메인테이너에게 연락하세요

## 행동 강령 (Code of Conduct)

### 우리의 약속 (Our Pledge)

우리는 모든 사람이 환영받는 환경을 만들기 위해 노력합니다.

We are committed to providing a welcoming and inclusive environment for everyone.

### 우리의 기준 (Our Standards)

긍정적인 환경을 위한 행동:

Positive behaviors include:

- 다른 관점과 경험 존중
- 건설적인 피드백 제공 및 수용
- 커뮤니티 최선의 이익을 위한 행동

부적절한 행동:

Unacceptable behaviors include:

- 괴롭힘, 차별, 또는 모욕적인 언어
- 다른 사람의 개인 정보 공개
- 전문적이지 않은 행동

## 감사합니다! (Thank You!)

여러분의 기여가 이 프로젝트를 더 좋게 만듭니다!

Your contributions make this project better!

---

Happy Contributing! 🎉
