# core/event_handler.py

from memory_system import manager

async def handle_message(message):
    """Discord 메시지 이벤트를 받아 처리합니다."""
    # 봇 자신의 메시지는 무시합니다.
    if message.author.bot:
        return

    user_id = str(message.author.id)
    username = message.author.name
    message_text = message.content

    # 메시지 내용을 비동기적으로 처리하고 응답을 받습니다.
    # 이 부분은 추후 복잡한 비동기 작업에 대비한 구조입니다.
    response_text = manager.process_message(user_id, username, message_text)

    # 응답이 있다면 채널에 메시지를 보냅니다.
    if response_text:
        await message.channel.send(response_text)