# 📁 项目结构说明

```
YuKesong2/
│
├── 📄 README.md                    # 项目主文档
├── 📄 QUICKSTART.md                # 5分钟快速启动指南
├── 📄 DEMO_GUIDE.md                # 黑客松演示脚本（3分钟）
├── 📄 PROJECT_STRUCTURE.md         # 本文件
├── 📄 .gitignore                   # Git忽略配置
├── 🚀 start.sh                     # 一键启动脚本
│
├── 📁 backend/                     # 后端API服务
│   ├── 📄 main.py                  # FastAPI主应用
│   ├── 📄 database.py              # SQLite数据库模型
│   ├── 📄 vector_store.py          # ChromaDB向量存储
│   ├── 📄 ai_services.py           # AI服务集成（STT/LLM/TTS）
│   ├── 📄 seed_demo_data.py        # 演示数据生成脚本
│   ├── 📄 requirements.txt         # Python依赖
│   ├── 📄 .env.example             # 环境变量模板
│   ├── 📄 README.md                # 后端文档
│   ├── 📁 chroma_data/             # ChromaDB本地存储（自动生成）
│   └── 📄 yukesong.db              # SQLite数据库（自动生成）
│
├── 📁 frontend/                    # 前端应用（老人端）
│   ├── 📁 src/
│   │   ├── 📁 components/
│   │   │   ├── 📄 IdleView.jsx             # 空闲界面（大按钮拨号）
│   │   │   ├── 📄 IdleView.css
│   │   │   ├── 📄 InCallView.jsx           # 通话界面（iOS风格）
│   │   │   ├── 📄 InCallView.css
│   │   │   ├── 📄 VoiceActivityDetector.jsx # VAD语音检测
│   │   │   └── 📄 VoiceActivityDetector.css
│   │   ├── 📄 App.jsx                      # 主应用组件
│   │   ├── 📄 App.css
│   │   ├── 📄 main.jsx                     # React入口
│   │   └── 📄 index.css                    # 全局样式
│   ├── 📄 index.html                       # HTML模板
│   ├── 📄 vite.config.js                   # Vite配置
│   ├── 📄 package.json                     # Node.js依赖
│   └── 📄 README.md                        # 前端文档
│
└── 📁 dashboard/                   # 演示仪表盘（儿孙端）
    ├── 📄 index.html               # 仪表盘主页
    ├── 📄 styles.css               # 样式表
    ├── 📄 script.js                # 业务逻辑
    └── 📄 README.md                # 仪表盘文档
```

---

## 📦 核心模块说明

### 🔧 后端 (Backend)

#### `main.py` - FastAPI主应用
- **职责**: 提供RESTful API
- **端点**:
  - `POST /api/chat` - 核心对话接口
  - `GET /api/generate_biography` - 生成传记和评估
  - `GET /api/conversations` - 获取对话历史

#### `database.py` - 数据库层
- **技术**: SQLite + SQLAlchemy
- **表结构**:
  - `chat_history`: 对话记录
    - id, session_id, user_text, ai_text, timestamp
    - has_memory_concern, has_time_confusion, has_logic_confusion

#### `vector_store.py` - 向量数据库
- **技术**: ChromaDB
- **功能**:
  - 存储对话向量
  - RAG记忆检索
  - 洞见管理

#### `ai_services.py` - AI服务集成
- **STT**: 讯飞语音识别（方言支持）
- **LLM**: Gemini 1.5 Pro（对话生成）
- **TTS**: ElevenLabs（声音克隆）
- **Prompt工程**: "好奇的晚辈"人格

#### `seed_demo_data.py` - 数据填充
- 生成20条演示对话
- 填充7条洞见
- 用于快速展示效果

---

### 🎨 前端 (Frontend)

#### `App.jsx` - 状态管理
- **状态**:
  - `isCalling`: boolean - 是否在通话中
  - `callState`: 'idle' | 'connecting' | 'connected' | 'ended'
- **逻辑**: 控制界面切换

#### `IdleView.jsx` - 空闲界面
- **F-002**: 大按钮拨号界面
- **设计**: 模拟"打电话"心智模型
- **元素**: 头像、姓名、呼叫按钮

#### `InCallView.jsx` - 通话界面
- **F-003**: 像素级复刻iOS通话界面
- **功能**:
  - 实时通话时长
  - 静音/扬声器控制
  - 红色挂断按钮
  - AI说话动画

#### `VoiceActivityDetector.jsx` - VAD组件
- **F-004**: 语音活动检测
- **技术**: Web Audio API
- **流程**:
  1. 实时音量分析
  2. 超过阈值 → 开始录音
  3. 静音1.5秒 → 停止录音
  4. 发送音频到后端

