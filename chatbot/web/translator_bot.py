import os
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일에서 환경변수를 로드합니다
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

def translator_bot():
    """
    다국어 번역 봇
    사용자가 입력한 텍스트를 원하는 언어로 번역해줍니다
    """
    print("=== 번역 봇 ===")
    print("번역할 텍스트를 직접 입력해주세요.")
    print("'quit'를 입력하면 종료됩니다.\n")

    # 사용자로부터 번역할 텍스트와 목표 언어를 한 번에 받습니다
    text_to_translate = input("번역할 텍스트를 입력하세요: ")

    # 종료 조건 확인
    if text_to_translate.lower() == 'quit':
        print("번역 봇을 종료합니다.")
        return

    # 목표 언어 입력 받기
    target_language = input("어떤 언어로 번역할까요? (예: 영어, 중국어, 일본어, 프랑스어 등): ")

    try:
        # OpenAI API 호출
        response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        # system role: 번역 전문가 역할을 정의
                        "role": "system",
                        "content": f"""당신은 전문 번역가입니다.
                        사용자가 제공한 텍스트를 {target_language}로 정확하게 번역해주세요.
                        번역 결과만 제공하고, 추가 설명은 하지 마세요.
                        만약 번역이 불가능한 경우에만 이유를 설명해주세요."""
                    },
                    {
                        # user role: 사용자의 번역 요청
                        "role": "user",
                        "content": f"다음 텍스트를 {target_language}로 번역해주세요: {text_to_translate}"
                    }
                ],
                max_tokens=200,  # 번역 결과 길이 제한
                temperature=0.3  # 낮은 창의성으로 정확한 번역
            )

        # 번역 결과 출력
        translation = response.choices[0].message.content
        print(f"\n번역 결과: {translation}")
        print("-" * 50)

    except Exception as e:
        print(f"번역 중 오류가 발생했습니다: {e}")

def batch_translator():
    """
    여러 문장을 한 번에 번역하는 기능
    """
    print("\n=== 일괄 번역 모드 ===")
    target_language = input("목표 언어: ")

    sentences = []
    print("번역할 문장들을 입력하세요 (빈 줄을 입력하면 번역 시작):")

    while True:
        sentence = input()
        if sentence == "":
            break
        sentences.append(sentence)

    if not sentences:
        print("번역할 문장이 없습니다.")
        return

    try:
        # 여러 문장을 한 번에 번역하도록 프롬프트 구성
        text_to_translate = "\n".join([f"{i+1}. {sentence}" for i, sentence in enumerate(sentences)])

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"""당신은 전문 번역가입니다.
                    다음 문장들을 {target_language}로 번역해주세요.
                    번호와 함께 각 문장을 번역하여 결과를 제공해주세요."""
                },
                {
                    "role": "user",
                    "content": text_to_translate
                }
            ],
            max_tokens=500,
            temperature=0.3
        )

        print(f"\n=== {target_language} 번역 결과 ===")
        print(response.choices[0].message.content)

    except Exception as e:
        print(f"일괄 번역 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    while True:
        print("\n1. 단일 번역")
        print("2. 일괄 번역")
        print("3. 종료")

        choice = input("선택하세요 (1-3): ")

        if choice == "1":
            translator_bot()
        elif choice == "2":
            batch_translator()
        elif choice == "3":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 1, 2, 3 중에서 선택해주세요.")