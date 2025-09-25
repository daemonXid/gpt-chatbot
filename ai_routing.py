import sys

def analyze_question(question: str) -> str:
    """
    사용자의 질문을 분석하여 '심플' 또는 '고급'으로 분류합니다.

    Args:
        question: 사용자의 질문 문자열

    Returns:
        '심플' 또는 '고급' 문자열
    """
    # '고급' 질문으로 판단할 키워드 목록
    advanced_keywords = [
        "자세히",
        "심층",
        "분석",
        "비교",
        "장단점",
        "원리",
        "구체적으로",
        "상세하게",
        "차이점",
        "이유",
        "방법",
        "예시",
        "설명",
        "정의",
        "핵심",
    ]

    # 질문에 고급 키워드가 포함되어 있는지 확인
    if any(keyword in question for keyword in advanced_keywords):
        return "고급"
    
    return "심플"

def main():
    """
    프로그램의 메인 진입점입니다.
    명령줄 인자로 질문을 받아 분석하고 결과를 출력합니다.
    """
    # 명령줄에서 사용자 질문을 가져옵니다.
    user_question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""

    result = analyze_question(user_question)
    print(f"<{result}>")

if __name__ == "__main__":
    main()