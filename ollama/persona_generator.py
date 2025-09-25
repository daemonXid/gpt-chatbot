import os
import json
from openai import OpenAI
from dotenv import load_dotenv

def generate_personas(topic: str) -> dict:
    """
    주어진 토론 주제에 대해 LLM을 사용하여 두 개의 대립하는 페르소나를 생성합니다.

    Args:
        topic: 토론 주제.

    Returns:
        'persona1'과 'persona2' 설명을 포함하는 사전 또는 오류 메시지.
    """
    load_dotenv(override=True)
    
    try:
        client = OpenAI(
            base_url=os.getenv("OLLAMA_BASE_URL"),
            api_key="ollama",
        )
        model = os.getenv("OLLAMA_MODEL")

        system_prompt = """
        당신은 토론의 사회자이자 작가입니다. 주어진 토론 주제에 대해, 두 명의 대립하는 페르소나를 생성하는 역할을 합니다.
        각 페르소나는 명확한 찬성 또는 반대 입장을 가져야 합니다.
        결과는 반드시 다음 JSON 형식으로만 제공해야 합니다. 다른 설명은 일절 포함하지 마세요.

        {
          "persona1": "페르소나 1의 설명. (예: 당신은 [주제]의 열렬한 지지자입니다. ...)",
          "persona2": "페르소나 2의 설명. (예: 당신은 [주제]에 대해 신중한 비평가입니다. ...)"
        }
        """

        user_prompt = f"""
        토론 주제: "{topic}"

        위 주제에 대한 찬성 페르소나 1과 반대 페르소나 2를 생성해주세요.
        각 페르소나 설명의 마지막에는 "또한, 당신의 모든 답변은 반드시 5줄 이내로 간결하게 작성해야 합니다." 라는 문장을 반드시 포함시켜 주세요.
        """

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            response_format={"type": "json_object"}, # JSON 모드 사용
        )

        generated_text = response.choices[0].message.content
        personas = json.loads(generated_text)

        if "persona1" in personas and "persona2" in personas:
            return personas
        else:
            return {"error": "LLM이 유효한 페르소나를 생성하지 못했습니다."}

    except json.JSONDecodeError:
        return {"error": "LLM의 응답이 JSON 형식이 아닙니다.", "raw_response": generated_text}
    except Exception as e:
        return {"error": f"페르소나 생성 중 오류 발생: {str(e)}"}

if __name__ == '__main__':
    # 테스트용 코드
    test_topic = "소셜 미디어는 사회에 긍정적인 영향을 미치는가?"
    generated = generate_personas(test_topic)
    import pprint
    pprint.pprint(generated)
