# memory_system/tools.py

import uuid
from memory_system.vector_db import collection


# --- 개인 기억 관리 도구 (CRUD) ---

def save_memory(user_id: str, username: str, fact: str):
    """지정된 사용자에 대한 새로운 '개인적인' 사실(기억)을 저장합니다."""
    memory_id = f"{user_id}_{uuid.uuid4()}"
    collection.add(
        documents=[fact],
        metadatas=[{"owner_user_id": user_id, "owner_username": username, "memory_type": "personal"}],
        ids=[memory_id]
    )
    print(f"🧠 PERSONAL MEMORY SAVED for {username}: {fact}")
    return f"ACTION_SUCCESS: '{fact}' 정보가 {username}님에 대한 새로운 개인 기억으로 저장되었습니다."


def search_memory(user_id: str, query: str):
    """'특정 사용자'의 개인 기억 속에서 정보를 검색합니다."""
    results = collection.query(
        query_texts=[query],
        n_results=3,
        where={"owner_user_id": user_id}
    )
    found_memories = results['documents'][0]
    if not found_memories:
        print(f"🚫 PERSONAL MEMORY NOT FOUND for user {user_id} with query: {query}")
        return "RESULT_NOT_FOUND: 해당 사용자에 대한 관련 기억을 찾지 못했습니다."
    print(f"🔍 PERSONAL MEMORY FOUND for user {user_id}: {found_memories}")
    return "\n".join(found_memories)


def delete_memory(user_id: str, fact_to_delete_query: str):
    """지정된 사용자의 개인 기억 중 특정 정보와 가장 유사한 것을 찾아 삭제합니다."""
    results = collection.query(
        query_texts=[fact_to_delete_query],
        n_results=1,
        where={"owner_user_id": user_id},
        include=["documents"]
    )
    if not results['ids'][0]:
        print(f"🚫 DELETE FAILED: Memory not found for user {user_id} with query: {fact_to_delete_query}")
        return "ACTION_FAILED: 삭제할 기억을 찾지 못했습니다."
    target_id = results['ids'][0][0]
    deleted_document = results['documents'][0][0]
    collection.delete(ids=[target_id])
    print(f"🗑️ MEMORY DELETED for user {user_id}: {deleted_document}")
    return f"ACTION_SUCCESS: 관련 기억('{deleted_document}')이 성공적으로 삭제되었습니다."


def update_memory(user_id: str, username: str, old_fact_query: str, new_fact: str):
    """사용자의 기존 개인 기억을 새로운 사실로 업데이트합니다."""
    print(f"🔄 MEMORY UPDATE initiated for {username}. Query: '{old_fact_query}'")
    delete_result = delete_memory(user_id, old_fact_query)
    if "ACTION_FAILED" in delete_result:
        # 기존 정보가 없어도 그냥 새로 저장
        save_result = save_memory(user_id, username, new_fact)
        return f"기존 정보는 찾지 못했지만, 새 정보로 저장했습니다: {save_result}"

    save_result = save_memory(user_id, username, new_fact)
    return f"ACTION_SUCCESS: 기억 업데이트 완료. {save_result}"


# --- 소셜 추론 도구 ---

def save_user_alias(user_id: str, username: str, alias: str):
    """사용자의 Discord 계정과 실제 이름/별명(alias)을 연결하여 공개 정보로 저장합니다."""
    memory_id = f"alias_{user_id}_{alias.replace(' ', '_')}"
    document = f"Discord 사용자 '{username}'(ID: {user_id})님의 별명은 '{alias}'입니다."
    collection.add(
        documents=[document],
        metadatas=[{"owner_user_id": user_id, "owner_username": username, "memory_type": "alias"}],
        ids=[memory_id]
    )
    print(f"🏢 PUBLIC ALIAS SAVED: {username} is now known as {alias}")
    return f"ACTION_SUCCESS: 이제부터 {username}님을 '{alias}'(으)로도 기억하겠습니다."


def search_public_memory(query: str):
    """모든 사용자의 '별명(alias)' 정보 중에서 특정 이름과 관련된 것을 검색합니다."""
    results = collection.query(
        query_texts=[query],
        n_results=5,  # 동명이인 가능성을 대비해 조금 더 많이 검색
        where={"memory_type": "alias"},
        include=["metadatas", "documents"]
    )

    docs = results['documents'][0]
    metadatas = results['metadatas'][0]

    if not docs:
        print(f"🚫 PUBLIC MEMORY NOT FOUND with query: {query}")
        return "RESULT_NOT_FOUND: 서버 전체에서 해당 이름을 가진 사용자를 찾을 수 없습니다."

    # AI가 결과를 파싱하기 쉽도록 구조화된 문자열로 반환
    structured_results = []
    for meta, doc in zip(metadatas, docs):
        structured_results.append(
            f"[Found User: username='{meta['owner_username']}', user_id='{meta['owner_user_id']}', matched_info='{doc}']"
        )

    print(f"🌍 PUBLIC MEMORY FOUND: {structured_results}")

    # 동명이인 여부를 AI가 판단할 수 있도록 결과 개수 정보도 함께 제공
    return f"FOUND_{len(structured_results)}_USERS:\n" + "\n".join(structured_results)