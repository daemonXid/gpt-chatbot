# 🤖 AI 챗봇 모음

OpenAI API를 활용한 다양한 용도의 AI 챗봇 모음입니다.

## 📁 프로젝트 구조

```
gpt-chatbot/
├── app.py                      # Flask 웹 애플리케이션 메인 파일
├── .env                        # OpenAI API 키 설정 파일
├── requirements.txt            # 필요한 Python 라이브러리
├── README.md                   # 프로젝트 설명서
├── templates/                  # HTML 템플릿
│   ├── index.html             # 메인 페이지
│   └── chatbot.html           # 챗봇 페이지
├── static/                     # 정적 파일 (CSS, JS, 이미지)
└── chatbot/                    # 🤖 챗봇 모듈들 (용도별 분류)
    ├── __init__.py            # 패키지 초기화 파일
    │
    ├── web/                   # 🌐 웹 인터페이스 지원 챗봇들
    │   ├── __init__.py
    │   ├── README.md          # 웹 챗봇 사용법
    │   ├── chatbot_10_lines.py    # 10줄 대화 챗봇
    │   ├── translator_bot.py      # 번역 봇
    │   ├── summarizer_bot.py      # 요약 봇
    │   ├── question_generator_bot.py # 질문 생성 봇
    │   ├── coding_assistant_bot.py   # 코딩 도우미 봇
    │   └── diary_writing_bot.py      # 일기 작성 봇
    │
    ├── advanced/              # 🚀 고급 API 활용 챗봇들 (터미널 전용)
    │   ├── __init__.py
    │   ├── README.md          # 고급 챗봇 사용법
    │   ├── email_classifier_bot.py   # 이메일 분류 (Embeddings API)
    │   ├── podcast_transcription_bot.py # 음성 변환 (Whisper API)
    │   └── news_clustering_bot.py    # 뉴스 그룹화 (Embeddings API)
    │
    ├── terminal/              # 💻 터미널 전용 실행 스크립트들
    │   ├── __init__.py
    │   ├── run_chat.py        # 터미널용 대화 봇
    │   └── run_translator.py  # 터미널용 번역 봇
    │
    └── examples/              # 🔧 예제 및 테스트 파일들
        ├── __init__.py
        ├── conversations.py   # 대화 예제 코드
        ├── hello_ai.py       # 기본 AI 테스트
        ├── simple_test.py    # 간단한 테스트
        └── test_setup.py     # 설정 테스트
```

## 🚀 실행 방법

### 웹 애플리케이션 (추천)
```bash
# 1. 프로젝트 디렉토리로 이동
cd "C:\Users\songw\Documents\likelion_workspace\real-projects\gpt-chatbot"

# 2. Flask 앱 실행
python app.py

# 3. 브라우저에서 접속
# http://127.0.0.1:8000
```

### 개별 챗봇 (터미널)

**🌐 웹 챗봇들 (터미널에서 실행):**
```bash
python chatbot/web/chatbot_10_lines.py
python chatbot/web/translator_bot.py
python chatbot/web/summarizer_bot.py
python chatbot/web/question_generator_bot.py
python chatbot/web/coding_assistant_bot.py
python chatbot/web/diary_writing_bot.py
```

**🚀 고급 API 챗봇들 (터미널 전용):**
```bash
python chatbot/advanced/email_classifier_bot.py
python chatbot/advanced/podcast_transcription_bot.py
python chatbot/advanced/news_clustering_bot.py
```

**💻 터미널 전용 스크립트들:**
```bash
python chatbot/terminal/run_chat.py
python chatbot/terminal/run_translator.py
```

**🔧 예제 및 테스트:**
```bash
python chatbot/examples/hello_ai.py
python chatbot/examples/simple_test.py
```

## 🤖 챗봇 종류

### 웹 인터페이스 지원 (6개)
1. **10줄 대화 챗봇** - 자연스러운 대화 (최대 10턴)
2. **번역 봇** - 다국어 번역 (`"안녕하세요" -> 영어`)
3. **요약 봇** - 긴 텍스트 요약
4. **질문 생성 봇** - 주제별 질문 생성
5. **코딩 도우미 봇** - 프로그래밍 도움
6. **일기 작성 봇** - 감성적인 일기 작성

### 터미널 전용 (3개)
7. **이메일 분류 봇** - Embeddings API로 고객 문의 자동 분류
8. **음성 변환 봇** - Whisper API로 오디오→텍스트 변환
9. **뉴스 그룹화 봇** - Embeddings API로 유사 뉴스 클러스터링

## ⚙️ 설정 방법

### 1. 환경 설정
```bash
# 필요한 라이브러리 설치
pip install openai python-dotenv flask numpy scikit-learn
```

### 2. API 키 설정
`.env` 파일에 OpenAI API 키 설정:
```
OPENAI_API_KEY=your-openai-api-key-here
```

## 🔧 사용된 기술

### OpenAI API
- **Chat Completions API**: 대화형 AI, 텍스트 생성
- **Embeddings API**: 텍스트 벡터화, 의미적 유사성 계산
- **Whisper API**: 음성을 텍스트로 변환

### 웹 프레임워크
- **Flask**: Python 웹 애플리케이션 프레임워크
- **HTML/CSS/JavaScript**: 반응형 웹 인터페이스

### 머신러닝
- **scikit-learn**: 클러스터링 및 유사도 계산
- **numpy**: 수치 계산

## 🎯 주요 기능

### 3가지 Role 시스템
1. **system role**: AI의 역할과 행동 방식 정의
2. **user role**: 사용자의 입력 내용
3. **assistant role**: AI의 응답 (대화 맥락 유지)

### 웹 인터페이스 특징
- 🌐 반응형 디자인 (모바일/데스크톱)
- 💬 실시간 채팅 인터페이스
- 🔄 대화 초기화 기능
- 📱 직관적인 UI/UX

### 고급 기능
- 📧 의미 기반 이메일 분류
- 🎙️ 고정밀 음성 인식
- 📰 뉴스 자동 그룹화
- 🧠 임베딩 벡터 활용

## 📞 문의

프로젝트 관련 문의사항이 있으시면 언제든 말씀해주세요!