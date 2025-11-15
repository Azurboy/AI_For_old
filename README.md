# 语客颂 (YuKeSong) - AI老年陪伴与认知健康监测系统

> **"Build Whatever You Want" Hackathon Project**  
> 零门槛老年AI陪伴 + 非侵入式阿尔茨海默症早期检测

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18-61dafb.svg)](https://reactjs.org/)

---

## 📖 项目简介

**语客颂**是一个为老年人设计的AI陪伴系统，通过模拟电话交互提供：
1. **情感陪伴**：温暖、自然的AI对话，像孙女一样亲切
2. **认知监测**：非侵入式阿尔茨海默症早期检测（基于临床语言生物标记物）
3. **家属可视化**：详细的认知评估报告和风险预警

### 🎯 核心价值

- **零门槛交互**：模拟电话通话，老年人无需学习
- **非侵入式**：用户完全感受不到被"测试"
- **临床级分析**：基于10个语言生物标记物的科学评估
- **情感桥梁**：帮助家属理解父母的认知和情感状态

---

## 🏗️ 技术架构

### 双层多智能体架构（Dual-Layer Multi-Agent Architecture）

```
┌─────────────────────────────────────────────────┐
│          用户（老年人）                          │
│              ↓↑ 语音交互                         │
└─────────────────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        ↓                           ↑
┌──────────────────────┐    ┌──────────────────────┐
│  层一：伴侣智能体      │    │  语音识别（STT）      │
│  Companion Agent     │←───│  TeleAI ASR          │
│                      │    └──────────────────────┘
│ • 温暖、同理心对话    │
│ • 隐式激发策略        │    ┌──────────────────────┐
│ • 禁止测试性提问      │───→│  语音合成（TTS）      │
│                      │    │  ElevenLabs          │
└──────────────────────┘    └──────────────────────┘
        │
        │ 对话日志（异步）
        ↓
┌──────────────────────┐    ┌──────────────────────┐
│  层二：分析智能体      │    │  长期记忆（LTM）      │
│  Analyst Agent       │←───│  ChromaDB (RAG)      │
│                      │    └──────────────────────┘
│ • 临床语言学分析      │
│ • 10个生物标记物      │    ┌──────────────────────┐
│ • 认知风险评估        │───→│  对话历史（SQLite）   │
│                      │    │  纵向数据分析         │
└──────────────────────┘    └──────────────────────┘
        │
        ↓
┌──────────────────────┐
│  智能仪表盘（家属端）  │
│  • 认知评估报告       │
│  • 情感分析          │
│  • 风险预警          │
└──────────────────────┘
```

---

## 🛠️ 技术栈

### 后端（Backend）

| 技术 | 用途 | 版本 |
|------|------|------|
| **FastAPI** | Web框架 | 0.115.0 |
| **Python** | 后端语言 | 3.8+ |
| **SQLite + SQLAlchemy** | 对话历史存储 | 2.0.36 |
| **ChromaDB** | 向量数据库（RAG） | 0.4.24 |
| **httpx** | 异步HTTP客户端 | 0.28.1 |
| **pydantic** | 数据验证 | 2.10.3 |

### 前端（Frontend）

| 技术 | 用途 |
|------|------|
| **React 18** | UI框架 |
| **Vite** | 构建工具 |
| **Web Audio API** | 语音录制 |
| **纯CSS** | iOS风格通话UI |

### AI服务（使用硅基流动 SiliconFlow API）

| 服务 | 模型 | 用途 |
|------|------|------|
| **STT** | TeleAI/TeleSpeechASR | 语音识别 |
| **LLM（伴侣）** | Qwen/Qwen2.5-7B-Instruct | 对话交互（temp=0.8） |
| **LLM（分析）** | Qwen/Qwen2.5-7B-Instruct | 临床分析（temp=0.2） |
| **TTS** | ElevenLabs（可选） | 语音合成 |

---

## 🧠 AI Context Engineering

### 1. 伴侣智能体 System Prompt

**核心策略：隐式激发（Implicit Elicitation）**

| 策略 | 示例 | 目的 |
|------|------|------|
| **情景记忆激发** | "您昨天提到您看了一部电影，是讲什么的呀？" | 测试短期记忆 |
| **语义记忆激发** | "我们来玩个游戏！看看能想出多少种蔬菜？" | 测试词语流畅性 |
| **叙事激发** | "您能给我讲讲您孙子的故事吗？" | 测试语篇连贯性 |

**严格禁止事项：**
- ❌ 测试性问题："今天星期几？"、"请记住这三个词"
- ❌ 诊断性语言："您可能有认知问题"
- ❌ 暴露身份："我是AI"、"我在检测您"

### 2. 分析智能体 System Prompt

**评估10个临床语言生物标记物（基于阿尔茨海默症研究）：**

1. **Anomia_WordFinding_Difficulty**（命名障碍）
2. **Circumlocution**（迂回表达）
3. **Semantic_Error**（语义错误）
4. **Empty_Speech_Poverty_of_Content**（内容空洞）
5. **Repetition_Perseveration**（重复/持续言语）
6. **Speech_Fragmentation_Trailing_Off**（言语碎片化）
7. **Syntactic_Simplification**（句法简化）
8. **Pronoun_Misuse**（代词误用）
9. **Hesitation_Pause_Frequency_Duration**（犹豫和停顿）
10. **Global_Coherence_Loss**（全局连贯性丧失）

**评分标准：** 1（无迹象）- 7（非常强烈）

**输出格式：** 结构化JSON，包含score、rationale、raw_quote

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- 硅基流动（SiliconFlow）API Key

### 1. 克隆项目

```bash
git clone https://github.com/Azurboy/AI_For_old.git
cd AI_For_old
```

### 2. 配置后端

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env，填入你的API Keys
```

**`.env` 配置示例：**

```env
# 硅基流动API Key（必需）
SILICONFLOW_API_KEY=sk-your-api-key-here

# ElevenLabs TTS（可选）
ELEVENLABS_API_KEY=your-elevenlabs-key
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM

# Gemini API（可选，用于biography功能）
GEMINI_API_KEY=your-gemini-key
```

### 3. 配置前端

```bash
cd ../frontend
npm install
```

### 4. 启动服务

**方式一：使用启动脚本（推荐）**

```bash
# 返回项目根目录
cd ..
chmod +x start.sh
./start.sh
```

**方式二：手动启动**

```bash
# 终端1：启动后端
cd backend
python3 main.py

# 终端2：启动前端
cd frontend
npm run dev
```

### 5. 访问应用

- **对话界面**（老年人端）：http://localhost:3000
- **智能仪表盘**（家属端）：http://localhost:3000/dashboard/insights.html
- **API文档**：http://localhost:8000/docs

---

## 📱 使用指南

### 对话测试（伴侣智能体）

1. 打开 http://localhost:3000
2. 点击 **"呼叫小雅"**
3. 点击麦克风按钮开始说话
4. 进行5-10轮自然对话

**示例对话：**
- "今天天气真好"
- "我今天做了红烧肉"
- "我孙子叫小明"
- "我...嗯...我记不太清了"

**体验亮点：**
- ✅ 对话自然、温暖
- ✅ 不会问"今天星期几"之类的测试问题
- ✅ 会用开放式问题引导对话

### 深度分析（分析智能体）

1. 打开 http://localhost:3000/dashboard/insights.html
2. 点击 **"🔬 进行深度分析"** 按钮
3. 等待20-60秒（AI正在分析）
4. 查看详细报告：
   - 10个临床语言生物标记物评分
   - 每个指标的理由和原始引文
   - 整体认知风险评估
   - 情感分析和建议

---

## 📊 API端点

### 对话相关

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/chat` | POST | 发送音频，获取AI回复 |
| `/api/conversations` | GET | 获取对话历史 |

### 分析相关

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/dashboard/insights` | GET | 生成深度分析报告 |
| `/api/generate_biography` | GET | 生成人生纪要 |

### 配置相关

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/config` | GET | 检查API配置状态 |
| `/` | GET | 系统信息 |

---

## 📁 项目结构

```
AI_For_old/
├── backend/                    # 后端服务
│   ├── main.py                # FastAPI入口
│   ├── ai_services.py         # 双层智能体实现
│   ├── database.py            # SQLite数据库
│   ├── vector_store.py        # ChromaDB向量存储
│   ├── requirements.txt       # Python依赖
│   └── .env.example           # 环境变量模板
├── frontend/                   # 前端应用
│   ├── src/
│   │   ├── components/
│   │   │   ├── IdleView.jsx   # 待机界面
│   │   │   ├── InCallView.jsx # 通话界面
│   │   │   └── VoiceActivityDetector.jsx
│   │   ├── App.jsx            # 主应用
│   │   └── main.jsx           # React入口
│   ├── public/
│   │   └── dashboard/
│   │       └── insights.html  # 智能仪表盘
│   ├── package.json           # Node依赖
│   └── vite.config.js         # Vite配置
├── start.sh                   # 启动脚本
├── .gitignore                 # Git忽略文件
└── README.md                  # 项目文档
```

---

## 🎯 核心功能

### ✅ 已实现

- [x] 语音识别（STT）- 硅基流动 TeleAI ASR
- [x] 伴侣智能体对话 - Qwen2.5-7B
- [x] 分析智能体临床评估 - Qwen2.5-7B
- [x] 10个临床语言生物标记物分析
- [x] 智能仪表盘可视化
- [x] RAG长期记忆（ChromaDB）
- [x] 对话历史存储（SQLite）
- [x] iOS风格通话UI

### 🚧 待优化

- [ ] 语音合成（TTS）- ElevenLabs集成
- [ ] 多用户支持（user_id管理）
- [ ] 纵向趋势分析（时间序列）
- [ ] 家属微信推送通知
- [ ] PDF报告导出
- [ ] 实时WebSocket通信

---

## 🔬 技术亮点

### 1. 双层多智能体架构

- **架构优雅性**：通过分离对话层和分析层，实现"温暖陪伴"和"客观分析"的完美平衡
- **System Prompt隔离**：两个LLM使用同一模型但完全不同的prompt和温度参数
- **角色隔离**：对话层永远不知道分析的存在，用户无测试感

### 2. 隐式激发策略

- **非侵入式设计**：通过自然对话激发认知数据，而非传统测试
- **基于临床研究**：策略映射自标准化认知测试（VFT、Cookie Theft Test等）
- **用户体验优先**：老年人感受到的是温暖陪伴，而非冰冷检测

### 3. 临床级分析

- **科学依据**：10个生物标记物基于阿尔茨海默症早期检测研究
- **量化评估**：1-7分评分制，每个指标都有理由和引文
- **纵向追踪**：支持长期数据积累和趋势分析

### 4. RAG记忆架构

- **双重使命**：同一LTM系统服务对话个性化和纵向分析
- **高效检索**：ChromaDB向量数据库实现语义搜索
- **成本优化**：避免全量历史注入，降低Token消耗

---

## 📝 开发日志

### 2025-01-XX

- ✅ 实现双层多智能体架构
- ✅ 伴侣智能体System Prompt优化（隐式激发策略）
- ✅ 分析智能体System Prompt优化（10个生物标记物）
- ✅ 移除所有模拟数据，强制真实LLM调用
- ✅ 智能仪表盘UI重构（临床生物标记物可视化）
- ✅ 从讯飞API切换到硅基流动API（简化集成）

---

## 🤝 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 👨‍💻 作者

**Azurboy**
- GitHub: [@Azurboy](https://github.com/Azurboy)
- 项目仓库: [AI_For_old](https://github.com/Azurboy/AI_For_old)

---

## 🙏 致谢

- **硅基流动（SiliconFlow）**：提供优质的LLM和STT API
- **Qwen团队**：开源优秀的Qwen2.5模型
- **ChromaDB**：提供高效的向量数据库
- **FastAPI & React**：提供现代化的开发框架

---

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- GitHub Issues: [提交Issue](https://github.com/Azurboy/AI_For_old/issues)
- Email: [你的邮箱]

---

<div align="center">

**用AI温暖陪伴，用科技守护健康** ❤️

Made with ❤️ for the "Build Whatever You Want" Hackathon

</div>
