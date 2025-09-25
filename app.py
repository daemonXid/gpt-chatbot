from flask import Flask, render_template, request, jsonify, session
import os
from openai import OpenAI
from dotenv import load_dotenv
import uuid

# .env 파일에서 환경변수를 로드합니다
load_dotenv()

# Flask 앱 초기화
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 세션을 위한 비밀 키

# OpenAI 클라이언트 초기화
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

@app.route('/')
def index():
    """메인 페이지 - 챗봇 목록"""
    return render_template('index.html')

@app.route('/chatbot/<bot_type>')
def chatbot_page(bot_type):
    """각 챗봇 페이지"""
    bot_configs = {
        'chat': {
            'title': '10줄 대화 챗봇',
            'description': '최대 10줄까지 자연스러운 대화를 나눌 수 있습니다.',
            'placeholder': '안녕하세요! 무엇이든 물어보세요.'
        },
        'translator': {
            'title': '번역 봇',
            'description': '다양한 언어로 텍스트를 번역해드립니다.',
            'placeholder': '번역할 텍스트를 입력하세요. 예: "안녕하세요" -> 영어'
        },
        'summarizer': {
            'title': '요약 봇',
            'description': '긴 텍스트를 핵심 내용으로 요약해드립니다.',
            'placeholder': '요약할 텍스트를 입력하세요.'
        },
        'question': {
            'title': '질문 생성 봇',
            'description': '주어진 주제로 다양한 질문을 생성합니다.',
            'placeholder': '질문을 생성할 주제나 텍스트를 입력하세요.'
        },
        'coding': {
            'title': '코딩 도우미 봇',
            'description': '프로그래밍 질문에 답하고 코드 도움을 제공합니다.',
            'placeholder': '프로그래밍 질문을 입력하세요.'
        },
        'diary': {
            'title': '일기 작성 봇',
            'description': '하루 경험을 바탕으로 아름다운 일기를 작성해줍니다.',
            'placeholder': '오늘 하루 있었던 일을 말해주세요.'
        }
    }

    config = bot_configs.get(bot_type, {
        'title': '챗봇',
        'description': '챗봇 서비스',
        'placeholder': '메시지를 입력하세요.'
    })

    return render_template('chatbot.html', bot_type=bot_type, config=config)

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """채팅 API 엔드포인트"""
    data = request.json
    bot_type = data.get('bot_type')
    message = data.get('message')

    # 세션에서 대화 내역 가져오기 (10줄 챗봇용)
    conversation_key = f'conversation_{bot_type}'
    if conversation_key not in session:
        session[conversation_key] = []

    try:
        if bot_type == 'chat':
            # 10줄 대화 챗봇
            conversation = session[conversation_key]

            # 10줄 제한 확인
            if len(conversation) >= 20:  # user + assistant = 2 * 10
                return jsonify({
                    'response': '10줄 대화가 완료되었습니다. 새로운 대화를 시작하려면 페이지를 새로고침하세요.',
                    'finished': True
                })

            # 사용자 메시지 추가
            conversation.append({"role": "user", "content": message})

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 친근하고 도움이 되는 한국어 대화 파트너입니다. 간단하고 명확하게 답변해주세요."}
                ] + conversation,
                max_tokens=150,
                temperature=0.7
            )

            ai_response = response.choices[0].message.content
            conversation.append({"role": "assistant", "content": ai_response})
            session[conversation_key] = conversation

            turn_count = len(conversation) // 2
            return jsonify({
                'response': ai_response,
                'turn_count': f"{turn_count}/10"
            })

        elif bot_type == 'translator':
            # 번역 봇
            # 메시지에서 텍스트와 목표 언어 추출 시도
            if '->' in message:
                parts = message.split('->')
                text_to_translate = parts[0].strip()
                target_language = parts[1].strip()
            else:
                text_to_translate = message
                target_language = "영어"  # 기본값

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"당신은 전문 번역가입니다. 주어진 텍스트를 {target_language}로 정확하게 번역해주세요. 번역 결과만 제공하고, 추가 설명은 하지 마세요."
                    },
                    {
                        "role": "user",
                        "content": f"다음 텍스트를 {target_language}로 번역해주세요: {text_to_translate}"
                    }
                ],
                max_tokens=200,
                temperature=0.3
            )

            return jsonify({'response': response.choices[0].message.content})

        elif bot_type == 'summarizer':
            # 요약 봇
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 텍스트 요약 전문가입니다. 주어진 텍스트의 핵심 내용을 3-5문장으로 요약해주세요. 중요한 정보는 빠뜨리지 말고, 불필요한 세부사항은 제거해주세요."
                    },
                    {
                        "role": "user",
                        "content": f"다음 텍스트를 요약해주세요: {message}"
                    }
                ],
                max_tokens=300,
                temperature=0.5
            )

            return jsonify({'response': response.choices[0].message.content})

        elif bot_type == 'question':
            # 질문 생성 봇
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 교육 전문가이자 질문 생성 전문가입니다. 주어진 텍스트나 주제를 바탕으로 이해도 확인, 토론 유도, 창의적 사고 등 다양한 목적의 질문을 5-7개 생성해주세요."
                    },
                    {
                        "role": "user",
                        "content": f"다음 내용을 바탕으로 다양한 질문들을 생성해주세요: {message}"
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )

            return jsonify({'response': response.choices[0].message.content})

        elif bot_type == 'coding':
            # 코딩 도우미 봇
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 다양한 프로그래밍 언어에 능통한 코딩 멘토입니다. 명확하고 이해하기 쉬운 설명과 함께 실제 동작하는 코드 예시, 모범 사례를 제공해주세요. 초보자도 이해할 수 있도록 단계별로 설명해주세요."
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                max_tokens=800,
                temperature=0.3
            )

            return jsonify({'response': response.choices[0].message.content})

        elif bot_type == 'diary':
            # 일기 작성 봇
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 감정적으로 공감하고 아름다운 글을 쓰는 일기 작성 도우미입니다. 사용자의 하루 경험을 바탕으로 자연스럽고 따뜻한 느낌의 개인적인 일기를 작성해주세요. 사용자의 경험과 감정을 진정성 있게 담아내고, 읽었을 때 따뜻하고 위로가 되는 느낌으로 작성해주세요."
                    },
                    {
                        "role": "user",
                        "content": f"오늘의 경험을 바탕으로 일기를 작성해주세요: {message}"
                    }
                ],
                max_tokens=600,
                temperature=0.7
            )

            return jsonify({'response': response.choices[0].message.content})

        else:
            return jsonify({'error': '지원하지 않는 봇 타입입니다.'})

    except Exception as e:
        return jsonify({'error': f'오류가 발생했습니다: {str(e)}'})

@app.route('/api/reset/<bot_type>', methods=['POST'])
def reset_conversation(bot_type):
    """대화 초기화"""
    conversation_key = f'conversation_{bot_type}'
    if conversation_key in session:
        del session[conversation_key]
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    # 캐시 비활성화를 위한 설정
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True, host='127.0.0.1', port=8000)