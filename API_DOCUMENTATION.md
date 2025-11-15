# 🔌 API文档

基础URL: `http://localhost:8000`

---

## 📡 端点列表

### 1. 健康检查

**GET** `/`

检查API服务器是否正常运行。

**响应:**
```json
{
  "status": "ok",
  "message": "YuKeSong API is running",
  "version": "1.0.0"
}
```

---

### 2. 核心对话接口 ⭐

**POST** `/api/chat`

**功能**: 核心交互端点（F-007）

**流程**:
1. STT: 讯飞语音识别
2. Context: ChromaDB检索相关记忆
3. LLM: Gemini生成AI回复
4. TTS: ElevenLabs生成语音
5. Save: 后台保存到数据库

**请求:**
- Content-Type: `multipart/form-data`
- Body:
  - `audio`: 音频文件 (File) - 支持 webm, mp3, wav等格式

**示例 (cURL):**
```bash
curl -X POST http://localhost:8000/api/chat \
  -F "audio=@recording.webm"
```

**示例 (JavaScript):**
```javascript
const formData = new FormData();
formData.append('audio', audioBlob, 'user_speech.webm');

const response = await fetch('/api/chat', {
  method: 'POST',
  body: formData
});

// 获取AI文本回复（从header）
const aiText = response.headers.get('X-AI-Text');
const userText = response.headers.get('X-User-Text');

// 获取音频流
const audioBlob = await response.blob();
const audioUrl = URL.createObjectURL(audioBlob);
```

**响应:**
- Content-Type: `audio/mpeg`
- Body: 音频流（MP3格式）
- Headers:
  - `X-AI-Text`: AI回复的文本内容
  - `X-User-Text`: 识别的用户文本

**错误响应:**
```json
{
  "error": "语音识别失败"
}
```

**状态码:**
- `200`: 成功
- `400`: 请求错误（如音频格式不支持）
- `500`: 服务器错误

---

### 3. 生成传记和认知评估 ⭐

**GET** `/api/generate_biography`

**功能**: 演示端点（F-008），生成老人的人生纪要和认知健康评估

**请求:**
无需参数

**示例:**
```bash
curl http://localhost:8000/api/generate_biography
```

**响应:**
```json
{
  "biography": "## 李建国的人生故事\n\n### 青春岁月\n李建国1947年出生...",
  "cognitive_assessment": {
    "overall_risk": "低风险",
    "memory_score": 8,
    "time_orientation": 9,
    "language_fluency": 8,
    "concerns": [
      "偶尔重复相同问题",
      "夜间睡眠质量波动"
    ]
  },
  "total_conversations": 42,
  "first_conversation": "2025-11-11T10:30:00",
  "last_conversation": "2025-11-14T16:45:00"
}
```

**字段说明:**

| 字段 | 类型 | 说明 |
|------|------|------|
| biography | string | Markdown格式的人生纪要 |
| cognitive_assessment | object | 认知健康评估 |
| └─ overall_risk | string | 总体风险等级：低风险/中风险/高风险 |
| └─ memory_score | int | 记忆力评分 (0-10) |
| └─ time_orientation | int | 时间定向评分 (0-10) |
| └─ language_fluency | int | 语言流畅度评分 (0-10) |
| └─ concerns | array | 关注点列表 |
| total_conversations | int | 总对话次数 |
| first_conversation | string | 首次对话时间 (ISO 8601) |
| last_conversation | string | 最近对话时间 (ISO 8601) |

**空数据响应:**
```json
{
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
```

**状态码:**
- `200`: 成功
- `500`: 生成失败

---

### 4. 获取对话历史

**GET** `/api/conversations`

**功能**: 获取对话记录（调试用）

**请求参数:**
- `limit` (可选): 返回记录数，默认50

**示例:**
```bash
curl http://localhost:8000/api/conversations?limit=10
```

**响应:**
```json
{
  "total": 10,
  "conversations": [
    {
      "id": 42,
      "user_text": "今天天气真好",
      "ai_text": "是啊奶奶！您今天出去散步了吗？",
      "timestamp": "2025-11-14T10:30:00"
    },
    {
      "id": 41,
      "user_text": "我昨天做了红烧肉",
      "ai_text": "哇！一定很好吃，您的红烧肉怎么做的呀？",
      "timestamp": "2025-11-14T09:15:00"
    }
  ]
}
```

