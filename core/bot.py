# core/bot.py
import discord
from core import event_handler

def run_bot(token):
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print("-" * 30)
        print(f"🚀 Bot is ready! Logged in as {client.user}")
        print("-" * 30)

    @client.event
    async def on_message(message):
        # 메시지가 오면 event_handler에게 처리를 위임합니다.
        await event_handler.handle_message(message)

    client.run(token)