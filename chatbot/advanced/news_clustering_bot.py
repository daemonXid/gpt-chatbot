"""
뉴스 기사 그룹화 챗봇 - Embeddings API 활용

이 봇이 할 수 있는 일:
1. 비슷한 주제의 뉴스 기사들을 자동으로 그룹화
2. 대량의 뉴스 데이터를 의미 있는 클러스터로 분류
3. 중복되는 뉴스나 유사한 보도를 식별
4. 뉴스 트렌드 분석 및 주요 이슈 파악
5. 개인화된 뉴스 추천 시스템 구축

사용하는 API:
- Embeddings API: 뉴스 기사를 벡터로 변환하여 의미적 유사성 계산
- Chat Completions API: 클러스터 분석 및 요약 생성

활용 시나리오:
- 뉴스 포털의 자동 기사 분류
- 소셜 미디어 모니터링 및 트렌드 분석
- 언론사의 중복 보도 방지
- 뉴스 큐레이션 서비스
- 미디어 분석 및 여론 조사
- 가짜뉴스 탐지 시스템

분석 기능:
- K-means 클러스터링으로 기사 그룹화
- 코사인 유사도를 통한 기사 간 관련성 측정
- 클러스터별 대표 기사 선정
- 주요 키워드 및 토픽 추출
"""

import os
from openai import OpenAI
import numpy as np
from dotenv import load_dotenv
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import json
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# .env 파일에서 환경변수를 로드합니다
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

class NewsClusterer:
    def __init__(self):
        self.news_articles = []  # 뉴스 기사 저장
        self.embeddings = []     # 임베딩 벡터 저장
        self.clusters = {}       # 클러스터 결과 저장

    def get_embedding(self, text):
        """
        텍스트를 임베딩 벡터로 변환하는 함수
        Embeddings API를 사용하여 뉴스 기사의 의미를 수치화합니다
        """
        try:
            # 텍스트 전처리 (줄바꿈 제거, 길이 제한)
            text = text.replace('\n', ' ').strip()
            if len(text) > 8000:  # API 제한을 고려한 길이 제한
                text = text[:8000]

            # OpenAI Embeddings API 호출
            response = client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )

            return response['data'][0]['embedding']

        except Exception as e:
            print(f"임베딩 생성 중 오류 발생: {e}")
            return None

    def add_news_article(self, title, content, source="", date=""):
        """
        뉴스 기사를 추가하는 함수
        """
        # 제목과 내용을 합쳐서 전체 텍스트 생성
        full_text = f"{title}. {content}"

        # 임베딩 생성
        print(f"기사 임베딩 생성 중: {title[:50]}...")
        embedding = self.get_embedding(full_text)

        if embedding:
            article_data = {
                'id': len(self.news_articles),
                'title': title,
                'content': content,
                'source': source,
                'date': date,
                'full_text': full_text
            }

            self.news_articles.append(article_data)
            self.embeddings.append(embedding)
            return True
        else:
            print(f"기사 추가 실패: {title}")
            return False

    def cluster_news(self, num_clusters=None):
        """
        뉴스 기사들을 클러스터링하는 함수
        """
        if len(self.news_articles) < 2:
            print("클러스터링을 위해 최소 2개의 기사가 필요합니다.")
            return False

        # 자동으로 클러스터 수 결정 (지정되지 않은 경우)
        if num_clusters is None:
            num_clusters = min(5, max(2, len(self.news_articles) // 3))

        print(f"{len(self.news_articles)}개 기사를 {num_clusters}개 그룹으로 클러스터링 중...")

        try:
            # K-means 클러스터링 실행
            kmeans = KMeans(n_clusters=num_clusters, random_state=42)
            cluster_labels = kmeans.fit_predict(self.embeddings)

            # 클러스터 결과 저장
            self.clusters = {}
            for i, label in enumerate(cluster_labels):
                if label not in self.clusters:
                    self.clusters[label] = []
                self.clusters[label].append(self.news_articles[i])

            return True

        except Exception as e:
            print(f"클러스터링 중 오류 발생: {e}")
            return False

    def find_similar_articles(self, target_article_id, threshold=0.7):
        """
        특정 기사와 유사한 기사들을 찾는 함수
        """
        if target_article_id >= len(self.news_articles):
            return []

        target_embedding = self.embeddings[target_article_id]
        similar_articles = []

        for i, embedding in enumerate(self.embeddings):
            if i != target_article_id:
                similarity = cosine_similarity([target_embedding], [embedding])[0][0]
                if similarity >= threshold:
                    article = self.news_articles[i].copy()
                    article['similarity'] = similarity
                    similar_articles.append(article)

        # 유사도 순으로 정렬
        similar_articles.sort(key=lambda x: x['similarity'], reverse=True)
        return similar_articles

    def analyze_cluster(self, cluster_id):
        """
        Chat Completions API를 사용하여 클러스터를 분석하는 함수
        """
        if cluster_id not in self.clusters:
            return "존재하지 않는 클러스터입니다."

        articles = self.clusters[cluster_id]

        # 클러스터의 모든 기사 제목과 내용 요약
        cluster_text = "\n".join([
            f"제목: {article['title']}\n내용 요약: {article['content'][:200]}..."
            for article in articles
        ])

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """당신은 뉴스 분석 전문가입니다.
                        주어진 뉴스 기사 그룹을 분석하여 다음을 제공해주세요:
                        1. 공통 주제 및 핵심 키워드
                        2. 주요 이슈나 논점
                        3. 이 그룹의 뉴스들이 다루는 전반적인 내용
                        4. 트렌드나 패턴 분석
                        한국어로 명확하게 작성해주세요."""
                    },
                    {
                        "role": "user",
                        "content": f"다음 뉴스 기사들을 분석해주세요:\n\n{cluster_text}"
                    }
                ],
                max_tokens=400,
                temperature=0.5
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"클러스터 분석 중 오류 발생: {e}"

    def get_cluster_summary(self):
        """
        전체 클러스터링 결과 요약
        """
        if not self.clusters:
            return "클러스터링이 수행되지 않았습니다."

        summary = f"=== 뉴스 클러스터링 결과 ===\n"
        summary += f"총 기사 수: {len(self.news_articles)}\n"
        summary += f"클러스터 수: {len(self.clusters)}\n\n"

        for cluster_id, articles in self.clusters.items():
            summary += f"📰 클러스터 {cluster_id + 1} ({len(articles)}개 기사)\n"
            summary += "대표 기사들:\n"

            # 각 클러스터의 처음 3개 기사만 표시
            for i, article in enumerate(articles[:3]):
                summary += f"  {i+1}. {article['title']}\n"

            if len(articles) > 3:
                summary += f"  ... 외 {len(articles) - 3}개 기사\n"
            summary += "\n"

        return summary

