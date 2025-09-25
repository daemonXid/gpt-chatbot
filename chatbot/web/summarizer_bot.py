import os
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일에서 환경변수를 로드합니다
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

def text_summarizer():
    """
    텍스트 요약 봇
    긴 텍스트를 입력받아 핵심 내용을 요약해줍니다
    """
    print("=== 텍스트 요약 봇 ===")
    print("요약할 텍스트를 직접 입력해주세요.")
    print("'quit'를 입력하면 종료됩니다.\n")

    # 요약할 텍스트 입력받기
    text_to_summarize = input("요약할 텍스트를 입력하세요: ")

    # 종료 조건 확인
    if text_to_summarize.lower() == 'quit':
        print("요약 봇을 종료합니다.")
        return

    # 입력된 텍스트가 없으면 종료
    if not text_to_summarize.strip():
        print("텍스트가 입력되지 않았습니다.")
        return

    # 요약 길이 선택
    print("\n요약 길이를 선택하세요:")
    print("1. 짧게 (1-2문장)")
    print("2. 보통 (3-5문장)")
    print("3. 자세히 (6-10문장)")

    choice = input("선택 (1-3): ")

        # 요약 길이에 따른 설정
        if choice == "1":
            summary_type = "매우 간단하게 1-2문장으로"
            max_tokens = 100
        elif choice == "2":
            summary_type = "적당히 3-5문장으로"
            max_tokens = 200
        elif choice == "3":
            summary_type = "자세히 6-10문장으로"
            max_tokens = 300
        else:
            summary_type = "적당히 3-5문장으로"
            max_tokens = 200

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        # system role: 요약 전문가 역할 정의
                        "role": "system",
                        "content": f"""당신은 텍스트 요약 전문가입니다.
                        주어진 텍스트의 핵심 내용을 {summary_type} 요약해주세요.
                        중요한 정보는 빠뜨리지 말고, 불필요한 세부사항은 제거해주세요.
                        한국어로 명확하고 이해하기 쉽게 작성해주세요."""
                    },
                    {
                        # user role: 요약할 텍스트 제공
                        "role": "user",
                        "content": f"다음 텍스트를 요약해주세요:\n\n{text_to_summarize}"
                    }
                ],
                max_tokens=max_tokens,
                temperature=0.5  # 중간 정도의 창의성으로 자연스러운 요약
            )

            summary = response.choices[0].message.content

            print("\n" + "="*50)
            print("📝 요약 결과")
            print("="*50)
            print(summary)
            print("="*50 + "\n")

        except Exception as e:
            print(f"요약 중 오류가 발생했습니다: {e}")

def file_summarizer():
    """
    파일 내용을 읽어서 요약하는 기능
    """
    print("\n=== 파일 요약 모드 ===")
    file_path = input("요약할 텍스트 파일 경로를 입력하세요: ")

    try:
        # 파일 읽기 (UTF-8 인코딩)
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        if not file_content.strip():
            print("파일이 비어있습니다.")
            return

        print(f"파일 내용 ({len(file_content)} 글자)을 읽었습니다.")

        # 텍스트가 너무 긴 경우 처리
        if len(file_content) > 3000:
            print("⚠️  텍스트가 매우 깁니다. 처음 3000자만 요약합니다.")
            file_content = file_content[:3000]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """당신은 문서 요약 전문가입니다.
                    파일의 내용을 읽고 다음과 같이 구조화된 요약을 제공해주세요:

                    1. 주제/제목
                    2. 핵심 내용 (3-5개 bullet point)
                    3. 결론 또는 중요한 시사점

                    한국어로 명확하게 작성해주세요."""
                },
                {
                    "role": "user",
                    "content": f"다음 파일 내용을 요약해주세요:\n\n{file_content}"
                }
            ],
            max_tokens=400,
            temperature=0.5
        )

        summary = response.choices[0].message.content

        print(f"\n📄 파일 요약 결과: {file_path}")
        print("="*60)
        print(summary)
        print("="*60)

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다. 경로를 확인해주세요.")
    except Exception as e:
        print(f"파일 요약 중 오류가 발생했습니다: {e}")

def url_summarizer():
    """
    웹페이지 URL 내용을 요약하는 기능 (개념적 예시)
    실제로는 웹 스크래핑 라이브러리가 필요합니다
    """
    print("\n=== URL 요약 모드 (개념적 예시) ===")
    print("실제 구현을 위해서는 requests, beautifulsoup4 등의 라이브러리가 필요합니다.")

    url = input("요약할 웹페이지 URL을 입력하세요: ")

    # 실제 구현 예시 코드 (주석 처리)
    """
    import requests
    from bs4 import BeautifulSoup

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
        # 텍스트 정리 및 요약 로직...
    except:
        print("웹페이지를 가져올 수 없습니다.")
    """

    print(f"URL: {url}")
    print("웹 스크래핑 기능은 별도의 라이브러리 설치가 필요합니다.")

if __name__ == "__main__":
    while True:
        print("\n📋 요약 봇 메뉴")
        print("1. 텍스트 직접 입력 요약")
        print("2. 파일 내용 요약")
        print("3. URL 내용 요약 (예시)")
        print("4. 종료")

        choice = input("선택하세요 (1-4): ")

        if choice == "1":
            text_summarizer()
        elif choice == "2":
            file_summarizer()
        elif choice == "3":
            url_summarizer()
        elif choice == "4":
            print("요약 봇을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 1, 2, 3, 4 중에서 선택해주세요.")