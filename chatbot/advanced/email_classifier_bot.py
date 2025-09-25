"""
고객 문의 이메일 분류 챗봇 - Embeddings API 활용

이 봇이 할 수 있는 일:
1. 고객 문의 이메일을 주제별로 자동 분류
2. 대량의 이메일을 효율적으로 처리
3. 유사한 문의들을 그룹화하여 관리
4. 새로운 이메일이 어떤 카테고리에 속하는지 예측
5. 고객 서비스팀의 업무 효율성 향상

사용하는 API:
- Embeddings API: 텍스트를 벡터로 변환하여 의미적 유사성 계산
- Chat Completions API: 최종 분류 결과 해석 및 설명

활용 시나리오:
- 전자상거래 사이트의 고객 문의 자동 분류
- 헬프데스크 티켓 우선순위 결정
- 고객 서비스 담당자 배정
- FAQ 자동 추천 시스템
"""

import os
from openai import OpenAI
import numpy as np
from dotenv import load_dotenv
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import json

# .env 파일에서 환경변수를 로드합니다
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

class EmailClassifier:
    def __init__(self):
        # 미리 정의된 이메일 카테고리
        self.categories = [
            "배송 문의",
            "반품/교환",
            "결제 문제",
            "제품 문의",
            "기술 지원",
            "계정 문제",
            "일반 문의"
        ]

        # 카테고리별 샘플 텍스트 (학습용)
        self.category_samples = {
            "배송 문의": "언제 배송되나요? 배송 조회 추적 번호",
            "반품/교환": "제품을 반품하고 싶어요 교환 환불",
            "결제 문제": "결제가 안 되요 카드 오류 결제 실패",
            "제품 문의": "제품 사양 크기 색상 재고",
            "기술 지원": "앱이 작동하지 않아요 오류 버그",
            "계정 문제": "로그인이 안 되요 비밀번호 찾기",
            "일반 문의": "매장 위치 영업시간 연락처"
        }

    def get_embedding(self, text):
        """
        텍스트를 임베딩 벡터로 변환하는 함수
        Embeddings API를 사용하여 텍스트의 의미를 수치화합니다
        """
        try:
            # OpenAI Embeddings API 호출
            response = client.embeddings.create(
                model="text-embedding-ada-002",  # 임베딩 모델 지정
                input=text.replace("\n", " ")  # 개행 문자 제거
            )

            # 임베딩 벡터 반환
            return response['data'][0]['embedding']

        except Exception as e:
            print(f"임베딩 생성 중 오류 발생: {e}")
            return None

    def classify_email(self, email_text):
        """
        이메일 텍스트를 분류하는 함수
        """
        print("이메일을 분석 중입니다...")

        # 입력 이메일의 임베딩 생성
        email_embedding = self.get_embedding(email_text)
        if email_embedding is None:
            return None

        # 각 카테고리와의 유사도 계산
        similarities = {}

        for category, sample_text in self.category_samples.items():
            # 카테고리 샘플의 임베딩 생성
            category_embedding = self.get_embedding(sample_text)
            if category_embedding is None:
                continue

            # 코사인 유사도 계산
            similarity = cosine_similarity(
                [email_embedding],
                [category_embedding]
            )[0][0]

            similarities[category] = similarity

        # 가장 유사한 카테고리 찾기
        best_category = max(similarities, key=similarities.get)
        confidence = similarities[best_category]

        return {
            'category': best_category,
            'confidence': confidence,
            'all_scores': similarities
        }

    def explain_classification(self, email_text, classification_result):
        """
        Chat Completions API를 사용하여 분류 결과를 설명하는 함수
        """
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """당신은 고객 서비스 전문가입니다.
                        이메일 분류 결과를 바탕으로 다음을 설명해주세요:
                        1. 왜 이 카테고리로 분류되었는지
                        2. 어떤 키워드나 내용이 결정적이었는지
                        3. 이 문의에 대한 대응 방안 제안"""
                    },
                    {
                        "role": "user",
                        "content": f"""
                        이메일 내용: {email_text}
                        분류 결과: {classification_result['category']}
                        신뢰도: {classification_result['confidence']:.2f}

                        이 분류 결과에 대해 설명해주세요.
                        """
                    }
                ],
                max_tokens=300,
                temperature=0.5
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"설명 생성 중 오류 발생: {e}"

def main():
    """
    메인 함수 - 이메일 분류 봇 실행
    """
    print("=== 고객 문의 이메일 분류 봇 ===")
    print("이메일 내용을 입력하면 자동으로 카테고리를 분류해드립니다.")
    print("'quit'를 입력하면 종료됩니다.\n")

    classifier = EmailClassifier()

    # 사용자로부터 이메일 내용 입력받기
    email_text = input("분류할 이메일 내용을 입력하세요: ")

    if email_text.lower() == 'quit':
        print("이메일 분류 봇을 종료합니다.")
        return

    # 이메일 분류 실행
    result = classifier.classify_email(email_text)

    if result:
        print("\n" + "="*50)
        print("📧 이메일 분류 결과")
        print("="*50)
        print(f"카테고리: {result['category']}")
        print(f"신뢰도: {result['confidence']:.2f} ({result['confidence']*100:.1f}%)")
        print("\n📊 전체 카테고리별 유사도:")

        # 유사도 순으로 정렬하여 표시
        sorted_scores = sorted(result['all_scores'].items(),
                             key=lambda x: x[1], reverse=True)

        for category, score in sorted_scores:
            bar_length = int(score * 20)  # 0-1을 0-20 길이로 변환
            bar = "█" * bar_length + "░" * (20 - bar_length)
            print(f"{category:12} | {bar} | {score:.3f}")

        print("\n🤖 AI 분석 설명:")
        print("-" * 50)
        explanation = classifier.explain_classification(email_text, result)
        print(explanation)
        print("="*50)
    else:
        print("이메일 분류에 실패했습니다.")

def batch_classify_demo():
    """
    여러 이메일을 한번에 분류하는 데모 함수
    """
    print("\n=== 일괄 분류 데모 ===")

    # 샘플 이메일들
    sample_emails = [
        "주문한 상품이 언제 도착하나요? 배송 조회 방법을 알려주세요.",
        "앱이 계속 튕겨요. 로그인도 안 되고 오류가 발생해요.",
        "구매한 제품이 마음에 들지 않아서 반품하고 싶습니다.",
        "결제가 실패했는데 돈은 빠져나갔어요. 어떻게 해야 하나요?",
        "이 제품의 상세한 사양과 크기를 알려주세요."
    ]

    classifier = EmailClassifier()

    print("샘플 이메일들을 분류해보겠습니다...\n")

    for i, email in enumerate(sample_emails, 1):
        print(f"📧 이메일 {i}:")
        print(f"내용: {email}")

        result = classifier.classify_email(email)
        if result:
            print(f"분류: {result['category']} (신뢰도: {result['confidence']:.2f})")
        print("-" * 40)

if __name__ == "__main__":
    while True:
        print("\n📋 이메일 분류 봇 메뉴")
        print("1. 단일 이메일 분류")
        print("2. 일괄 분류 데모")
        print("3. 종료")

        choice = input("선택하세요 (1-3): ")

        if choice == "1":
            main()
        elif choice == "2":
            batch_classify_demo()
        elif choice == "3":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 1, 2, 3 중에서 선택해주세요.")