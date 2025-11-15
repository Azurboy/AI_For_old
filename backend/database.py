"""
数据库模型和初始化
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# 本地SQLite数据库
DATABASE_URL = "sqlite:///./yukesong.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class ChatHistory(Base):
    """对话历史表"""
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, default="demo_elder")  # MVP只有一个"老人"
    user_text = Column(Text, nullable=False)  # 老人说的话（方言转普通话）
    ai_text = Column(Text, nullable=False)    # AI回复的文本
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # 认知健康相关字段（可选）
    has_memory_concern = Column(Integer, default=0)  # 0=正常, 1=有风险
    has_time_confusion = Column(Integer, default=0)
    has_logic_confusion = Column(Integer, default=0)


def init_db():
    """初始化数据库"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """获取数据库session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

