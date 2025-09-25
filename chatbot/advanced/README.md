# 🚀 고급 API 활용 챗봇들

이 폴더의 챗봇들은 **특수한 OpenAI API**를 사용하는 고급 기능을 제공합니다.
**터미널에서만** 실행 가능하며, 웹 인터페이스는 지원하지 않습니다.

## ⚠️ 주의사항

이 챗봇들은 일반적인 Chat Completions API 외에 추가 API를 사용합니다:
- **Embeddings API**: 텍스트 벡터화 및 유사성 계산
- **Whisper API**: 음성을 텍스트로 변환

## 🤖 포함된 챗봇들

### 1. **email_classifier_bot.py** - 이메일 분류 봇
- **사용 API**: Embeddings API + Chat Completions API
- **기능**: 고객 문의 이메일을 7가지 카테고리로 자동 분류
- **활용**: 고객 서비스 자동화, 헬프데스크 티켓 분류

```bash
python chatbot/advanced/email_classifier_bot.py
```

**분류 카테고리**:
- 배송 문의, 반품/교환, 결제 문제, 제품 문의
- 기술 지원, 계정 문제, 일반 문의

### 2. **podcast_transcription_bot.py** - 음성 변환 봇
- **사용 API**: Whisper API + Chat Completions API
- **기능**: 오디오/비디오 파일을 정확한 텍스트로 변환
- **활용**: 팟캐스트 자막, 회의록, 강의 스크립트 생성

```bash
python chatbot/advanced/podcast_transcription_bot.py
```

**지원 형식**: MP3, MP4, M4A, WAV, WEBM, OGG (최대 25MB)

### 3. **news_clustering_bot.py** - 뉴스 그룹화 봇
- **사용 API**: Embeddings API + Chat Completions API
- **기능**: 유사한 주제의 뉴스 기사들을 자동으로 그룹화
- **활용**: 뉴스 큐레이션, 트렌드 분석, 중복 기사 탐지

```bash
python chatbot/advanced/news_clustering_bot.py
```

**주요 기능**:
- K-means 클러스터링
- 코사인 유사도 계산
- 클러스터별 분석 및 요약

## 📊 기술적 세부사항

### Embeddings API 활용
- **모델**: text-embedding-ada-002
- **용도**: 텍스트의 의미를 벡터로 변환
- **응용**: 유사성 측정, 분류, 클러스터링

### Whisper API 활용
- **모델**: whisper-1
- **용도**: 음성을 텍스트로 변환
- **특징**: 100+ 언어 지원, 노이즈 환경 대응

### 머신러닝 라이브러리
- **scikit-learn**: 클러스터링, 유사도 계산
- **numpy**: 수치 계산 및 배열 처리

## 🔧 필요한 라이브러리

```bash
pip install openai numpy scikit-learn matplotlib seaborn
```

## 💡 활용 시나리오

### 비즈니스
- 고객 서비스 자동화 (이메일 분류)
- 콘텐츠 관리 (뉴스 그룹화)
- 미디어 제작 (음성 변환)

### 교육/연구
- 텍스트 마이닝 연구
- 자연어 처리 학습
- AI 애플리케이션 프로토타입