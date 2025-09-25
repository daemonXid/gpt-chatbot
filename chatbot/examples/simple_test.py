import os
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일에서 환경변수를 로드합니다
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

def simple_chat():
    print("=== 간단한 챗봇 테스트 ===")

    user_input = input("질문을 입력하세요: ")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 도움이 되는 AI 어시스턴트입니다."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.7
        )

        print(f"\nAI: {response.choices[0].message.content}")
        print("테스트 성공! ✅")

    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    simple_chat()