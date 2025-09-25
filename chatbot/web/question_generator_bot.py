import os
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일에서 환경변수를 로드합니다
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

def question_generator_bot():
    """
    질문 생성 봇
    주어진 텍스트나 주제를 바탕으로 다양한 질문을 생성합니다
    """
    print("=== 질문 생성 봇 ===")
    print("텍스트나 주제를 입력하면 관련 질문들을 생성해드립니다.")
    print("'quit'를 입력하면 종료됩니다.\n")

    # 사용자로부터 텍스트 또는 주제 입력받기
    input_text = input("질문을 생성할 텍스트나 주제를 입력하세요: ")

    # 종료 조건 확인
    if input_text.lower() == 'quit':
        print("질문 생성 봇을 종료합니다.")
        return

    # 질문 유형 선택
    print("\n생성할 질문 유형을 선택하세요:")
    print("1. 이해도 확인 질문")
    print("2. 토론/논의 질문")
    print("3. 창의적 사고 질문")
    print("4. 모든 유형 질문")

    choice = input("선택 (1-4): ")

    # 질문 유형에 따른 프롬프트 설정
    if choice == "1":
        question_type = "이해도를 확인할 수 있는 질문들"
        instruction = "주요 내용의 이해 정도를 평가할 수 있는 질문"
    elif choice == "2":
        question_type = "토론이나 논의를 유도하는 질문들"
        instruction = "깊이 있는 토론과 다양한 관점을 이끌어낼 수 있는 질문"
    elif choice == "3":
        question_type = "창의적 사고를 자극하는 질문들"
        instruction = "창의성과 비판적 사고를 촉진할 수 있는 질문"
    else:
        question_type = "다양한 유형의 질문들"
        instruction = "이해도 확인, 토론 유도, 창의적 사고 등 다양한 목적의 질문"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    # system role: 질문 생성 전문가 역할 정의
                    "role": "system",
                    "content": f"""당신은 교육 전문가이자 질문 생성 전문가입니다.
                    주어진 텍스트나 주제를 바탕으로 {instruction}을 생성해주세요.

                    다음 형식으로 10개의 질문을 생성해주세요:
                    1. [질문]
                    2. [질문]
                    ...

                    질문은 명확하고 구체적이며 흥미로워야 합니다."""
                },
                {
                    # user role: 질문 생성 요청
                    "role": "user",
                    "content": f"다음 내용을 바탕으로 {question_type}을 생성해주세요:\n\n{input_text}"
                }
            ],
            max_tokens=500,
            temperature=0.7  # 창의적인 질문 생성을 위해 높은 창의성
        )

        questions = response.choices[0].message.content

        print("\n" + "="*60)
        print("❓ 생성된 질문들")
        print("="*60)
        print(questions)
        print("="*60)

    except Exception as e:
        print(f"질문 생성 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    question_generator_bot()