def main():
    """
    메인 함수 - 뉴스 클러스터링 봇 실행
    """
    print("=== 뉴스 기사 그룹화 봇 ===")
    print("비슷한 주제의 뉴스 기사들을 자동으로 그룹화해드립니다.")
    print("여러 개의 뉴스 기사를 입력한 후 클러스터링을 수행합니다.\n")

    clusterer = NewsClusterer()

    # 뉴스 기사 입력받기
    print("뉴스 기사들을 입력해주세요.")
    print("각 기사마다 제목과 내용을 입력하고, 'done'을 입력하면 클러스터링을 시작합니다.")
    print("'quit'를 입력하면 종료됩니다.\n")

    article_count = 1
    while True:
        print(f"--- 기사 {article_count} ---")
        title = input("뉴스 제목: ")

        if title.lower() == 'quit':
            print("뉴스 클러스터링 봇을 종료합니다.")
            return
        elif title.lower() == 'done':
            break

        content = input("뉴스 내용 (요약): ")

        if content.lower() == 'quit':
            print("뉴스 클러스터링 봇을 종료합니다.")
            return

        source = input("뉴스 출처 (선택사항): ")

        # 기사 추가
        success = clusterer.add_news_article(title, content, source)
        if success:
            print(f"✅ 기사 {article_count} 추가 완료\n")
            article_count += 1
        else:
            print("❌ 기사 추가 실패\n")

    if len(clusterer.news_articles) < 2:
        print("클러스터링을 위해 최소 2개의 기사가 필요합니다.")
        return

    # 클러스터 수 설정
    num_clusters = input(f"\n클러스터 수를 입력하세요 (기본값: 자동, 현재 기사 수: {len(clusterer.news_articles)}): ")
    if num_clusters.isdigit():
        num_clusters = int(num_clusters)
    else:
        num_clusters = None

    # 클러스터링 실행
    print("\n" + "="*60)
    success = clusterer.cluster_news(num_clusters)

    if success:
        print("🎯 클러스터링 완료!")
        print("="*60)

        # 결과 요약 출력
        summary = clusterer.get_cluster_summary()
        print(summary)

        # 상세 분석 옵션
        while True:
            print("\n추가 분석 옵션:")
            print("1. 특정 클러스터 상세 분석")
            print("2. 유사 기사 찾기")
            print("3. 결과 저장")
            print("4. 메뉴로 돌아가기")

            choice = input("선택하세요 (1-4): ")

            if choice == "1":
                cluster_id = input(f"분석할 클러스터 번호 (1-{len(clusterer.clusters)}): ")
                if cluster_id.isdigit():
                    cluster_id = int(cluster_id) - 1
                    if cluster_id in clusterer.clusters:
                        print(f"\n📊 클러스터 {cluster_id + 1} 분석 결과:")
                        print("-" * 40)
                        analysis = clusterer.analyze_cluster(cluster_id)
                        print(analysis)
                    else:
                        print("존재하지 않는 클러스터 번호입니다.")
                else:
                    print("올바른 숫자를 입력해주세요.")

            elif choice == "2":
                print("\n기사 목록:")
                for i, article in enumerate(clusterer.news_articles):
                    print(f"{i+1}. {article['title']}")

                article_id = input("기준 기사 번호: ")
                if article_id.isdigit():
                    article_id = int(article_id) - 1
                    if 0 <= article_id < len(clusterer.news_articles):
                        similar = clusterer.find_similar_articles(article_id, 0.7)
                        print(f"\n🔍 '{clusterer.news_articles[article_id]['title']}'와 유사한 기사들:")
                        print("-" * 50)
                        if similar:
                            for article in similar:
                                print(f"• {article['title']} (유사도: {article['similarity']:.3f})")
                        else:
                            print("유사한 기사가 없습니다.")
                    else:
                        print("올바른 기사 번호를 입력해주세요.")

            elif choice == "3":
                filename = f"news_clustering_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(clusterer.get_cluster_summary())
                        f.write("\n" + "="*60 + "\n")
                        for cluster_id in clusterer.clusters:
                            f.write(f"\n클러스터 {cluster_id + 1} 상세 분석:\n")
                            f.write("-" * 30 + "\n")
                            analysis = clusterer.analyze_cluster(cluster_id)
                            f.write(analysis)
                            f.write("\n")
                    print(f"✅ 결과가 저장되었습니다: {filename}")
                except Exception as e:
                    print(f"❌ 저장 실패: {e}")

            elif choice == "4":
                break
            else:
                print("올바른 선택을 해주세요.")

    else:
        print("❌ 클러스터링에 실패했습니다.")

