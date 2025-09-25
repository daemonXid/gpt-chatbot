# AI 토론 시스템 개발 가이드

## 프로젝트 개요
프롬프트 엔지니어링을 도와주는 솔루션으로, 두 개의 AI(긍정적/부정적)가 토론하는 시스템을 Django로 개발

## 시스템 아키텍처

### AI 구성
- **AI1**: OpenAI API 사용 (긍정적 관점)
- **AI2**: Ollama API 사용 (부정적 관점)
- 각각 다른 시스템 프롬프트로 구성하여 토론 진행

### 핵심 기능
1. **토론 시뮬레이션**: 두 AI 간 대화형 토론
2. **데이터 저장**: 모든 프롬프트와 결과 DB 저장
3. **평가 시스템**: 토론 결과에 대한 점수 매기기
4. **히스토리 조회**: 이전 토론 내용 확인

## 데이터베이스 설계

### 필수 저장 항목
- `ai1_prompt`: AI1의 시스템 프롬프트
- `ai2_prompt`: AI2의 시스템 프롬프트  
- `user_prompt`: 사용자 입력 프롬프트
- `output`: 토론 결과/응답
- `evaluation`: 평가 점수
- `created_at`: 생성 시간
- `updated_at`: 수정 시간

### 추가 고려사항
- 토론 세션 ID로 대화 그룹핑
- 각 턴별 메시지 저장
- 사용자별 히스토리 관리

## 기술 스택

### 백엔드
- **Framework**: Django
- **Database**: PostgreSQL/SQLite
- **AI SDK**: OpenAI Python SDK
- **API Integration**: OpenAI + Ollama

### 프론트엔드
- **디자인**: 네이버 메인페이지 스타일
- **Template**: Django Templates
- **CSS Framework**: 부트스트랩 또는 커스텀 CSS
- **JavaScript**: 실시간 토론 UI 업데이트

## 환경 설정

### 필요한 환경 변수