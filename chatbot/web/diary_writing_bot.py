import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

# .env 파일에서 환경변수를 로드합니다
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

def diary_writing_bot():
    """
    일기 작성 봇
    사용자의 하루 경험을 듣고 의미 있는 일기로 작성해줍니다
    """
    print("=== 일기 작성 봇 ===")
    print("오늘 하루 있었던 일들을 알려주시면 아름다운 일기로 작성해드릴게요!")
    print("'quit'를 입력하면 종료됩니다.\n")

    # 사용자로부터 하루 일과 입력받기
    daily_experience = input("오늘 하루 어떤 일이 있었는지 자유롭게 말씀해주세요: ")

    # 종료 조건 확인
    if daily_experience.lower() == 'quit':
        print("일기 작성 봇을 종료합니다.")
        return

    # 감정 상태 확인
    emotion = input("\n오늘의 전반적인 기분은 어떠셨나요? (예: 기쁨, 우울, 평온, 흥미진진, 피곤 등): ").strip()

    # 특별한 순간이나 깨달음 확인
    special_moment = input("오늘 특별히 기억에 남는 순간이나 깨달은 점이 있다면 알려주세요: ").strip()

    # 일기 스타일 선택
    print("\n어떤 스타일의 일기를 원하시나요?")
    print("1. 감성적이고 문학적인 스타일")
    print("2. 간단하고 솔직한 스타일")
    print("3. 성찰적이고 철학적인 스타일")
    print("4. 유머러스하고 밝은 스타일")

    style_choice = input("선택 (1-4): ").strip()

    # 스타일에 따른 설정
    if style_choice == "1":
        style_instruction = "감성적이고 문학적인 표현을 사용하여 시적인 느낌의 일기"
    elif style_choice == "2":
        style_instruction = "간단하고 솔직한 표현으로 일상적이고 자연스러운 일기"
    elif style_choice == "3":
        style_instruction = "성찰적이고 철학적인 관점에서 깊이 있는 사고가 담긴 일기"
    elif style_choice == "4":
        style_instruction = "유머러스하고 밝은 톤으로 재미있고 긍정적인 일기"
    else:
        style_instruction = "자연스럽고 따뜻한 느낌의 개인적인 일기"

    try:
        # 오늘 날짜 가져오기
        today = datetime.now().strftime("%Y년 %m월 %d일")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    # system role: 일기 작성 도우미 역할 정의
                    "role": "system",
                    "content": f"""당신은 감정적으로 공감하고 아름다운 글을 쓰는 일기 작성 도우미입니다.
                    사용자의 하루 경험을 바탕으로 {style_instruction}를 작성해주세요.

                    일기 작성 가이드라인:
                    1. 사용자의 경험과 감정을 진정성 있게 담아내기
                    2. 하루의 의미와 가치를 발견하도록 도움
                    3. 읽었을 때 따뜻하고 위로가 되는 느낌
                    4. 개인적이고 내밀한 톤 유지
                    5. 날짜를 포함하여 완성된 일기 형태로 작성

                    일기는 300-500자 정도의 적당한 길이로 작성해주세요."""
                },
                {
                    # user role: 일기 작성 요청
                    "role": "user",
                    "content": f"""오늘 날짜: {today}
                    하루 일과: {daily_experience}
                    오늘의 기분: {emotion}
                    특별한 순간: {special_moment}

                    이 정보를 바탕으로 아름다운 일기를 작성해주세요."""
                }
            ],
            max_tokens=600,
            temperature=0.7  # 창의적이고 감성적인 표현을 위해 적절한 창의성
        )

        diary_content = response.choices[0].message.content

        print("\n" + "="*60)
        print("📔 작성된 일기")
        print("="*60)
        print(diary_content)
        print("="*60)

        # 일기 저장 옵션
        save_option = input("\n이 일기를 파일로 저장하시겠습니까? (y/n): ").strip().lower()

        if save_option == 'y' or save_option == 'yes':
            # 날짜를 파일명에 포함
            filename = f"diary_{datetime.now().strftime('%Y%m%d')}.txt"

            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(diary_content)
                print(f"✅ 일기가 저장되었습니다: {filename}")
            except Exception as e:
                print(f"❌ 파일 저장 중 오류 발생: {e}")

        # 추가 일기 작성 제안
        print("\n💝 일기 작성 팁:")
        print("- 매일 조금씩이라도 기록하는 습관을 만들어보세요")
        print("- 감정보다는 구체적인 경험을 중심으로 적어보세요")
        print("- 미래의 자신에게 하는 편지라고 생각해보세요")

    except Exception as e:
        print(f"일기 작성 중 오류가 발생했습니다: {e}")

def reflection_prompt():
    """
    성찰을 돕는 질문들을 제공하는 기능
    """
    print("\n=== 성찰 도우미 ===")
    print("일기를 쓰기 전에 이런 질문들을 생각해보세요:\n")

    reflection_questions = [
        "오늘 가장 감사했던 순간은 언제였나요?",
        "오늘 새롭게 배운 것이 있다면 무엇인가요?",
        "오늘 누군가에게 도움을 주거나 받은 적이 있나요?",
        "오늘 예상과 다르게 흘러간 일이 있었나요?",
        "오늘 내가 성장했다고 느낀 순간이 있었나요?",
        "내일은 오늘보다 어떤 면에서 더 나아지고 싶나요?"
    ]

    for i, question in enumerate(reflection_questions, 1):
        print(f"{i}. {question}")

    print("\n이런 질문들을 통해 하루를 되돌아본 후 일기를 작성하면")
    print("더 의미 있는 일기가 될 수 있어요! 📝")

if __name__ == "__main__":
    while True:
        print("\n📖 일기 작성 봇 메뉴")
        print("1. 일기 작성하기")
        print("2. 성찰 도우미")
        print("3. 종료")

        choice = input("선택하세요 (1-3): ")

        if choice == "1":
            diary_writing_bot()
        elif choice == "2":
            reflection_prompt()
        elif choice == "3":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 1, 2, 3 중에서 선택해주세요.")