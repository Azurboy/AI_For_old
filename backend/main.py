"""
主API服务器 - FastAPI
"""
# 首先加载环境变量
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
from urllib.parse import quote
import uuid

from database import init_db, get_db, ChatHistory
from vector_store import vector_store
from ai_services import ai_services

# 初始化FastAPI
app = FastAPI(title="YuKeSong API", version="1.0.0")

# CORS配置（允许前端访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # MVP阶段允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 启动时初始化数据库
@app.on_event("startup")
async def startup_event():
    init_db()
    print("✅ 数据库已初始化")
    print("✅ ChromaDB已就绪")
    print("🚀 服务器启动成功！")


@app.get("/")
async def root():
    """健康检查"""
    return {
        "status": "ok",
        "message": "YuKeSong API is running",
        "version": "1.0.0",
        "siliconflow_configured": bool(ai_services.siliconflow_api_key)
    }


@app.get("/api/config")
async def check_config():
    """检查API配置状态"""
    return {
        "siliconflow": {
            "configured": bool(ai_services.siliconflow_api_key),
            "api_key_prefix": ai_services.siliconflow_api_key[:10] + "..." if ai_services.siliconflow_api_key else "未配置",
            "services": {
                "stt": "TeleAI/TeleSpeechASR",
                "llm": "Qwen/Qwen2.5-7B-Instruct"
            }
        },
        "elevenlabs": {
            "configured": bool(ai_services.elevenlabs_api_key)
        }
    }


@app.post("/api/chat")
async def chat_endpoint(
    audio: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):
    """
    核心交互端点 (F-007)
    
    流程：
    1. STT: 讯飞语音识别
    2. Context: 检索相关记忆
    3. LLM: Gemini生成回复
    4. TTS: ElevenLabs生成语音
    5. Save: 后台保存到数据库和向量库
    """
    try:
        # 读取音频数据
        audio_data = await audio.read()
        
        # Step 1: STT - 语音转文字
        user_text = await ai_services.speech_to_text(audio_data)
        
        if not user_text or user_text == "语音识别失败，请重试":
            return JSONResponse(
                status_code=400,
                content={"error": "语音识别失败"}
            )
        
        # Step 2: 检索相关记忆
        relevant_memories = vector_store.query_relevant_memories(user_text, n_results=3)
        
        # 获取最近对话历史
        recent_history = db.query(ChatHistory).order_by(
            ChatHistory.timestamp.desc()
        ).limit(5).all()
        
        history_list = [
            {"user_text": h.user_text, "ai_text": h.ai_text}
            for h in reversed(recent_history)
        ]
        
        # Step 3: LLM - 生成AI回复
        ai_text = await ai_services.generate_response(
            user_text=user_text,
            conversation_history=history_list,
            relevant_memories=relevant_memories
        )
        
        # Step 4: TTS - 生成语音
        audio_response = await ai_services.text_to_speech(ai_text)
        
        # Step 5: 后台保存（不阻塞响应）
        background_tasks.add_task(
            save_conversation,
            db=db,
            user_text=user_text,
            ai_text=ai_text
        )
        
        # 返回音频和文本（对中文进行URL编码以支持HTTP header）
        from urllib.parse import quote
        return Response(
            content=audio_response,
            media_type="audio/mpeg",
            headers={
                "X-AI-Text": quote(ai_text),  # URL编码中文
                "X-User-Text": quote(user_text)
            }
        )
        
    except Exception as e:
        print(f"Chat Error: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


def save_conversation(db: Session, user_text: str, ai_text: str):
    """后台任务：保存对话到数据库和向量库"""
    try:
        # 保存到SQLite
        chat = ChatHistory(
            session_id="demo_elder",
            user_text=user_text,
            ai_text=ai_text,
            timestamp=datetime.utcnow()
        )
        db.add(chat)
        db.commit()
        
        # 保存到ChromaDB
        conversation_id = f"conv_{uuid.uuid4().hex[:8]}"
        vector_store.add_conversation(conversation_id, user_text, ai_text)
        
        print(f"✅ 对话已保存: {user_text[:20]}...")
        
    except Exception as e:
        print(f"保存失败: {e}")
        db.rollback()


@app.get("/api/generate_biography")
async def generate_biography(db: Session = Depends(get_db)):
    """
    演示端点 (F-008)
    
    生成：
    1. 老人的"人生纪要"（Markdown）
    2. 认知健康评估（JSON）
    """
    try:
        # 获取所有对话记录
        all_conversations = db.query(ChatHistory).order_by(
            ChatHistory.timestamp.asc()
        ).all()
        
        if not all_conversations:
            return {
                "biography": "## 暂无对话记录\n\n请先与老人进行对话。",
                "cognitive_assessment": {
                    "overall_risk": "未评估",
                    "memory_score": 0,
                    "time_orientation": 0,
                    "language_fluency": 0,
                    "concerns": ["暂无数据"]
                },
                "total_conversations": 0
            }
        
        # 调用AI生成传记和评估
        result = await ai_services.generate_biography(all_conversations)
        
        return {
            **result,
            "total_conversations": len(all_conversations),
            "first_conversation": all_conversations[0].timestamp.isoformat(),
            "last_conversation": all_conversations[-1].timestamp.isoformat()
        }
        
    except Exception as e:
        print(f"Biography Error: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.get("/api/conversations")
async def get_conversations(limit: int = 50, db: Session = Depends(get_db)):
    """获取对话历史（调试用）"""
    conversations = db.query(ChatHistory).order_by(
        ChatHistory.timestamp.desc()
    ).limit(limit).all()
    
    return {
        "total": len(conversations),
        "conversations": [
            {
                "id": conv.id,
                "user_text": conv.user_text,
                "ai_text": conv.ai_text,
                "timestamp": conv.timestamp.isoformat()
            }
            for conv in conversations
        ]
    }


@app.get("/api/dashboard/insights")
async def get_dashboard_insights(db: Session = Depends(get_db)):
    """
    仪表盘端点 - 对话洞察分析
    
    返回：
    1. 对话总结
    2. 情感分析（用户情绪、需求）
    3. 认知能力评估（记忆、时间定向、语言能力）
    4. 关键信息提取
    """
    try:
        # 获取所有对话记录
        all_conversations = db.query(ChatHistory).order_by(
            ChatHistory.timestamp.desc()
        ).all()
        
        if not all_conversations:
            return {
                "summary": "暂无对话数据",
                "total_conversations": 0,
                "emotion_analysis": {},
                "cognitive_assessment": {},
                "key_insights": []
            }
        
        # 调用AI进行深度分析
        insights = await ai_services.generate_dashboard_insights(all_conversations)
        
        # 添加统计信息
        insights["statistics"] = {
            "total_conversations": len(all_conversations),
            "first_conversation": all_conversations[-1].timestamp.isoformat(),
            "last_conversation": all_conversations[0].timestamp.isoformat(),
            "avg_user_text_length": sum(len(c.user_text) for c in all_conversations) / len(all_conversations),
            "recent_conversations": [
                {
                    "user": c.user_text,
                    "ai": c.ai_text,
                    "time": c.timestamp.isoformat()
                }
                for c in all_conversations[:5]
            ]
        }
        
        return insights
        
    except Exception as e:
        print(f"Dashboard Insights Error: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

