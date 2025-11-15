"""
测试讯飞语音识别API
用于验证API配置是否正确，以及语音识别是否工作
"""
import asyncio
import os
from pathlib import Path
from ai_services import ai_services

async def test_stt_with_file(audio_file_path: str):
    """
    使用音频文件测试STT
    """
    print("=" * 60)
    print("🎤 测试讯飞语音识别API")
    print("=" * 60)
    
    # 检查文件是否存在
    if not os.path.exists(audio_file_path):
        print(f"❌ 音频文件不存在: {audio_file_path}")
        print("\n请提供一个音频文件路径，或使用Web界面测试")
        return
    
    print(f"📁 音频文件: {audio_file_path}")
    
    # 读取音频数据
    with open(audio_file_path, 'rb') as f:
        audio_data = f.read()
    
    print(f"📊 音频大小: {len(audio_data)} bytes")
    print("\n🔄 正在调用讯飞API...")
    print("-" * 60)
    
    # 调用STT
    result = await ai_services.speech_to_text(audio_data)
    
    print("-" * 60)
    print(f"\n✨ 识别结果:")
    print(f"   {result}")
    print("\n" + "=" * 60)


async def test_api_config():
    """
    测试API配置
    """
    print("\n🔧 检查API配置...")
    print("-" * 60)
    
    app_id = os.getenv("XUNFEI_APP_ID", "")
    api_key = os.getenv("XUNFEI_API_KEY", "")
    api_secret = os.getenv("XUNFEI_API_SECRET", "")
    
    if app_id and api_key and api_secret:
        print(f"✅ XUNFEI_APP_ID: {app_id}")
        print(f"✅ XUNFEI_API_KEY: {api_key[:8]}***")
        print(f"✅ XUNFEI_API_SECRET: {api_secret[:8]}***")
    else:
        print("❌ 讯飞API配置不完整")
        print("\n请检查 backend/.env 文件，确保包含:")
        print("  - XUNFEI_APP_ID")
        print("  - XUNFEI_API_KEY")
        print("  - XUNFEI_API_SECRET")
    
    print("-" * 60)


async def main():
    """
    主测试函数
    """
    # 加载环境变量
    from dotenv import load_dotenv
    load_dotenv()
    
    # 检查配置
    await test_api_config()
    
    # 提示用户
    print("\n📝 测试选项:")
    print("   1. 使用自己的音频文件测试")
    print("   2. 使用Web界面测试（推荐）")
    print("\n💡 推荐方式: 启动后端和前端，在浏览器中测试")
    print("   - 后端: python main.py")
    print("   - 前端: cd frontend && npm run dev")
    print("   - 访问: http://localhost:3000")
    
    # 如果有测试音频文件，可以在这里测试
    test_file = "test_audio.wav"  # 替换为你的测试音频文件
    
    if os.path.exists(test_file):
        print(f"\n发现测试文件: {test_file}")
        choice = input("是否使用此文件测试？(y/n): ")
        if choice.lower() == 'y':
            await test_stt_with_file(test_file)
    else:
        print(f"\n如果你有音频文件，可以运行:")
        print(f"   python test_xunfei_stt.py <音频文件路径>")


if __name__ == "__main__":
    import sys
    
    # 支持命令行参数
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        asyncio.run(test_stt_with_file(audio_file))
    else:
        asyncio.run(main())


