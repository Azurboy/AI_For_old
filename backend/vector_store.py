"""
ChromaDB向量存储 - 用于RAG记忆检索
"""
import chromadb
import os


class VectorStore:
    """向量数据库管理类"""
    
    def __init__(self):
        # 本地持久化存储（使用新版API）
        self.client = chromadb.PersistentClient(
            path="./chroma_data"
        )
        
        # 获取或创建collection
        self.collection = self.client.get_or_create_collection(
            name="elder_memories",
            metadata={"description": "老人的对话记忆和洞见"}
        )
    
    def add_conversation(self, conversation_id: str, user_text: str, ai_text: str):
        """添加对话到向量库"""
        combined_text = f"老人说: {user_text}\nAI回复: {ai_text}"
        
        self.collection.add(
            documents=[combined_text],
            metadatas=[{
                "user_text": user_text,
                "ai_text": ai_text,
                "type": "conversation"
            }],
            ids=[conversation_id]
        )
    
    def add_insight(self, insight_id: str, insight_text: str, category: str = "general"):
        """添加洞见到向量库（例如：发现老人喜欢红烧肉）"""
        self.collection.add(
            documents=[insight_text],
            metadatas=[{
                "category": category,
                "type": "insight"
            }],
            ids=[insight_id]
        )
    
    def query_relevant_memories(self, query_text: str, n_results: int = 3):
        """根据当前对话检索相关记忆"""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        
        if results['documents']:
            return results['documents'][0]
        return []


# 全局实例
vector_store = VectorStore()

