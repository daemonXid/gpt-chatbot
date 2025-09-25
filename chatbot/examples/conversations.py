# conversation.py
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_ai():
    """AI와 대화하기"""

    # 대화 기록 저장
    messages = [
        {"role": "system", "content": "당신은 친절한 학습 도우미입니다."}
    ]

    print("AI 도우미: 안녕하세요! 무엇이 궁금하신가요?")
    print("(종료하려면 'quit' 입력)")
    print("-" * 50)

    while True:
        # 사용자 입력
        user_input = input("나: ")

        # 종료 조건
        if user_input.lower() == 'quit':
            print("AI 도우미: 안녕히 가세요!")
            break

        # 사용자 메시지 추가
        messages.append({"role": "user", "content": user_input})

        # AI 응답 생성
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        # AI 응답 추출
        ai_message = response.choices[0].message.content

        # AI 메시지 기록
        messages.append({"role": "assistant", "content": ai_message})

        # 응답 출력
        print(f"AI 도우미: {ai_message}")
        print("-" * 50)

# 실행
if __name__ == "__main__":
    chat_with_ai()
