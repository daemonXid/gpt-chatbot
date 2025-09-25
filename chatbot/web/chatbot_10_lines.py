import os
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일에서 환경변수를 로드합니다
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

def chat_10_lines():
    """
    10줄까지만 대화할 수 있는 챗봇
    대화 내역을 리스트로 관리하여 컨텍스트를 유지합니다
    """
    # 대화 내역을 저장할 리스트 (최대 10줄까지만 유지)
    conversation = []

    print("=== 10줄 대화 챗봇 ===")
    print("최대 10줄까지 대화할 수 있습니다. 'quit'를 입력하면 종료됩니다.")

    # 사용자가 시작할 질문을 받습니다
    initial_question = input("첫 번째 질문을 입력하세요: ")
    if initial_question.lower() == 'quit':
        print("대화를 종료합니다.")
        return

    # 첫 번째 질문을 대화에 추가
    conversation.append({"role": "user", "content": initial_question})
    turn = 1

    for turn in range(1, 11):  # 최대 10번의 대화 턴
        # 첫 번째 턴이 아니라면 사용자 입력 받기
        if turn > 1:
            user_input = input(f"\n[{turn}/10] 당신: ")

            # 종료 조건 확인
            if user_input.lower() == 'quit':
                print("대화를 종료합니다.")
                break

            # 사용자 메시지를 대화 내역에 추가
            conversation.append({"role": "user", "content": user_input})

        try:
            # OpenAI API 호출
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # 사용할 모델 지정
                messages=[
                    # system role: AI의 역할과 행동 방식을 정의
                    {"role": "system", "content": "당신은 친근하고 도움이 되는 한국어 대화 파트너입니다. 간단하고 명확하게 답변해주세요."},
                ] + conversation,  # 기존 대화 내역과 합치기
                max_tokens=150,  # 응답 길이 제한
                temperature=0.7  # 창의성 수준 (0-1, 높을수록 창의적)
            )

            # AI 응답 추출
            ai_response = response.choices[0].message.content
            print(f"AI: {ai_response}")

            # AI 응답을 대화 내역에 추가
            conversation.append({"role": "assistant", "content": ai_response})

        except Exception as e:
            print(f"오류가 발생했습니다: {e}")
            break

    print(f"\n대화가 종료되었습니다. 총 {len(conversation)//2}번의 대화를 나누었습니다.")

if __name__ == "__main__":
    chat_10_lines()


    # 127.0.0.1:8000/chatbot_10_lines.py