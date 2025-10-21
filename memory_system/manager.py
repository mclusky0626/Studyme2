# memory_system/manager.py

import google.generativeai as genai
from google.generativeai.types import generation_types
from config import MODEL_NAME, SYSTEM_PROMPT, SAFETY_SETTINGS
from memory_system import tools

# Gemini 모델 초기화
model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    tools=[
        tools.save_my_memory,
        tools.update_my_memory,
        tools.delete_my_memory,
        tools.save_my_alias,
        tools.find_user_by_alias,
        tools.search_user_memory
    ],
    system_instruction=SYSTEM_PROMPT,
    safety_settings=SAFETY_SETTINGS
)

# 사용자별 대화 기록을 관리하기 위한 딕셔너리
user_conversations = {}


def process_message(user_id: str, username: str, message_text: str):
    """
    사용자 메시지를 받아 AI 응답을 생성하는 전체 과정을 처리합니다.
    (답변 우선 처리 및 최종 안정화 버전)
    """
    if user_id not in user_conversations:
        user_conversations[user_id] = model.start_chat(history=[])

    chat_session = user_conversations[user_id]

    try:
        contextual_message = f"From user '{username}' (ID: {user_id}): {message_text}"
        response = chat_session.send_message(contextual_message)

        # 도구 호출을 최대 5번까지 제한하여 무한 루프를 방지
        for _ in range(5):
            # --- [핵심 아키텍처 수정] ---
            # 1. 안전하게 응답 파트를 가져옵니다.
            if not response.candidates or not response.candidates[0].content.parts:
                print("🚨 WARNING: Received an empty or incomplete response from API.")
                return "죄송합니다, 답변을 생성할 수 없습니다."
            part = response.candidates[0].content.parts[0]

            # 2. 텍스트 답변이 있으면, 무조건 그것을 최종 답변으로 삼고 즉시 루프를 종료합니다.
            if hasattr(part, 'text') and part.text:
                return part.text

            # 3. 텍스트 답변이 없다면, 유효한 함수 호출이 있는지 확인합니다.
            if not hasattr(part, 'function_call') or not hasattr(part.function_call,
                                                                 'name') or not part.function_call.name:
                # 유효한 함수 호출도 없으면, AI가 길을 잃은 것이므로 중단합니다.
                print(f"🚨 ERROR: No text response and no valid function call. Aborting.")
                return "죄송합니다, AI가 작업을 결정하는 데 실패했습니다. 다시 시도해주세요."

            # 4. 유효한 함수 호출이 있으면, 도구를 실행합니다.
            function_call = part.function_call
            func_name = function_call.name
            args = {key: value for key, value in function_call.args.items()} if function_call.args else {}

            tool_function = getattr(tools, func_name)

            if "my" in func_name:
                args['user_id'] = user_id
                args['username'] = username

            try:
                tool_response = tool_function(**args)
            except Exception as e:
                print(f"🚨 TOOL EXECUTION ERROR in '{func_name}': {e}")
                tool_response = f"Error: 도구 '{func_name}' 실행 중 오류가 발생했습니다: {e}"

            try:
                # 도구 실행 결과를 다시 보내 다음 행동을 유도합니다.
                response = chat_session.send_message(
                    {"function_response": {"name": func_name, "response": {"result": tool_response}}}
                )
            except Exception as e:
                print(f"🚨 WARNING: API call stopped after function response. {e}")
                return "도구 실행 결과에 민감한 내용이 포함되어 답변을 생성할 수 없습니다."

        # for 루프가 모두 돌았는데도 답변이 없으면 타임아웃 처리
        return "죄송합니다, 작업을 처리하는 데 너무 오래 걸립니다."

    except Exception as e:
        import traceback
        print(f"🚨 An error occurred in Memory Manager: {e}\n{traceback.format_exc()}")
        return "죄송합니다, 처리 중 심각한 오류가 발생했습니다."