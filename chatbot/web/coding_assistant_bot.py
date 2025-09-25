import os
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일에서 환경변수를 로드합니다
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

def coding_assistant_bot():
    """
    코딩 도우미 봇
    프로그래밍 관련 질문이나 코드에 대한 도움을 제공합니다
    """
    print("=== 코딩 도우미 봇 ===")
    print("프로그래밍 질문이나 코드 관련 도움이 필요하시면 언제든 물어보세요!")
    print("'quit'를 입력하면 종료됩니다.\n")

    # 사용자로부터 코딩 질문 입력받기
    coding_question = input("코딩 관련 질문이나 도움이 필요한 내용을 입력하세요: ")

    # 종료 조건 확인
    if coding_question.lower() == 'quit':
        print("코딩 도우미 봇을 종료합니다.")
        return

    # 프로그래밍 언어 선택 (선택사항)
    print("\n주로 사용하는 프로그래밍 언어가 있다면 알려주세요:")
    print("(예: Python, JavaScript, Java, C++, C#, Go, Rust 등)")
    programming_language = input("언어명 (모르겠다면 Enter): ").strip()

    try:
        # 프로그래밍 언어가 지정된 경우와 아닌 경우에 따른 프롬프트 조정
        if programming_language:
            system_prompt = f"""당신은 {programming_language} 전문가이자 친절한 코딩 멘토입니다.
            다음을 제공해주세요:
            1. 명확하고 이해하기 쉬운 설명
            2. 실제 동작하는 코드 예시 (가능한 경우)
            3. 모범 사례와 주의사항
            4. 관련된 개념이나 대안 방법

            초보자도 이해할 수 있도록 단계별로 설명해주세요."""
        else:
            system_prompt = """당신은 다양한 프로그래밍 언어에 능통한 코딩 멘토입니다.
            질문에 가장 적합한 언어를 선택하여 다음을 제공해주세요:
            1. 명확하고 이해하기 쉬운 설명
            2. 실제 동작하는 코드 예시 (가능한 경우)
            3. 모범 사례와 주의사항
            4. 관련된 개념이나 대안 방법

            초보자도 이해할 수 있도록 단계별로 설명해주세요."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    # system role: 코딩 멘토 역할 정의
                    "role": "system",
                    "content": system_prompt
                },
                {
                    # user role: 코딩 질문
                    "role": "user",
                    "content": coding_question
                }
            ],
            max_tokens=800,
            temperature=0.3  # 정확한 기술적 답변을 위해 낮은 창의성
        )

        coding_help = response.choices[0].message.content

        print("\n" + "="*70)
        print("💻 코딩 도우미 답변")
        print("="*70)
        print(coding_help)
        print("="*70)

        # 추가 질문 기회 제공
        follow_up = input("\n추가 질문이 있으시면 입력하세요 (없으면 Enter): ").strip()

        if follow_up and follow_up.lower() != 'quit':
            print("\n📝 추가 답변을 생성 중...")

            follow_up_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": coding_question
                    },
                    {
                        "role": "assistant",
                        "content": coding_help
                    },
                    {
                        "role": "user",
                        "content": follow_up
                    }
                ],
                max_tokens=500,
                temperature=0.3
            )

            print("\n" + "="*70)
            print("🔍 추가 답변")
            print("="*70)
            print(follow_up_response.choices[0].message.content)
            print("="*70)

    except Exception as e:
        print(f"코딩 도움 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    coding_assistant_bot()