---

### 📊 仪表盘 (Dashboard)

#### `index.html` - 页面结构
- **布局**:
  - 顶部: 标题 + 刷新按钮
  - 统计卡片: 4个关键指标
  - 左侧面板: 认知健康评估
  - 右侧面板: 人生纪要

#### `script.js` - 业务逻辑
- **功能**:
  - 调用 `/api/generate_biography`
  - 渲染Markdown
  - 动态更新统计数据

#### `styles.css` - 视觉设计
- **风格**: 现代、清晰、温暖
- **配色**: 紫色渐变主题
- **响应式**: 支持移动端

---

## 🔄 数据流

### 对话流程

```
1. 用户说话
   ↓
2. VoiceActivityDetector 检测 → 录音
   ↓
3. POST /api/chat (audioBlob)
   ↓
4. 后端: STT → 文本
   ↓
5. 后端: 检索RAG记忆
   ↓
6. 后端: Gemini生成回复
   ↓
7. 后端: TTS → 音频
   ↓
8. 后台保存: SQLite + ChromaDB
   ↓
9. 返回: 音频 + Header(文本)
   ↓
10. 前端: 播放音频 + 显示文本
```

### 仪表盘流程

```
1. 点击"刷新数据"
   ↓
2. GET /api/generate_biography
   ↓
3. 后端: 查询所有对话
   ↓
4. 后端: Gemini生成传记 + 评估
   ↓
5. 返回: JSON
   {
     biography: Markdown,
     cognitive_assessment: {...},
     total_conversations: 20
   }
   ↓
6. 前端: 渲染Markdown + 更新统计
```

---

## 🗄️ 数据存储

### SQLite (关系型)
- **文件**: `backend/yukesong.db`
- **表**: `chat_history`
- **用途**: 结构化对话记录

### ChromaDB (向量型)
- **目录**: `backend/chroma_data/`
- **Collection**: `elder_memories`
- **用途**: 语义检索、RAG记忆

---

## 🔐 配置文件

### `backend/.env`
```bash
XUNFEI_APP_ID=xxx          # 讯飞语音识别
XUNFEI_API_KEY=xxx
XUNFEI_API_SECRET=xxx

GEMINI_API_KEY=xxx         # Gemini 1.5 Pro

ELEVENLABS_API_KEY=xxx     # ElevenLabs TTS
ELEVENLABS_VOICE_ID=xxx
```

**注意**: `.env` 不会被git跟踪（在 `.gitignore` 中）

---

## 🧪 测试脚本

### 生成演示数据
```bash
cd backend
python seed_demo_data.py
```

### 启动所有服务
```bash
./start.sh
```

### 手动测试API
```bash
# 健康检查
curl http://localhost:8000/

# 获取对话历史
curl http://localhost:8000/api/conversations

# 生成传记
curl http://localhost:8000/api/generate_biography
```

---

## 📈 扩展方向

### 短期 (黑客松后)
- [ ] 实现讯飞STT完整集成
- [ ] 声音克隆上传界面
- [ ] 多设备同步

### 中期 (产品化)
- [ ] 儿孙端注册/登录
- [ ] 多老人管理
- [ ] 推送通知（异常提醒）
- [ ] 数据导出（PDF报告）

### 长期 (商业化)
- [ ] 小程序/App
- [ ] 专用硬件设备
- [ ] 养老机构B2B方案
- [ ] 医疗机构数据对接

---

## 💡 设计原则

1. **零门槛**: 老人不需要学习，像打电话一样简单
2. **非侵入**: 不让老人感觉被"测试"或"监控"
3. **有温度**: AI有人格，不是冰冷的工具
4. **本地优先**: 数据存本地，保护隐私
5. **演示优先**: MVP聚焦黑客松演示，砍掉非核心功能

---

## 🎯 黑客松评分对应

| 功能 | 文件位置 | 评分点 |
|------|---------|--------|
| VAD自动录音 | `VoiceActivityDetector.jsx` | P0: 流畅对话 |
| iOS通话界面 | `InCallView.jsx` | P0: 零门槛交互 |
| 方言识别 | `ai_services.py` - STT | P1: 技术难度 |
| 声音克隆 | `ai_services.py` - TTS | P1: 情感连接 |
| RAG记忆 | `vector_store.py` | P2: AI智能 |
| 非侵入评估 | `ai_services.py` - Prompt | P2: 产品洞察 |
| 传记生成 | `generate_biography` API | P3: 价值展示 |
| 认知评估 | 仪表盘展示 | P3: 医疗价值 |

---

**更新日期**: 2025-11-14  
**版本**: 1.0.0 (MVP)

