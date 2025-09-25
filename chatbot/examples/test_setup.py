import os  # os 모듈을 임포트합니다.
from dotenv import load_dotenv  # python-dotenv 패키지에서 load_dotenv 함수를 임포트합니다.

load_dotenv() # .env 파일의 환경 변수를 로드합니다.

api_key = os.getenv("OPENAI_API_KEY") # 환경 변수에서 API 키를 가져옵니다.

if api_key :
    print("API Key loaded successfully // : " , api_key) # API 키가 제대로 로드되었는지 확인합니다.
else:
    print("Failed to load API Key.") # API 키가 로드되지 않았을 때의 메시지입니다.




