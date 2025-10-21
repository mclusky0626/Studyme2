# core/event_handler.py

import asyncio  # [변경점 1] asyncio 라이브러리를 가져옵니다.
from memory_system import manager


async def handle_message(message):
    """Discord 메시지 이벤트를 받아 처리합니다."""
    # 봇 자신의 메시지는 무시합니다.
    if message.author.bot:
        return

    user_id = str(message.author.id)
    username = message.author.name
    message_text = message.content

    # [변경점 2] 시간이 오래 걸리는 동기 함수(process_message)를
    # 별도의 스레드에서 실행하도록 하여 메인 루프가 멈추는 것을 방지합니다.
    try:
        # 봇이 "생각 중..."임을 사용자에게 알려줍니다.
        async with message.channel.typing():
            response_text = await asyncio.to_thread(
                manager.process_message, user_id, username, message_text
            )

        # 응답이 있다면 채널에 메시지를 보냅니다.
        if response_text:
            await message.channel.send(response_text)

    except Exception as e:
        print(f"🚨 An error occurred in event_handler: {e}")
        await message.channel.send("죄송합니다. 요청을 처리하는 중에 오류가 발생했습니다.")