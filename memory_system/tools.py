# memory_system/tools.py

import uuid
from memory_system.vector_db import collection


# --- '나(메시지 작성자)'의 기억을 관리하는 도구들 ---

def save_my_memory(user_id: str, username: str, fact: str):
    """'나 자신'에 대한 새로운 개인적인 사실(기억)을 저장합니다. (예: 내 직업, 내 취미)"""
    memory_id = f"{user_id}_{uuid.uuid4()}"
    collection.add(
        documents=[fact],
        metadatas=[{"owner_user_id": user_id, "owner_username": username, "memory_type": "personal"}],
        ids=[memory_id]
    )
    print(f"🧠 MY MEMORY SAVED for {username}: {fact}")
    return f"ACTION_SUCCESS: '{fact}' 정보가 당신의 새로운 개인 기억으로 저장되었습니다."


def update_my_memory(user_id: str, username: str, old_fact_query: str, new_fact: str):
    """'나 자신'의 기존 개인 기억을 새로운 사실로 업데이트합니다."""
    # 먼저 삭제할 정보를 검색
    results = collection.query(query_texts=[old_fact_query], n_results=1, where={"owner_user_id": user_id})
    if not results['ids'][0]:
        # 기존 정보가 없어도 그냥 새로 저장
        return save_my_memory(user_id, username, new_fact)

    # 있으면 삭제 후 새로 저장
    collection.delete(ids=results['ids'][0])
    return save_my_memory(user_id, username, new_fact)


def delete_my_memory(user_id: str, fact_to_delete_query: str):
    """'나 자신'의 개인 기억 중 특정 정보와 가장 유사한 것을 찾아 삭제합니다."""
    results = collection.query(query_texts=[fact_to_delete_query], n_results=1, where={"owner_user_id": user_id},
                               include=["documents"])
    if not results['ids'][0]:
        return "ACTION_FAILED: 삭제할 기억을 찾지 못했습니다."
    target_id = results['ids'][0][0]
    deleted_document = results['documents'][0][0]
    collection.delete(ids=[target_id])
    print(f"🗑️ MY MEMORY DELETED for user {user_id}: {deleted_document}")
    return f"ACTION_SUCCESS: 당신의 기억('{deleted_document}')이 성공적으로 삭제되었습니다."


# --- '모든 유저'를 대상으로 하거나 '특정 유저'를 검색하는 도구들 ---

def save_my_alias(user_id: str, username: str, alias: str):
    """'나 자신'의 Discord 계정과 실제 이름/별명(alias)을 연결하여 공개 정보로 저장합니다."""
    memory_id = f"alias_{user_id}_{alias.replace(' ', '_')}"
    document = f"Discord 사용자 '{username}'(ID: {user_id})님의 별명은 '{alias}'입니다."
    collection.add(
        documents=[document],
        metadatas=[{"owner_user_id": user_id, "owner_username": username, "memory_type": "alias"}],
        ids=[memory_id]
    )
    print(f"🏢 PUBLIC ALIAS SAVED: {username} is now known as {alias}")
    return f"ACTION_SUCCESS: 이제부터 당신을 '{alias}'(으)로도 기억하겠습니다."


def find_user_by_alias(alias_query: str):
    """서버 전체에서 특정 별명(alias)을 가진 사용자를 검색하여, 그 사람의 Discord ID와 사용자명을 찾습니다."""
    results = collection.query(
        query_texts=[alias_query],
        n_results=5,
        where={"memory_type": "alias"},
        include=["metadatas", "documents"]
    )
    docs, metadatas = results['documents'][0], results['metadatas'][0]
    if not docs:
        return "RESULT_NOT_FOUND: 서버 전체에서 해당 이름을 가진 사용자를 찾을 수 없습니다."

    structured_results = [
        f"[Found User: username='{meta['owner_username']}', user_id='{meta['owner_user_id']}', matched_info='{doc}']"
        for meta, doc in zip(metadatas, docs)
    ]
    return f"FOUND_{len(structured_results)}_USERS:\n" + "\n".join(structured_results)


def search_user_memory(target_user_id: str, query: str):
    """
    [가장 중요] '특정 사용자 ID(target_user_id)'를 가진 사람의 개인 기억 속에서 정보를 검색합니다.
    다른 사람의 정보를 찾으려면 반드시 이 함수를 사용해야 합니다.
    """
    results = collection.query(
        query_texts=[query],
        n_results=3,
        where={"owner_user_id": target_user_id}  # 이제 AI가 지정한 ID로 검색합니다!
    )
    found_memories = results['documents'][0]
    if not found_memories:
        return "RESULT_NOT_FOUND: 해당 사용자에 대한 관련 기억을 찾지 못했습니다."

    print(f"🔍 SEARCHED MEMORY for user {target_user_id}: {found_memories}")
    return "\n".join(found_memories)