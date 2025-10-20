# main.py

import os
from dotenv import load_dotenv
from core.bot import run_bot

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not DISCORD_BOT_TOKEN or not GEMINI_API_KEY:
    raise ValueError("API 키와 토큰을 .env 파일에 설정해주세요.")

# Gemini API 키 설정 (라이브러리 전역)
import google.generativeai as genai
genai.configure(api_key=GEMINI_API_KEY)


if __name__ == "__main__":
    print("Starting Discord Bot...")
    run_bot(DISCORD_BOT_TOKEN)