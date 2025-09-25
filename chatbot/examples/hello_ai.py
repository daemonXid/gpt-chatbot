from openai import OpenAI                               # openai 패키지에서 OpenAI 클래스를 임포트합니다.
import os                                               # os 모듈을 임포트합니다.
from dotenv import load_dotenv                          # python-dotenv 패키지에서 load_dotenv 함수를 임포트합니다.

load_dotenv()                                           # .env 파일의 환경 변수를 로드합니다.

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))    # OpenAI 클라이언트를 생성합니다.
 
response = client.chat.completions.create(              # 채팅 완료를 생성합니다.
    model="gpt-4o-mini",                                # 사용할 모델을 지정합니다.
    messages=[                                          # 메시지 목록을 지정합니다.
        {"role": "system", "content": "너는 부처님으로서 학생의 질문에 개념적이고 고수준의 응답을 한다"},  # 시스템 메시지로 역할과 행동 지침을 설정합니다.
        {"role": "user", "content": "1+1은?  "},  # 사용자 메시지로 질문을 설정합니다.
        
    ]
)  

print(response.choices[0].message.content)                  # AI의 응답을 출력합니다.



# # 응답 객체 자세히 보기
# print("전체 응답 구조:")                                    # 전체 응답 구조를 출력합니다.
# print(f"모델: {response.model}")                            # 사용된 모델을 출력합니다.        
# print(f"토큰 사용량: {response.usage.total_tokens}")        # 사용된 토큰 수를 출력합니다.
# print(f"응답 내용: {response.choices[0].message.content}")  # AI의 응답을 출력합니다.


