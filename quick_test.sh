#!/bin/bash

# 快速测试脚本 - 验证讯飞API配置

echo "🧪 讯飞语音识别 - 快速测试"
echo "================================"
echo ""

# 检查.env文件
if [ ! -f "backend/.env" ]; then
    echo "❌ 未找到 backend/.env 文件"
    echo "正在创建..."
    cat > backend/.env << 'EOF'
XUNFEI_APP_ID=62fed114
XUNFEI_API_KEY=23c852ec7b677eb9b7f28fbfe9527da7
XUNFEI_API_SECRET=Njk5NGU1M2MxMzNiMmNhNjJlNzZjNGVm
GEMINI_API_KEY=your_gemini_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
EOF
    echo "✅ .env 文件已创建"
fi

echo "📋 API配置检查:"
echo "--------------------------------"
cd backend
python3 test_xunfei_stt.py
cd ..

echo ""
echo "================================"
echo "✨ 下一步:"
echo ""
echo "1️⃣  启动后端 (终端1):"
echo "   cd backend && python3 main.py"
echo ""
echo "2️⃣  启动前端 (终端2):"
echo "   cd frontend && npm run dev"
echo ""
echo "3️⃣  浏览器测试:"
echo "   访问 http://localhost:3000"
echo "   点击'呼叫小雅'，对着麦克风说话"
echo ""
echo "📖 详细步骤请查看: HOW_TO_TEST.md"
echo "================================"


