# memory_system/vector_db.py

import chromadb
from config import VECTOR_DB_PATH, COLLECTION_NAME

# ChromaDB 클라이언트 초기화. 지정된 경로에 데이터를 영구적으로 저장합니다.
client = chromadb.PersistentClient(path=VECTOR_DB_PATH)

# 사용자 기억을 저장할 컬렉션을 가져오거나 생성합니다.
# 이 컬렉션이 모든 기억의 저장소가 됩니다.
collection = client.get_or_create_collection(name=COLLECTION_NAME)

print("✅ VectorDB a.k.a. Memory Store is ready.")