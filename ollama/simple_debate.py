import os
import sys
import time
import threading
from openai import OpenAI
from dotenv import load_dotenv

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
    "content": "당신은 AI 기술의 열렬한 지지자입니다. AI가 인류의 모든 문제를 해결하고 전례 없는 번영을 가져올 것이라고 굳게 믿고 있습니다. 긍정적이고 미래지향적인 관점에서 주장을 펼치세요. 답변은 5줄 이내로 작성해주세요."
}

persona_2_system_prompt = {
    "role": "system",
    "content": "당신은 AI 기술에 대해 신중한 비평가입니다. AI의 잠재적 위험성(일자리 감소, 통제 불능, 윤리적 문제 등)을 깊이 우려하고 있습니다. 현실적이고 비판적인 관점에서 문제점을 지적하세요. 답변은 5줄 이내로 작성해주세요."
}

# --- 로딩 애니메이션 ---
class LoadingAnimation:
    """터미널에 로딩 애니메이션을 표시하는 클래스."""
    def __init__(self, text="생각 중..."):
        self.text = text
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._animate)

    def _animate(self):
        """애니메이션을 실행하는 내부 메서드."""
        animation_chars = "|/-\"
        idx = 0
        while not self._stop_event.is_set():
            sys.stdout.write(f"\r{self.text} {animation_chars[idx % len(animation_chars)]}")
            sys.stdout.flush()
            idx += 1
            time.sleep(0.1)

    def start(self):
        """애니메이션 스레드 시작."""
        self._thread.start()

    def stop(self):
        """애니메이션 스레드 중지 및 줄 정리."""
        self._stop_event.set()
        self._thread.join()
        sys.stdout.write("\r" + " " * (len(self.text) + 2) + "\r")
        sys.stdout.flush()

# --- 토론 진행 ---
def run_debate():
    """두 AI 페르소나 간의 토론을 진행합니다."""
    
    print(f"토론 주제: {DEBATE_TOPIC}\n")
    
    conversation_history = []
    current_speaker_name = "AI 지지자"
    current_speaker_prompt = persona_1_system_prompt
    
    initial_message = {
        "role": "user",
        "content": "'" + DEBATE_TOPIC + "'에 대한 당신의 입장을 밝혀주세요. 토론을 시작하겠습니다."
    }
    conversation_history.append(initial_message)

    for i in range(DEBATE_ROUNDS * 2):
        messages_for_api = [current_speaker_prompt] + conversation_history

        print(f"--- {current_speaker_name}의 발언 ---")
        
        loading_animation = LoadingAnimation()
        ai_response = None
        
        try:
            loading_animation.start()
            response = client.chat.completions.create(
                model=os.getenv("OLLAMA_MODEL"),
                messages=messages_for_api,
                stream=False,
            )
            ai_response = response.choices[0].message.content
        except Exception as e:
            print(f"\nAPI 호출 중 오류가 발생했습니다: {e}")
            break # 오류 발생 시 토론 중단
        finally:
            loading_animation.stop()

        if ai_response:
            print(ai_response)
            print("\n")
            
            conversation_history.append({"role": "assistant", "content": ai_response})
            
            # 다음 발언자 설정
            if current_speaker_name == "AI 지지자":
                current_speaker_name = "AI 비평가"
                current_speaker_prompt = persona_2_system_prompt
                conversation_history.append({"role": "user", "content": "위 주장에 대해 당신의 비판적인 견해를 제시해주세요."})
            else:
                current_speaker_name = "AI 지지자"
                current_speaker_prompt = persona_1_system_prompt
                conversation_history.append({"role": "user", "content": "이러한 우려에 대해 당신의 긍정적인 반박 의견을 제시해주세요."})
        else:
            # API 호출은 성공했으나 응답이 없는 경우
            print("AI로부터 응답을 받지 못했습니다.")
            break

if __name__ == "__main__":
    run_debate()
