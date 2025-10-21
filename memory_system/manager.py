# memory_system/manager.py

import google.generativeai as genai
from config import MODEL_NAME, SYSTEM_PROMPT
from memory_system import tools

# Gemini 모델 초기화 (최종 버전)
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

)

# 사용자별 대화 기록을 관리하기 위한 딕셔너리
user_conversations = {}


def process_message(user_id: str, username: str, message_text: str):
    """
    사용자 메시지를 받아 AI 응답을 생성하는 전체 과정을 처리합니다.
    """
    if user_id not in user_conversations:
        user_conversations[user_id] = model.start_chat(history=[])

    chat_session = user_conversations[user_id]

    try:
        # 1. 사용자 메시지를 AI에게 보냅니다.
        response = chat_session.send_message(message_text)

        # 2. AI가 도구 사용을 결정하면, 모든 연쇄 작업이 끝날 때까지 반복합니다.
        while response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call

            func_name = function_call.name
            args = {key: value for key, value in function_call.args.items()}

            tool_function = getattr(tools, func_name)

            # 함수 정의를 검사하여 필요한 인자만 동적으로 추가
            func_params = tool_function.__code__.co_varnames
            if 'user_id' in func_params:
                args['user_id'] = user_id
            if 'username' in func_params:
                args['username'] = username

            # 3. 도구를 실행하고 결과를 받습니다.
            tool_response = tool_function(**args)

            # 4. 도구 실행 결과를 다시 AI에게 보내 다음 행동을 결정하게 합니다.
            response = chat_session.send_message(
                {"function_response": {
                    "name": func_name,
                    "response": {"result": tool_response}
                    }
                }
            )

        # 5. 모든 도구 사용이 끝나면 최종 답변을 반환합니다.
        return response.text

    except Exception as e:
        import traceback
        print(f"🚨 An error occurred in Memory Manager: {e}\n{traceback.format_exc()}")
        return "죄송합니다, 처리 중 심각한 오류가 발생했습니다. 관리자에게 로그를 확인해달라고 요청해주세요."