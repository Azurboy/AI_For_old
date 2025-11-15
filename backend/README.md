# YuKeSong 后端 API

## 快速启动

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的API密钥
```

### 3. 启动服务器

```bash
python main.py
```

服务器将在 `http://localhost:8000` 启动。

## API端点

### POST /api/chat
核心对话端点（F-007）

**请求:**
- `audio`: 音频文件 (multipart/form-data)

**响应:**
- 音频流 (audio/mpeg)
- Header `X-AI-Text`: AI回复文本
- Header `X-User-Text`: 识别的用户文本

### GET /api/generate_biography
生成传记和认知评估（F-008）

**响应:**
```json
{
  "biography": "## Markdown格式的人生纪要",
  "cognitive_assessment": {
    "overall_risk": "低风险/中风险/高风险",
    "memory_score": 8,
    "time_orientation": 9,
    "language_fluency": 8,
    "concerns": []
  },
  "total_conversations": 42
}
```

### GET /api/conversations
获取对话历史（调试用）

## 技术栈

- **FastAPI**: Web框架
- **SQLite**: 本地数据库（chat_history表）
- **ChromaDB**: 向量数据库（RAG记忆检索）
- **讯飞**: 语音识别（方言支持）
- **Gemini 1.5 Pro**: 大语言模型
- **ElevenLabs**: 语音合成（声音克隆）

