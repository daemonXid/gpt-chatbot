import os
from openai import OpenAI
from dotenv import load_dotenv

def stream_debate(topic: str, persona1: str, persona2: str):
    """
    주어진 주제와 페르소나로 AI 토론을 실행하고, 
    대화의 각 부분을 간단한 HTML 태그가 포함된 문자열로 생성(yield)합니다.
    """
    # .env 로드 및 클라이언트 설정
    load_dotenv(override=True)
    client = OpenAI(
        base_url=os.getenv("OLLAMA_BASE_URL"),
        api_key="ollama",
    )

    # --- 토론 설정 ---
    debate_rounds = 3
    model = os.getenv("OLLAMA_MODEL")

    # 파라미터로 받은 페르소나 설정
    persona_1_system_prompt = {"role": "system", "content": persona1}
    persona_2_system_prompt = {"role": "system", "content": persona2}

    yield f"<h2>토론 주제: {topic}</h2>"

    conversation_history = []
    # 첫 발언자는 페르소나 1 (찬성 측)으로 고정
    current_speaker_name = "찬성 측"
    current_speaker_prompt = persona_1_system_prompt
    
    initial_message = {
        "role": "user",
        "content": f"'{topic}'에 대한 당신의 입장을 밝혀주세요. 토론을 시작하겠습니다."
    }
    conversation_history.append(initial_message)

    for i in range(debate_rounds * 2):
        messages_for_api = [current_speaker_prompt] + conversation_history

        yield f"<h3>--- {current_speaker_name}의 발언 ---</h3>"
        
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages_for_api,
                stream=False,
            )
            ai_response = response.choices[0].message.content
            
            yield f"<p>{ai_response.replace('\n', '<br>')}</p>"

            conversation_history.append({"role": "assistant", "content": ai_response})
            
            # 다음 발언자 설정
            if current_speaker_name == "찬성 측":
                current_speaker_name = "반대 측"
                current_speaker_prompt = persona_2_system_prompt
                conversation_history.append({"role": "user", "content": "위 주장에 대해 당신의 비판적인 견해를 제시해주세요."})
            else:
                current_speaker_name = "찬성 측"
                current_speaker_prompt = persona_1_system_prompt
                conversation_history.append({"role": "user", "content": "이러한 우려에 대해 당신의 긍정적인 반박 의견을 제시해주세요."})

        except Exception as e:
            yield f"<p style='color: red;'>API 호출 중 오류가 발생했습니다: {e}</p>"
            break
    
    yield "<h3>--- 토론 종료 ---</h3>"