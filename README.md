
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.3.2-7289DA.svg)](https://github.com/Rapptz/discord.py)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini%20API-4285F4.svg)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---
물론입니다. 수많은 오류를 거쳐 마침내 완성된 봇을 위한 `README.md` 파일을 작성해 드리겠습니다. 간결하지만 모든 핵심 내용이 포함되도록 만들었습니다.

---

# Studyme2

**Studyme2**는 Google의 Gemini 1.5 Flash 모델을 기반으로 한 지능형 디스코드 봇입니다. 서버 구성원들에 대한 정보를 기억하고, 사용자 간의 관계를 연결하여 서버 전체를 위한 '소셜 메모리(Social Memory)'를 구축합니다.

## ✨ 핵심 기능

*   **🧠 개인 기억 관리**: 사용자가 자기 자신에 대해 말하는 정보(이름, 취미, 직업 등)를 저장, 수정, 삭제합니다.
*   **🌐 사용자 간 정보 연결**: 다른 사용자가 특정 인물에 대해 질문했을 때, 기억 속에서 해당 인물을 찾아내고 관련 정보를 알려줍니다.
*   **🗣️ 자연어 기반 상호작용**: `!기억해` 와 같은 딱딱한 명령어가 필요 없습니다. 그냥 평범하게 대화하면 봇이 맥락을 이해하고 스스로 판단하여 행동합니다.
*   **🛠️ 자율적인 도구 사용**: 질문의 의도를 파악한 뒤, '유저 찾기', '기억 검색', '정보 저장' 등 자신이 가진 도구(Tool)를 자율적으로 선택하고 순서에 맞게 사용하여 답변을 찾아냅니다.

## 🚀 시작하기

### 1. 사전 준비

*   Python 3.9 이상
*   Discord Bot Token
*   Google AI (Gemini) API Key

### 2. 설치 및 설정

1.  **프로젝트 클론**
    ```bash
    git clone <repository-url>
    cd Studyme2
    ```

2.  **가상 환경 생성 및 활성화**
    ```bash
    # Windows
    python -m venv .venv
    .\.venv\Scripts\activate

    # macOS / Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **필요 라이브러리 설치**
    ```bash
    pip install -r requirements.txt
    ```

4.  **.env 파일 생성**
    프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 아래 내용을 채워넣으세요. **따옴표는 사용하지 마세요.**
    ```env
    DISCORD_TOKEN=여러분의_디스코드봇_토큰을_입력하세요
    GEMINI_API_KEY=여러분의_Gemini_API_키를_입력하세요
    ```

### 3. 봇 실행

```bash
python main.py
```

## 🤖 활용 방법

봇을 서버에 초대한 후, 채널에서 자연스럽게 대화하면 됩니다.

---

### **예시 1: 내 정보 기억시키기**

> **나 (배건우):** 안녕, 내 이름은 배건우야.
>
> **Studyme2:** 알겠습니다. 이제부터 당신을 '배건우'(으)로도 기억하겠습니다.
>
> **나 (배건우):** 내 직업은 AI 연구원이고, 체스를 엄청 좋아해.
>
> **Studyme2:** 기억했습니다. 당신의 직업은 AI 연구원이고, 체스를 좋아한다는 사실을 저장했습니다.

### **예시 2: 내 정보 물어보기**

> **나 (배건우):** 내가 뭘 좋아한다고 했지?
>
> **Studyme2:** 당신은 체스를 엄청 좋아한다고 기억하고 있습니다.

### **예시 3: 다른 사람 정보 물어보기 (핵심 기능)**

> **다른 유저 (김한준):** 혹시 배건우님에 대해 아는 거 있어?
>
> **Studyme2:** 네, 확인해 보니 배건우님은 AI 연구원이며, 체스를 매우 좋아한다고 기록되어 있습니다.

### **예시 4: 정보 수정 및 삭제하기**

> **나 (배건우):** 아, 나 이제 직업이 프로그래머로 바뀌었어.
>
> **Studyme2:** 알겠습니다. 직업 정보를 'AI 연구원'에서 '프로그래머'로 업데이트했습니다.
>
> **나 (배건우):** 내 직업 정보는 이제 잊어줘.
>
> **Studyme2:** 관련 기억('사용자의 직업은 프로그래머이다')이 성공적으로 삭제되었습니다.

---
**기존 Studyme2와 바뀐점**
제미나이의 function calling 기능을 활용해 토큰 소모를 기존의 40%로 줄였습니다
기존의 프로젝트 보다 훨씬 경량화된 구조를 띄고있고, 더 유연한 DB관리가 가능합니다.