def demo_mode():
    """
    샘플 뉴스로 데모 실행
    """
    print("\n=== 데모 모드 ===")
    print("샘플 뉴스 기사로 클러스터링을 시연합니다.\n")

    clusterer = NewsClusterer()

    # 샘플 뉴스 기사들
    sample_news = [
        {
            'title': "AI 기술 발전으로 자율주행차 상용화 가속화",
            'content': "인공지능 기술의 급속한 발전으로 자율주행 자동차의 상용화가 예상보다 빨라질 전망이다. 테슬라와 구글을 비롯한 주요 기업들이 완전 자율주행 기술 개발에 박차를 가하고 있다.",
            'source': "테크뉴스"
        },
        {
            'title': "전기차 배터리 기술 혁신, 충전 시간 대폭 단축",
            'content': "새로운 배터리 기술로 전기차 충전 시간이 기존의 절반 이하로 단축될 예정이다. 이는 전기차 대중화에 큰 도움이 될 것으로 기대된다.",
            'source': "모빌리티뉴스"
        },
        {
            'title': "코로나19 신규 확진자 수 증가세 둔화",
            'content': "최근 일주일간 코로나19 신규 확진자 수가 전주 대비 감소하며 증가세가 둔화되고 있는 것으로 나타났다. 방역당국은 지속적인 관찰이 필요하다고 밝혔다.",
            'source': "헬스뉴스"
        },
        {
            'title': "새로운 변이바이러스 출현, 백신 효과성 검토 필요",
            'content': "새로운 코로나19 변이바이러스가 발견되면서 기존 백신의 효과성에 대한 재검토가 필요한 상황이다. 전문가들은 추가 연구가 필요하다고 강조했다.",
            'source': "메디컬뉴스"
        },
        {
            'title': "메타버스 플랫폼 이용자 수 급증",
            'content': "가상현실 기반 메타버스 플랫폼 이용자가 전년 대비 300% 증가했다. 특히 젊은 세대를 중심으로 가상공간에서의 소셜 활동이 활발해지고 있다.",
            'source': "IT뉴스"
        }
    ]

    print("샘플 뉴스 기사를 추가하는 중...")
    for news in sample_news:
        success = clusterer.add_news_article(
            news['title'],
            news['content'],
            news['source']
        )

    print(f"\n{len(sample_news)}개 샘플 기사 추가 완료!")

    # 클러스터링 실행
    print("클러스터링을 실행합니다...")
    success = clusterer.cluster_news(3)

    if success:
        print("\n" + "="*60)
        print("📊 데모 클러스터링 결과")
        print("="*60)
        summary = clusterer.get_cluster_summary()
        print(summary)

        # 각 클러스터 분석
        for cluster_id in clusterer.clusters:
            print(f"\n🔍 클러스터 {cluster_id + 1} 분석:")
            print("-" * 30)
            analysis = clusterer.analyze_cluster(cluster_id)
            print(analysis)
    else:
        print("데모 클러스터링에 실패했습니다.")

if __name__ == "__main__":
    while True:
        print("\n📰 뉴스 기사 그룹화 봇 메뉴")
        print("1. 직접 뉴스 입력하여 클러스터링")
        print("2. 샘플 뉴스로 데모 실행")
        print("3. 종료")

        choice = input("선택하세요 (1-3): ")

        if choice == "1":
            main()
        elif choice == "2":
            demo_mode()
        elif choice == "3":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 1, 2, 3 중에서 선택해주세요.")