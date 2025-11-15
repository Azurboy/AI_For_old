# ⚡ 5分钟快速启动

## 🚀 方法1: 一键启动（推荐）

```bash
chmod +x start.sh
./start.sh
```

然后访问：
- 👴 **老人端App**: http://localhost:3000
- 📊 **演示仪表盘**: http://localhost:8080
- 🔌 **后端API文档**: http://localhost:8000/docs

---

## 🔧 方法2: 分步启动

### Step 1: 配置环境

```bash
# 复制环境变量模板
cp backend/.env.example backend/.env

# 编辑 .env 文件（可选，有默认模拟数据）
# 填入你的API密钥：GEMINI_API_KEY, ELEVENLABS_API_KEY等
```

### Step 2: 启动后端

```bash
cd backend
pip3 install -r requirements.txt
python3 main.py
```

后端运行在 `http://localhost:8000`

### Step 3: 启动前端

**新开一个终端：**

```bash
cd frontend
npm install
npm run dev
```

前端运行在 `http://localhost:3000`

### Step 4: 启动仪表盘

**新开一个终端：**

```bash
cd dashboard
python3 -m http.server 8080
```

仪表盘运行在 `http://localhost:8080`

---

## ✅ 测试流程

### 1. 测试前端App
1. 打开 http://localhost:3000
2. 点击"呼叫小雅"
3. 允许麦克风权限
4. 说话测试VAD检测
5. 观察AI回复

### 2. 测试仪表盘
1. 打开 http://localhost:8080
2. 点击"刷新数据"
3. 查看生成的传记和评估

### 3. 测试API（可选）
访问 http://localhost:8000/docs 查看API文档

---

## 🔑 API密钥配置（可选）

如果不配置API密钥，系统会使用**模拟数据**，仍然可以演示完整流程。

### 获取API密钥

#### Gemini 1.5 Pro (必需)
1. 访问 https://ai.google.dev/
2. 创建API密钥
3. 填入 `GEMINI_API_KEY`

#### ElevenLabs TTS (可选)
1. 访问 https://elevenlabs.io/
2. 注册账号
3. 获取API Key和Voice ID
4. 填入 `ELEVENLABS_API_KEY` 和 `ELEVENLABS_VOICE_ID`

#### 讯飞STT (可选)
1. 访问 https://www.xfyun.cn/
2. 创建应用
3. 获取 AppID、API Key、API Secret
4. 填入 `XUNFEI_*` 相关配置

**注意**: 讯飞STT需要实现WebSocket连接，当前代码为占位符。

---

## ❓ 常见问题

### Q1: `pip install` 失败
**A**: 使用虚拟环境：
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# 或 venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Q2: `npm install` 很慢
**A**: 使用国内镜像：
```bash
npm install --registry=https://registry.npmmirror.com
```

### Q3: 前端无法访问后端API
**A**: 检查CORS配置，后端已允许所有来源。确保后端在8000端口运行。

### Q4: 麦克风权限被拒绝
**A**: 
- Chrome需要HTTPS或localhost
- Safari需要用户手动允许
- 检查浏览器设置 → 隐私 → 麦克风

### Q5: 没有声音回复
**A**: 
- 如果未配置ElevenLabs API，返回的是空音频
- 可以通过header `X-AI-Text` 看到文本回复
- 配置API后即可获得语音

---

## 📱 手机测试

### iOS/Android测试
1. 确保手机和电脑在同一WiFi
2. 获取电脑IP地址：
   ```bash
   # Mac
   ifconfig | grep "inet "
   
   # Windows
   ipconfig
   ```
3. 手机浏览器访问 `http://<电脑IP>:3000`

**注意**: 手机端需要HTTPS才能使用麦克风，可以使用ngrok等工具。

---

## 🎯 下一步

完成启动后，查看：
- 📖 **完整文档**: `README.md`
- 🎬 **演示指南**: `DEMO_GUIDE.md`
- 🔧 **后端API**: `backend/README.md`
- 🎨 **前端说明**: `frontend/README.md`

---

**祝你使用愉快！** 🎉

