# YuKeSong 前端 - 老人端App

## 功能特性

### ✅ F-001: 状态机 (State Machine)
- `isCalling`: 通话状态（true/false）
- `callState`: 通话阶段（idle/connecting/connected/ended）

### ✅ F-002: 空闲视图 (Idle View)
- 大按钮拨号界面
- 模拟"打电话"体验

### ✅ F-003: 通话中视图 (In-Call View)
- **像素级复刻iOS通话界面**
- 实时通话时长显示
- 静音/扬声器控制
- 红色挂断按钮

### ✅ F-004: 语音活动检测 (VAD)
- **自动检测用户说话**（无需按住）
- 实时音量分析
- 1.5秒静音自动停止录音
- 视觉反馈（录音动画）

## 快速启动

### 1. 安装依赖

```bash
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

前端将在 `http://localhost:3000` 启动。

### 3. 构建生产版本

```bash
npm run build
```

## 技术栈

- **React 18**: UI框架
- **Vite**: 构建工具
- **Web Audio API**: 语音活动检测
- **MediaRecorder API**: 录音功能

## 目录结构

```
frontend/
├── src/
│   ├── components/
│   │   ├── IdleView.jsx          # 空闲界面
│   │   ├── InCallView.jsx        # 通话界面
│   │   └── VoiceActivityDetector.jsx  # VAD组件
│   ├── App.jsx                   # 主应用
│   └── main.jsx                  # 入口文件
├── index.html
└── package.json
```

## API集成

前端通过 `/api/chat` 端点与后端交互：

```javascript
// 发送录音
const formData = new FormData();
formData.append('audio', audioBlob);

const response = await fetch('/api/chat', {
  method: 'POST',
  body: formData
});

// 获取AI回复
const aiText = response.headers.get('X-AI-Text');
const audioBlob = await response.blob();
```

## 演示要点

1. **零门槛交互**: 像打电话一样简单，老人无需学习
2. **VAD驱动**: 自动检测说话，流畅自然
3. **视觉还原**: 像素级模拟iOS通话界面
4. **实时反馈**: 说话时有动画提示

## 浏览器兼容性

- Chrome 80+
- Safari 14+
- Edge 80+

**注意**: 需要HTTPS或localhost环境才能使用麦克风。

