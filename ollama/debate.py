from openai import OpenAI
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv(override=True)

# 클라이언트 구성: base_url을 Ollama 엔드포인트로, api_key는 dummy 값 사용
client = OpenAI(
    base_url=os.getenv("OLLAMA_BASE_URL"),
    api_key="ollama",
)

# --- 토론 설정 ---
DEBATE_TOPIC = "AI 기술 발전은 인류에게 궁극적으로 이로운가?"
DEBATE_ROUNDS = 3

# 페르소나 정의
persona_1_system_prompt = {
    "role": "system",
    "content": "당신은 AI 기술의 열렬한 지지자입니다. AI가 인류의 모든 문제를 해결하고 전례 없는 번영을 가져올 것이라고 굳게 믿고 있습니다. 긍정적이고 미래지향적인 관점에서 주장을 펼치세요."
}

persona_2_system_prompt = {
    "role": "system",
    "content": "당신은 AI 기술에 대해 신중한 비평가입니다. AI의 잠재적 위험성(일자리 감소, 통제 불능, 윤리적 문제 등)을 깊이 우려하고 있습니다. 현실적이고 비판적인 관점에서 문제점을 지적하세요."
}

# --- 토론 진행 ---

def run_debate():
    """두 AI 페르소나 간의 토론을 진행합니다."""
    
    print(f"토론 주제: {DEBATE_TOPIC}\n")
    
    # 토론의 전체 대화 내용을 저장할 리스트
    conversation_history = []
    
    # 첫 번째 주자는 페르소나 1
    current_speaker_name = "AI 지지자"
    current_speaker_prompt = persona_1_system_prompt
    
    # 첫 발언을 위한 초기 메시지
    initial_message = {
        "role": "user",
        "content": "'" + DEBATE_TOPIC + "'에 대한 당신의 입장을 밝혀주세요. 토론을 시작하겠습니다."
    }
    conversation_history.append(initial_message)

    for i in range(DEBATE_ROUNDS * 2):
        # 현재 발언자의 시스템 프롬프트를 대화 기록 맨 앞에 추가
        messages_for_api = [current_speaker_prompt] + conversation_history

        print(f"--- {current_speaker_name}의 발언 ---")

        try:
            response = client.chat.completions.create(
                model=os.getenv("OLLAMA_MODEL"),
                messages=messages_for_api,
                stream=False,
            )
            
            ai_response = response.choices[0].message.content
            print(ai_response)
            print("\n")
            
            # AI의 답변을 대화 기록에 추가
            conversation_history.append({"role": "assistant", "content": ai_response})
            
            # 다음 발언자 설정
            if current_speaker_name == "AI 지지자":
                current_speaker_name = "AI 비평가"
                current_speaker_prompt = persona_2_system_prompt
                # 다음 AI에게 이전 발언을 전달하며 역할을 부여
                conversation_history.append({"role": "user", "content": "위 주장에 대해 당신의 비판적인 견해를 제시해주세요."})
            else:
                current_speaker_name = "AI 지지자"
                current_speaker_prompt = persona_1_system_prompt
                conversation_history.append({"role": "user", "content": "이러한 우려에 대해 당신의 긍정적인 반박 의견을 제시해주세요."})

        except Exception as e:
            print(f"API 호출 중 오류가 발생했습니다: {e}")
            break

if __name__ == "__main__":
    run_debate()
