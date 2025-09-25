"""
팟캐스트 음성 변환 챗봇 - Whisper API 활용

이 봇이 할 수 있는 일:
1. 오디오/비디오 파일을 정확한 텍스트로 변환
2. 다국어 음성 인식 (100+ 언어 지원)
3. 노이즈가 있는 환경에서도 높은 정확도
4. 화자 구분 및 타임스탬프 제공
5. 팟캐스트, 회의, 강의 등 긴 오디오 처리

사용하는 API:
- Whisper API: OpenAI의 강력한 음성 인식 모델
- Chat Completions API: 변환된 텍스트 후처리 및 요약

활용 시나리오:
- 팟캐스트 에피소드를 텍스트로 변환하여 검색 가능한 콘텐츠 생성
- 회의록 자동 생성
- 온라인 강의 자막 생성
- 콘텐츠 크리에이터를 위한 스크립트 추출
- 접근성 향상을 위한 자막 제공

지원 파일 형식:
- MP3, MP4, M4A, WAV, WEBM, OGG 등
- 최대 25MB 파일 크기
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
import json
from datetime import datetime

# .env 파일에서 환경변수를 로드합니다
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

class PodcastTranscriber:
    def __init__(self):
        self.supported_formats = ['.mp3', '.mp4', '.m4a', '.wav', '.webm', '.ogg']
        self.max_file_size = 25 * 1024 * 1024  # 25MB

    def check_file_validity(self, file_path):
        """
        파일이 유효한지 확인하는 함수
        - 파일 존재 여부
        - 지원되는 형식인지
        - 파일 크기 제한
        """
        if not os.path.exists(file_path):
            return False, "파일이 존재하지 않습니다."

        # 파일 확장자 확인
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension not in self.supported_formats:
            return False, f"지원하지 않는 파일 형식입니다. 지원 형식: {', '.join(self.supported_formats)}"

        # 파일 크기 확인
        file_size = os.path.getsize(file_path)
        if file_size > self.max_file_size:
            return False, f"파일 크기가 너무 큽니다. 최대 25MB까지 지원합니다. (현재: {file_size / (1024*1024):.1f}MB)"

        return True, "파일이 유효합니다."

    def transcribe_audio(self, file_path, language=None):
        """
        Whisper API를 사용하여 오디오 파일을 텍스트로 변환하는 함수

        매개변수:
        - file_path: 오디오 파일 경로
        - language: 언어 코드 (예: 'ko' for Korean, 'en' for English)
                   None이면 자동 감지
        """
        # 파일 유효성 검사
        is_valid, message = self.check_file_validity(file_path)
        if not is_valid:
            return None, message

        print("음성 파일을 텍스트로 변환 중입니다...")
        print("파일 크기가 클 경우 시간이 오래 걸릴 수 있습니다.")

        try:
            # 오디오 파일 열기
            with open(file_path, 'rb') as audio_file:
                # Whisper API 호출
                if language:
                    # 언어를 지정한 경우
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        language=language,  # 언어 지정으로 정확도 향상
                        response_format="verbose_json"  # 상세 정보 포함
                    )
                else:
                    # 언어 자동 감지
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        response_format="verbose_json"  # 상세 정보 포함
                    )

            return transcript, "변환 성공"

        except Exception as e:
            return None, f"음성 변환 중 오류 발생: {e}"

    def post_process_transcript(self, transcript_text):
        """
        Chat Completions API를 사용하여 변환된 텍스트를 후처리하는 함수
        - 문장 구분
        - 문법 교정
        - 읽기 쉽게 포맷팅
        """
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """당신은 텍스트 편집 전문가입니다.
                        음성으로 변환된 텍스트를 다음과 같이 정리해주세요:
                        1. 적절한 문장 구분과 문단 나누기
                        2. 불필요한 반복이나 말더듬 제거
                        3. 자연스러운 문법으로 수정
                        4. 읽기 쉽게 포맷팅

                        원본의 의미는 그대로 유지해주세요."""
                    },
                    {
                        "role": "user",
                        "content": f"다음 텍스트를 정리해주세요:\n\n{transcript_text}"
                    }
                ],
                max_tokens=1500,
                temperature=0.3
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"텍스트 후처리 중 오류 발생: {e}"

    def summarize_transcript(self, transcript_text):
        """
        변환된 텍스트를 요약하는 함수
        """
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """당신은 콘텐츠 요약 전문가입니다.
                        팟캐스트나 오디오 콘텐츠의 핵심 내용을 다음과 같이 정리해주세요:
                        1. 주요 주제 및 논점
                        2. 핵심 인사이트 (3-5개)
                        3. 결론 또는 액션 아이템
                        4. 전체적인 톤과 분위기"""
                    },
                    {
                        "role": "user",
                        "content": f"다음 텍스트를 요약해주세요:\n\n{transcript_text}"
                    }
                ],
                max_tokens=500,
                temperature=0.5
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"요약 생성 중 오류 발생: {e}"

    def save_transcript(self, transcript_data, file_path, cleaned_text=None, summary=None):
        """
        변환 결과를 파일로 저장하는 함수
        """
        try:
            # 원본 파일명에서 확장자 제거하고 _transcript.txt 추가
            base_name = os.path.splitext(file_path)[0]
            output_file = f"{base_name}_transcript.txt"

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("=== 팟캐스트 음성 변환 결과 ===\n")
                f.write(f"원본 파일: {os.path.basename(file_path)}\n")
                f.write(f"변환 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"언어: {transcript_data.get('language', '자동감지')}\n")
                f.write(f"길이: {transcript_data.get('duration', 'N/A')}초\n")
                f.write("\n" + "="*50 + "\n\n")

                # 원본 변환 텍스트
                f.write("📝 원본 변환 텍스트:\n")
                f.write("-" * 30 + "\n")
                f.write(transcript_data['text'])
                f.write("\n\n")

                # 정리된 텍스트 (있는 경우)
                if cleaned_text:
                    f.write("✨ 정리된 텍스트:\n")
                    f.write("-" * 30 + "\n")
                    f.write(cleaned_text)
                    f.write("\n\n")

                # 요약 (있는 경우)
                if summary:
                    f.write("📋 요약:\n")
                    f.write("-" * 30 + "\n")
                    f.write(summary)
                    f.write("\n\n")

            return output_file

        except Exception as e:
            print(f"파일 저장 중 오류 발생: {e}")
            return None

def main():
    """
    메인 함수 - 팟캐스트 변환 봇 실행
    """
    print("=== 팟캐스트 음성 변환 봇 ===")
    print("오디오/비디오 파일을 텍스트로 변환해드립니다.")
    print("'quit'를 입력하면 종료됩니다.\n")

    transcriber = PodcastTranscriber()

    # 파일 경로 입력받기
    file_path = input("변환할 오디오/비디오 파일 경로를 입력하세요: ")

    if file_path.lower() == 'quit':
        print("음성 변환 봇을 종료합니다.")
        return

    # 따옴표 제거 (파일 경로에 따옴표가 있을 경우)
    file_path = file_path.strip('"\'')

    # 언어 설정 (선택사항)
    print("\n언어를 지정하시겠습니까? (더 정확한 결과를 얻을 수 있습니다)")
    print("예: ko (한국어), en (영어), ja (일본어), zh (중국어)")
    language = input("언어 코드를 입력하세요 (자동감지하려면 Enter): ").strip()

    if not language:
        language = None

    # 음성 변환 실행
    transcript_data, message = transcriber.transcribe_audio(file_path, language)

    if transcript_data:
        print("\n" + "="*60)
        print("🎵 음성 변환 완료!")
        print("="*60)
        print(f"파일: {os.path.basename(file_path)}")
        print(f"언어: {transcript_data.get('language', '자동감지')}")
        print(f"길이: {transcript_data.get('duration', 'N/A')}초")
        print("\n📝 변환된 텍스트:")
        print("-" * 40)
        print(transcript_data['text'])

        # 추가 처리 옵션
        print("\n" + "="*40)
        print("추가 처리 옵션:")
        print("1. 텍스트 정리 및 포맷팅")
        print("2. 내용 요약 생성")
        print("3. 결과를 파일로 저장")
        print("4. 모든 처리 수행")

        choice = input("선택하세요 (1-4, Enter는 건너뛰기): ").strip()

        cleaned_text = None
        summary = None

        if choice in ['1', '4']:
            print("\n텍스트를 정리하고 있습니다...")
            cleaned_text = transcriber.post_process_transcript(transcript_data['text'])
            print("\n✨ 정리된 텍스트:")
            print("-" * 40)
            print(cleaned_text)

        if choice in ['2', '4']:
            print("\n내용을 요약하고 있습니다...")
            summary = transcriber.summarize_transcript(transcript_data['text'])
            print("\n📋 요약:")
            print("-" * 40)
            print(summary)

        if choice in ['3', '4']:
            print("\n결과를 파일로 저장하고 있습니다...")
            output_file = transcriber.save_transcript(transcript_data, file_path, cleaned_text, summary)
            if output_file:
                print(f"✅ 결과가 저장되었습니다: {output_file}")
            else:
                print("❌ 파일 저장에 실패했습니다.")

        print("\n" + "="*60)

    else:
        print(f"\n❌ 변환 실패: {message}")

def demo_mode():
    """
    데모 모드 - 샘플 설명
    """
    print("\n=== 데모 모드 ===")
    print("실제 오디오 파일이 필요한 기능입니다.")
    print("\n사용 예시:")
    print("1. 파일 경로 입력: C:/Users/podcast_episode.mp3")
    print("2. 언어 선택: ko (한국어)")
    print("3. 변환 실행 및 결과 확인")
    print("\n지원하는 파일 형식:")
    transcriber = PodcastTranscriber()
    print(f"- {', '.join(transcriber.supported_formats)}")
    print(f"- 최대 파일 크기: 25MB")

if __name__ == "__main__":
    while True:
        print("\n🎙️ 팟캐스트 음성 변환 봇 메뉴")
        print("1. 음성 파일 변환")
        print("2. 사용법 및 데모")
        print("3. 종료")

        choice = input("선택하세요 (1-3): ")

        if choice == "1":
            main()
        elif choice == "2":
            demo_mode()
        elif choice == "3":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 1, 2, 3 중에서 선택해주세요.")