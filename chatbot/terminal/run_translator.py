#!/usr/bin/env python3
"""
터미널 전용 번역 봇
웹 인터페이스 없이 명령줄에서 직접 실행하는 번역 봇입니다.
"""

import sys
import os

# 상위 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from chatbot.web.translator_bot import translator_bot

if __name__ == "__main__":
    print("🌐 터미널 번역 봇")
    print("=" * 40)
    translator_bot()