**状态码:**
- `200`: 成功

---

## 🔒 错误处理

所有端点遵循统一的错误格式：

```json
{
  "error": "错误描述信息"
}
```

**常见错误:**

| 状态码 | 错误 | 原因 |
|--------|------|------|
| 400 | 语音识别失败 | 音频格式不支持或音频损坏 |
| 500 | STT Error: ... | 讯飞API调用失败 |
| 500 | LLM Error: ... | Gemini API调用失败 |
| 500 | TTS Error: ... | ElevenLabs API调用失败 |

---

## 🧪 测试示例

### Python测试

```python
import requests

# 1. 健康检查
response = requests.get('http://localhost:8000/')
print(response.json())

# 2. 上传音频
with open('test_audio.webm', 'rb') as f:
    files = {'audio': f}
    response = requests.post('http://localhost:8000/api/chat', files=files)
    
    print('AI文本:', response.headers.get('X-AI-Text'))
    print('用户文本:', response.headers.get('X-User-Text'))
    
    # 保存音频
    with open('ai_response.mp3', 'wb') as out:
        out.write(response.content)

# 3. 获取传记
response = requests.get('http://localhost:8000/api/generate_biography')
data = response.json()
print('对话次数:', data['total_conversations'])
print('风险等级:', data['cognitive_assessment']['overall_risk'])
```

### JavaScript测试

```javascript
// 1. 健康检查
fetch('http://localhost:8000/')
  .then(res => res.json())
  .then(data => console.log(data));

// 2. 发送录音
const formData = new FormData();
formData.append('audio', audioBlob);

fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  body: formData
})
  .then(async (response) => {
    const aiText = response.headers.get('X-AI-Text');
    const audioBlob = await response.blob();
    
    // 播放音频
    const audio = new Audio(URL.createObjectURL(audioBlob));
    audio.play();
    
    console.log('AI说:', aiText);
  });

// 3. 获取传记
fetch('http://localhost:8000/api/generate_biography')
  .then(res => res.json())
  .then(data => {
    console.log('传记:', data.biography);
    console.log('评估:', data.cognitive_assessment);
  });
```

---

## 🌐 CORS配置

API已配置CORS允许所有来源访问（MVP阶段）：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**生产环境建议**: 限制 `allow_origins` 为特定域名。

---

## 📊 性能指标

| 端点 | 平均响应时间 | 最大负载 |
|------|--------------|----------|
| GET `/` | < 10ms | 无限制 |
| POST `/api/chat` | 2-5s | 取决于AI API |
| GET `/api/generate_biography` | 5-15s | 取决于对话数量 |

**注意**: 响应时间主要受外部AI API影响。

---

## 🔐 认证（未实现）

当前MVP版本**无需认证**。

未来版本可以添加：
- JWT Token
- API Key
- OAuth 2.0

---

## 📝 数据库Schema

### chat_history 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| session_id | VARCHAR | 会话ID（默认: demo_elder） |
| user_text | TEXT | 用户说的话 |
| ai_text | TEXT | AI回复 |
| timestamp | DATETIME | 时间戳 |
| has_memory_concern | INTEGER | 记忆关注 (0/1) |
| has_time_confusion | INTEGER | 时间混乱 (0/1) |
| has_logic_confusion | INTEGER | 逻辑混乱 (0/1) |

---

## 🚀 扩展API（规划中）

### 未来端点

```
POST /api/users/register          # 用户注册
POST /api/users/login             # 用户登录
POST /api/voices/upload           # 上传声音样本
GET  /api/elders/:id/summary      # 获取特定老人摘要
POST /api/alerts/config           # 配置告警规则
GET  /api/export/report           # 导出PDF报告
```

---

## 📚 相关文档

- [FastAPI官方文档](https://fastapi.tiangolo.com/)
- [Gemini API文档](https://ai.google.dev/docs)
- [ElevenLabs API文档](https://elevenlabs.io/docs)
- [讯飞语音API文档](https://www.xfyun.cn/doc/)

---

**更新日期**: 2025-11-14  
**API版本**: 1.0.0

