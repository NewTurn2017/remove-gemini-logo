# Gemini Logo Remover

AI 생성 이미지에서 Gemini 로고를 배치 제거하는 심플한 맥 앱

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 설치

### Homebrew (권장)

```bash
brew tap bear2u/tap
brew install gemini-logo-remover
```

### pip

```bash
pip install gemini-logo-remover
```

### 소스에서 설치

```bash
git clone https://github.com/bear2u/gemini-logo-remover.git
cd gemini-logo-remover
uv sync
uv run python main.py
```

## 사용법

```bash
gemini-logo-remover
```

또는 소스에서:

```bash
uv run python main.py
```

## 기능

- **드래그앤드롭**: 이미지 파일/폴더를 드롭존에 드래그
- **배치 처리**: 멀티스레드(4개)로 병렬 처리
- **설정 옵션**:
  - 로고 위치 (우하단/좌하단/우상단/좌상단)
  - 제거 영역 크기 (5~30%)
  - 출력 폴더 지정

## 지원 형식

PNG, JPG, JPEG, WebP, BMP, TIFF

## 스크린샷

앱 실행 시 다크 테마의 심플한 UI가 표시됩니다:

1. 이미지를 드래그앤드롭 또는 클릭하여 선택
2. 로고 위치와 제거 영역 크기 설정
3. "로고 제거 시작" 클릭
4. 처리된 이미지는 `_clean` 접미사로 저장

## 기술 스택

- **UI**: Tkinter + TkinterDnD2
- **이미지 처리**: OpenCV (TELEA 인페인팅 알고리즘)
- **병렬 처리**: ThreadPoolExecutor

## 라이선스

MIT License
