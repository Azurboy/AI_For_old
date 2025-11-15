# 🎉 欢迎使用语客颂！

恭喜！你的黑客松项目已经完整搭建完成。

---

## 🚀 立即开始（3个步骤）

### 1️⃣ 安装依赖

```bash
# 后端依赖
cd backend
pip3 install -r requirements.txt
cd ..

# 前端依赖
cd frontend
npm install
cd ..
```

### 2️⃣ 配置API密钥（可选）

```bash
cd backend
cp .env.example .env
# 编辑 .env 文件，填入你的API密钥
```

**注意**: 即使不配置API密钥，系统也能运行（使用模拟数据）！

### 3️⃣ 启动项目

**方法A: 一键启动（推荐）**
```bash
./start.sh
```

**方法B: 手动启动**
```bash
# 终端1 - 后端
cd backend && python3 main.py

# 终端2 - 前端
cd frontend && npm run dev

# 终端3 - 仪表盘
cd dashboard && python3 -m http.server 8080
```

---

## 🎯 访问地址

启动成功后，打开浏览器访问：

- 📱 **老人端App**: http://localhost:3000
- 📊 **演示仪表盘**: http://localhost:8080
- 🔌 **后端API**: http://localhost:8000/docs

---

## 🎬 演示流程

### 快速演示（30秒）

1. 打开 http://localhost:3000
2. 点击"呼叫小雅"按钮
3. 允许麦克风权限
4. 说话测试VAD自动检测
5. 打开 http://localhost:8080 查看仪表盘

### 完整演示（3分钟）

查看 **DEMO_GUIDE.md**，里面有详细的演讲稿和演示脚本！

---

## 📊 生成演示数据

为了让仪表盘看起来更有说服力，运行：

```bash
cd backend
python3 seed_demo_data.py
```

这会生成20条对话记录和7条洞见，然后刷新仪表盘就能看到效果！

---

## 🔑 API密钥获取

### Gemini 1.5 Pro （必需）
1. 访问: https://ai.google.dev/
2. 点击"Get API Key"
3. 复制密钥到 `backend/.env` 的 `GEMINI_API_KEY`

### ElevenLabs TTS （可选）
1. 访问: https://elevenlabs.io/
2. 注册账号
3. 复制API Key到 `ELEVENLABS_API_KEY`
4. 选择一个Voice ID（或使用默认的）

### 讯飞STT （可选）
1. 访问: https://www.xfyun.cn/
2. 创建应用
3. 获取AppID、API Key、API Secret
4. 填入对应字段

**注意**: 讯飞STT需要额外实现WebSocket连接，当前为占位符。

---

## ✅ 功能清单

### ✅ 已完成

#### 后端
- [x] FastAPI服务器
- [x] SQLite本地数据库
- [x] ChromaDB向量存储
- [x] AI服务框架（STT/LLM/TTS）
- [x] 核心对话端点 `/api/chat`
- [x] 传记生成端点 `/api/generate_biography`
- [x] RAG记忆检索
- [x] 非侵入式评估Prompt

#### 前端
- [x] React 18 + Vite
- [x] 状态机管理（isCalling + callState）
- [x] 空闲视图（大按钮拨号）
- [x] 通话视图（像素级iOS界面）
- [x] VAD语音活动检测
- [x] 实时音频播放
- [x] 说话动画提示

#### 仪表盘
- [x] 响应式布局
- [x] 统计卡片（4个关键指标）
- [x] 认知健康评估面板
- [x] 人生纪要面板（Markdown渲染）
- [x] 一键刷新数据

#### 文档
- [x] 项目README
- [x] 快速启动指南
- [x] 演示指南（3分钟脚本）
- [x] API文档
- [x] 项目结构说明

---

## 🎯 黑客松评分对应

| 功能 | 状态 | 评分点 |
|------|------|--------|
| VAD自动录音 | ✅ | P0: 流畅对话 |
| iOS通话界面 | ✅ | P0: 零门槛 |
| 方言识别 | 🔌 框架就绪 | P1: 技术难度 |
| 声音克隆 | 🔌 框架就绪 | P1: 情感连接 |
| RAG记忆 | ✅ | P2: AI智能 |
| 非侵入评估 | ✅ | P2: 产品洞察 |
| 传记生成 | ✅ | P3: 价值展示 |
| 认知评估 | ✅ | P3: 医疗价值 |

🔌 = AI API占位符已搭建，填入密钥即可使用

---

## 📚 核心文档导航

### 快速参考
- **立即启动** → `QUICKSTART.md`
- **演示准备** → `DEMO_GUIDE.md`
- **项目总览** → `README.md`

### 技术文档
- **API接口** → `API_DOCUMENTATION.md`
- **项目结构** → `PROJECT_STRUCTURE.md`
- **后端说明** → `backend/README.md`
- **前端说明** → `frontend/README.md`
- **仪表盘** → `dashboard/README.md`

---

## 🐛 故障排除

### 问题1: `pip install` 失败
**解决**: 使用虚拟环境
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 问题2: 前端无法连接后端
**检查**: 
1. 后端是否在8000端口运行
2. 浏览器控制台是否有CORS错误
3. vite.config.js的proxy配置是否正确

### 问题3: 麦克风权限被拒绝
**解决**:
- Chrome: 点击地址栏左侧🔒，允许麦克风
- Safari: 偏好设置 → 网站 → 麦克风
- 确保使用HTTPS或localhost

### 问题4: 没有AI回复
**检查**:
1. 后端日志是否有错误
2. .env文件中的API密钥是否正确
3. 如果没配置API，应该看到模拟回复

---

## 💡 演示技巧

### 前期准备
1. ✅ 运行 `seed_demo_data.py` 生成数据
2. ✅ 测试麦克风权限
3. ✅ 准备好演讲稿（DEMO_GUIDE.md）
4. ✅ 投屏两个页面（App + 仪表盘）

### 演示重点
1. **开场**: 问题引入（爸妈不会用ChatGPT）
2. **核心**: 展示VAD自动检测（强调"零门槛"）
3. **亮点**: 仪表盘刷新（展示AI洞察力）
4. **结尾**: 情感升华（用打电话守护爱）

### 应对提问
- 隐私？→ 本地存储
- 市场？→ 2.8亿老人
- 商业模式？→ B2C订阅 + B2B养老机构

---

## 🏆 接下来做什么？

### 黑客松期间
1. [ ] 配置Gemini API密钥
2. [ ] 生成演示数据
3. [ ] 练习演示流程
4. [ ] 准备PPT（可选）

### 黑客松后
1. [ ] 实现讯飞STT完整集成
2. [ ] 添加声音克隆上传功能
3. [ ] 开发儿孙端App
4. [ ] 部署到云端

---

## 🎉 祝你好运！

你已经拥有了一个完整、可演示的MVP！

**记住我们的愿景**:
> "用打电话守护爱，让AI成为温暖的陪伴者。"

**冲击第一名！** 🚀

---

**有问题？**
- 查看各个README文档
- 检查后端日志
- 浏览器控制台查看错误

**项目已就绪，开始你的表演吧！** 🎭

