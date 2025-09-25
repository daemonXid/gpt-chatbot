from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
# 클라이언트 구성: base_url을 Ollama 엔드포인트로, api_key는 dummy 값 사용
client = OpenAI(
    base_url=os.getenv("OLLAMA_BASE_URL"),
    api_key="ollama",  # 실제 인증은 Ollama 내부가 처리하므로 unused
)

response = client.chat.completions.create(
    model=os.getenv("OLLAMA_MODEL"),
    messages=[
        {"role": "system", "content": "너는 질문 내용에 따라서 고급인지 아닌지 판단하는 역할을 해. 고급인지 아닌지 판단하고 그 결과를 '고급' 또는 '심플'로 반환해."},
        {"role": "user", "content": "한국의 AI산업의 발전을 위해서 정부의 각 부처에서 준비하고 실행해야 할 내용을 정리해줘"},
    ],
)

print(response.choices[0].message.content)