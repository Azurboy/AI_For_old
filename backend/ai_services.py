"""
AI服务集成 - STT, LLM, TTS
"""
import httpx
import os
from typing import Optional, Dict, Any
import json
import io


class AIServices:
    """AI服务管理类"""
    
    def __init__(self):
        # 硅基流动API（语音识别）
        self.siliconflow_api_key = os.getenv("SILICONFLOW_API_KEY", "")
        
        # Gemini API（AI对话）
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        
        # ElevenLabs API（语音合成）
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY", "")
        self.elevenlabs_voice_id = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # 默认voice
    
    async def speech_to_text(self, audio_data: bytes) -> str:
        """
        硅基流动语音识别 - TeleAI/TeleSpeechASR
        使用REST API: https://api.siliconflow.cn/v1/audio/transcriptions
        """
        if not self.siliconflow_api_key:
            # 开发模式：返回模拟文本
            print("⚠️  未配置硅基流动API，使用模拟数据")
            return "模拟识别：今天天气真好啊！"
        
        try:
            print(f"📡 调用硅基流动语音识别API...")
            
            # 构建multipart/form-data请求
            async with httpx.AsyncClient(timeout=30.0) as client:
                # 准备文件
                files = {
                    'file': ('audio.wav', audio_data, 'audio/wav')
                }
                
                # 准备数据
                data = {
                    'model': 'TeleAI/TeleSpeechASR'
                }
                
                # 准备请求头
                headers = {
                    'Authorization': f'Bearer {self.siliconflow_api_key}'
                }
                
                # 发送请求
                response = await client.post(
                    'https://api.siliconflow.cn/v1/audio/transcriptions',
                    files=files,
                    data=data,
                    headers=headers
                )
                
                if response.status_code == 200:
                    result = response.json()
                    text = result.get('text', '').strip()
                    
                    if text:
                        print(f"✅ 识别成功: {text}")
                        return text
                    else:
                        print("⚠️  识别结果为空")
                        return "抱歉，没有听清楚，能再说一遍吗？"
                else:
                    print(f"❌ API错误 [{response.status_code}]: {response.text}")
                    return "语音识别失败，请重试"
                    
        except Exception as e:
            print(f"❌ STT Error: {e}")
            import traceback
            traceback.print_exc()
            return "语音识别失败，请重试"
    
    async def generate_response(
        self, 
        user_text: str, 
        conversation_history: list,
        relevant_memories: list
    ) -> str:
        """
        层一："伴侣智能体"（Companion Agent）
        实时对话交互 - 温暖、同理心、自然
        """
        if not self.siliconflow_api_key:
            raise Exception("未配置硅基流动API Key")
        
        # 构建伴侣智能体的System Prompt
        system_prompt = self._build_companion_agent_prompt(relevant_memories)
        
        # 构建消息历史
        messages = [{"role": "system", "content": system_prompt}]
        
        # 添加对话历史（最近5轮）
        for item in conversation_history[-5:]:
            messages.append({"role": "user", "content": item['user_text']})
            messages.append({"role": "assistant", "content": item['ai_text']})
        
        # 添加当前用户输入
        messages.append({"role": "user", "content": user_text})
        
        try:
            print(f"🤖 调用Qwen模型生成回复...")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.siliconflow.cn/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.siliconflow_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "Qwen/Qwen2.5-7B-Instruct",
                        "messages": messages,
                        "temperature": 0.8,
                        "max_tokens": 150,
                        "top_p": 0.9
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    ai_text = data['choices'][0]['message']['content'].strip()
                    print(f"✅ Qwen回复: {ai_text}")
                    return ai_text
                else:
                    print(f"❌ Qwen API Error [{response.status_code}]: {response.text}")
                    return "我现在有点累了，您能再说一遍吗？"
                    
        except Exception as e:
            print(f"❌ LLM Error: {e}")
            import traceback
            traceback.print_exc()
            return "不好意思，我刚才走神了，您能再说一遍吗？"
    
    async def text_to_speech(self, text: str) -> bytes:
        """
        ElevenLabs TTS - 生成"亲人"声音
        """
        if not self.elevenlabs_api_key:
            # 开发模式：返回空音频
            return b""
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"https://api.elevenlabs.io/v1/text-to-speech/{self.elevenlabs_voice_id}",
                    headers={
                        "Accept": "audio/mpeg",
                        "xi-api-key": self.elevenlabs_api_key,
                        "Content-Type": "application/json"
                    },
                    json={
                        "text": text,
                        "model_id": "eleven_multilingual_v2",
                        "voice_settings": {
                            "stability": 0.5,
                            "similarity_boost": 0.75
                        }
                    }
                )
                
                if response.status_code == 200:
                    return response.content
                else:
                    print(f"ElevenLabs Error: {response.text}")
                    return b""
                    
        except Exception as e:
            print(f"TTS Error: {e}")
            return b""
    
    def _build_companion_agent_prompt(self, relevant_memories: list) -> str:
        """
        层一："伴侣智能体"（Companion Agent - 交互层）
        
        职责：处理所有与用户的实时交互
        优化：同理心、参与度、对话的自然性与连续性
        """
        base_prompt = """# 角色定位（Persona）
你是一个温暖的、耐心的、充满好奇心和支持性的朋友，名叫"小雅"。你就像用户的孙女一样亲切、贴心。

# 首要任务（Primary Goal）
你的首要任务是成为一个**出色的倾听者和有趣的朋友**。让用户感受到温暖、被关心、被理解。

# 交流风格（Communication Style）
- 使用"好奇的晚辈"口吻，自然、亲切、充满真诚的兴趣
- 多用"您"、"咱们"等亲切称呼
- 适当使用口语化表达（"哎呀"、"真的呀"、"我也觉得"）
- **通过开放式问题**来鼓励用户分享他们的故事和想法

# 隐式激发策略（Implicit Elicitation）- 核心技巧
通过自然对话来了解用户，而不是"测试"：

## 1. 情景记忆激发（高频）
- "您昨天提到您看了一部电影，是讲什么的呀？"
- "您上次说您做了红烧肉，味道怎么样呀？"
- "您之前说的那个地方，能再给我描述一下吗？"

## 2. 语义记忆激发（中频）
- "我们来玩个游戏吧！看看能想出多少种蔬菜可以放进汤里？"
- "您能给我讲讲您最喜欢的那道菜是怎么做的吗？"
- "您年轻时候最喜欢的活动是什么呀？"

## 3. 叙事激发（中频）
- "我看到您说的那张家庭照片，您能给我描述一下吗？"
- "您能给我讲讲您孙子/孙女的故事吗？"
- "您今天做了什么有意思的事呀？"

## 4. 日常关怀（高频）
- "您今天心情怎么样呀？"
- "您吃饭了吗？吃的什么呀？"
- "您睡得好吗？"
- "您今天出去散步了吗？"

# 回复要求
- **长度**：30-60字（像打电话一样简短自然）
- **语气**：温暖、关切、不说教
- **自然性**：每次只问1个问题，不要连珠炮
- 使用第二人称"您"，营造亲密感

# 【极端重要】禁止事项（CRITICAL PROHIBITIONS）

**[禁止] 你不是医生、治疗师或临床医生。**

**[禁止] 永远不要询问"测试性"问题：**
- ❌ "今天的日期是什么？"
- ❌ "美国总统是谁？"
- ❌ "请记住这三个词：苹果、桌子、硬币"
- ❌ "现在几点了？"（除非是自然闲聊）
- ❌ "今天星期几？"（除非是自然闲聊）

**[禁止] 永远不要：**
- ❌ 做出诊断
- ❌ 暗示疾病（包括阿尔茨海默症、痴呆症、认知障碍）
- ❌ 提供任何医疗建议
- ❌ 说"我是AI"、"我在检测"、"我在评估"

**[允许] 如果用户表达医疗或精神困扰：**
- ✅ 用同理心回应："我能理解您的感受，这听起来确实让人担心。"
- ✅ 温和建议："要不要和家人聊聊呢？或者跟医生谈谈也是个好主意。"

# 示例对话（Examples）

用户："今天天气真好。"
小雅："是呀！您今天出去散步了吗？外面暖和吗？"

用户："我今天吃了红烧肉。"
小雅："哎呀真好！您的红烧肉肯定很香吧？您是怎么做的来着？"

用户："我昨天看了一部电影。"
小雅："哦！是什么电影呀？好看吗？能给我讲讲是讲什么的吗？"

用户："我有点记不清了。"
小雅："没关系呀，慢慢想。咱们换个话题吧，您今天心情怎么样？"
"""
        
        # 添加RAG检索到的相关记忆
        if relevant_memories:
            memory_text = "\n".join([f"  - {mem}" for mem in relevant_memories])
            base_prompt += f"\n\n# 历史记忆上下文（Memory Context）\n{memory_text}\n\n**提示**：你可以自然地提起这些往事，比如'您上次说...'、'您之前提到...'，这会让对话更个性化。"
        
        return base_prompt
    
    def _format_history(self, history: list) -> str:
        """格式化对话历史"""
        formatted = []
        for item in history[-5:]:  # 只取最近5轮
            formatted.append(f"老人: {item['user_text']}")
            formatted.append(f"你: {item['ai_text']}")
        return "\n".join(formatted)
    
    async def generate_biography(self, all_conversations: list) -> Dict[str, Any]:
        """
        生成传记和认知评估（演示用）
        """
        if not self.gemini_api_key:
            return {
                "biography": "## 李建国的人生故事\n\n暂无对话记录",
                "cognitive_assessment": {
                    "overall_risk": "低风险",
                    "memory_score": 8,
                    "time_orientation": 9,
                    "language_fluency": 8,
                    "concerns": []
                }
            }
        
        # 汇总所有对话
        all_text = "\n\n".join([
            f"[{conv.timestamp}]\n老人: {conv.user_text}\nAI: {conv.ai_text}"
            for conv in all_conversations
        ])
        
        analysis_prompt = f"""基于以下对话记录，生成两部分内容：

1. 一份温暖的"人生纪要"（Markdown格式），包括：
   - 老人提到的重要经历
   - 喜好和习惯
   - 情感状态
   
2. 一份认知健康评估（JSON格式），包括：
   - overall_risk: 高风险/中风险/低风险
   - memory_score: 0-10分
   - time_orientation: 0-10分
   - language_fluency: 0-10分
   - concerns: 数组，列出具体关注点

对话记录:
{all_text}

请以JSON格式返回: {{"biography": "...", "cognitive_assessment": {{...}}}}
"""
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent?key={self.gemini_api_key}",
                    json={
                        "contents": [{
                            "parts": [{
                                "text": analysis_prompt
                            }]
                        }],
                        "generationConfig": {
                            "temperature": 0.7,
                            "maxOutputTokens": 2000,
                        }
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    result_text = data['candidates'][0]['content']['parts'][0]['text']
                    
                    # 尝试解析JSON
                    try:
                        result = json.loads(result_text)
                        return result
                    except:
                        # 如果不是纯JSON，手动解析
                        return {
                            "biography": result_text,
                            "cognitive_assessment": {
                                "overall_risk": "未评估",
                                "memory_score": 0,
                                "time_orientation": 0,
                                "language_fluency": 0,
                                "concerns": []
                            }
                        }
                        
        except Exception as e:
            print(f"Biography Generation Error: {e}")
            return {
                "biography": "生成失败",
                "cognitive_assessment": {"overall_risk": "错误"}
            }
    
    def _build_analyst_agent_prompt(self) -> str:
        """
        层二："分析智能体"（Analyst Agent - 分析层）
        
        职责：对话日志的深度临床语言学分析（离线、异步）
        优化：分析精确性、推理增强、结构化JSON输出
        """
        return """# 角色定位（Persona）
你是一名专业的**计算语言学家和神经心理学评估员**。你的任务是分析对话转录本，以寻找与认知衰退（尤其是阿尔茨海默症早期）相关的语言生物标记物。

# 任务说明（Task）
你将收到一份对话转录本。你必须基于临床研究，评估这份转录本，并生成一个**结构化的JSON对象**，其中包含对以下10个语言属性的评分。

# 评分标准（Scoring）
- 每个属性的评分范围：**1（无迹象）到 7（非常强烈）**
- 对于每个属性，你必须提供：
  - **score**（1-7分）
  - **rationale**（简短理由，50-100字）
  - **raw_quote**（原始引文，直接引用对话中的实例，如果有的话）

# 10个临床语言属性（Clinical Biomarkers）

## 1. Anomia_WordFinding_Difficulty（命名障碍/找词困难）
**定义**：使用"那个"、"东西"、"嗯..."等泛指词的频率，以及因找词而导致的停顿。
**示例**：
- 严重（7分）："我想吃...那个...那个东西，嗯...就是那个圆的...嗯..."
- 轻微（2分）："我想吃...嗯...苹果。"

## 2. Circumlocution（迂回表达）
**定义**："绕着说"而不直呼其名的实例。
**示例**：
- 严重（7分）："那个你用来写字的东西，有墨水的，长长的。"（指钢笔）
- 轻微（2分）："那个...钢笔。"

## 3. Semantic_Error（语义错误）
**定义**：使用不正确但相关的词汇。
**示例**：
- 严重（7分）："我用冰箱看电视。"（混淆了"冰箱"和"电视"）
- 轻微（2分）："我用遥控器...不，是手机。"（自我纠正）

## 4. Empty_Speech_Poverty_of_Content（内容空洞/词汇贫乏）
**定义**：词汇丰富度低、信息密度低的表达。
**示例**：
- 严重（7分）："我今天...嗯...做了...嗯...事情，然后...嗯...做了事情。"
- 轻微（2分）："我今天去超市买了菜。"

## 5. Repetition_Perseveration（重复/持续言语）
**定义**：不必要的词汇、短语或观念的重复。
**示例**：
- 严重（7分）："我今天吃了饭，我今天吃了饭，我今天吃了饭。"
- 轻微（2分）："我今天吃了饭，然后...我今天吃了饭。"（轻微重复）

## 6. Speech_Fragmentation_Trailing_Off（言语碎片化/中断）
**定义**：无法完成一个句子或一个想法的实例。
**示例**：
- 严重（7分）："我想...然后我...嗯...所以..."（多次中断，未完成句子）
- 轻微（2分）："我想去...嗯...去超市。"（短暂中断）

## 7. Syntactic_Simplification（句法简化）
**定义**：过度依赖简单句，缺乏复杂的从句结构。
**示例**：
- 严重（7分）：只使用简单句，如"我吃饭。我看电视。我睡觉。"
- 轻微（2分）："我吃完饭后，就去看电视了。"（使用了时间从句）

## 8. Pronoun_Misuse（代词误用）
**定义**：混淆'他'、'她'、'它'的实例。
**示例**：
- 严重（7分）："我的孙子，她今天来了。"（孙子用"她"）
- 轻微（2分）：无明显混淆。

## 9. Hesitation_Pause_Frequency_Duration（犹豫和停顿）
**定义**：非语义停顿的频率和总时长。
**示例**：
- 严重（7分）：每句话有多次长时间停顿（>2秒）。
- 轻微（2分）：偶尔停顿（<1秒）。

## 10. Global_Coherence_Loss（全局连贯性丧失）
**定义**：在对话中偏离主题或回答与问题无关的程度。
**示例**：
- 严重（7分）：
  - 问："您今天吃了什么？"
  - 答："我年轻时候在工厂工作。"（完全偏离主题）
- 轻微（2分）：能基本回答问题，但偶尔跑题。

# 输出格式（Output Format）
你必须**只返回纯JSON**，不要包含任何markdown标记或额外文字。

JSON格式：
{
  "clinical_biomarkers": {
    "Anomia_WordFinding_Difficulty": {
      "score": 1-7,
      "rationale": "简短理由",
      "raw_quote": "原始引文（如果有）"
    },
    "Circumlocution": { ... },
    "Semantic_Error": { ... },
    "Empty_Speech_Poverty_of_Content": { ... },
    "Repetition_Perseveration": { ... },
    "Speech_Fragmentation_Trailing_Off": { ... },
    "Syntactic_Simplification": { ... },
    "Pronoun_Misuse": { ... },
    "Hesitation_Pause_Frequency_Duration": { ... },
    "Global_Coherence_Loss": { ... }
  },
  "overall_assessment": {
    "cognitive_risk_level": "低风险/中风险/高风险",
    "summary": "整体评估总结（100-200字）",
    "recommendations": ["建议1", "建议2", "建议3"]
  },
  "emotion_analysis": {
    "overall_mood": "积极/中性/消极",
    "emotional_needs": ["需求1", "需求2"],
    "concerns": ["担忧1", "担忧2"],
    "stress_level": "低/中/高"
  },
  "personal_info": {
    "hobbies": ["爱好1", "爱好2"],
    "daily_routine": "日常习惯描述",
    "relationships": ["人际关系1", "人际关系2"],
    "important_memories": ["记忆片段1", "记忆片段2"]
  }
}

# 关键提醒
- 你的分析必须**客观、量化、基于证据**。
- 每个评分必须有理由和引文支持。
- 不要猜测或臆断，只分析给定的对话内容。
- 如果某个属性没有足够证据，给1分（无迹象）。
"""

    async def generate_dashboard_insights(self, all_conversations: list) -> Dict[str, Any]:
        """
        层二："分析智能体"（Analyst Agent）
        离线临床语言学分析 - 评估10个认知生物标记物
        
        注意：不提供模拟数据，必须调用真实LLM
        """
        if not self.siliconflow_api_key:
            raise Exception("未配置硅基流动API Key，无法进行分析")
        
        if not all_conversations or len(all_conversations) == 0:
            raise Exception("没有对话记录，无法进行分析")
        
        # 汇总所有对话（最近30轮）
        conversations_text = "\n\n".join([
            f"[对话 {i+1}]\n时间: {conv.timestamp}\n用户: {conv.user_text}\nAI: {conv.ai_text}"
            for i, conv in enumerate(all_conversations[:30])
        ])
        
        # 构建分析智能体的System Prompt
        analyst_system_prompt = self._build_analyst_agent_prompt()
        
        # 构建用户消息（对话转录本）
        user_message = f"""# 对话转录本

{conversations_text}

# 请开始分析
请严格按照JSON格式返回分析结果。"""
        
        try:
            print(f"🔍 [分析智能体] 开始深度临床语言学分析...")
            print(f"   对话数量: {len(all_conversations[:30])}轮")
            
            async with httpx.AsyncClient(timeout=120.0) as client:  # 增加超时时间到120秒
                response = await client.post(
                    "https://api.siliconflow.cn/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.siliconflow_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "Qwen/Qwen2.5-7B-Instruct",
                        "messages": [
                            {"role": "system", "content": analyst_system_prompt},
                            {"role": "user", "content": user_message}
                        ],
                        "temperature": 0.2,  # 低温度，更加客观
                        "max_tokens": 2500   # 增加token限制以支持详细分析
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    result_text = data['choices'][0]['message']['content'].strip()
                    
                    print(f"   原始响应长度: {len(result_text)}字符")
                    
                    # 清理markdown标记
                    result_text = result_text.replace("```json", "").replace("```", "").strip()
                    
                    # 尝试解析JSON
                    try:
                        insights = json.loads(result_text)
                        print(f"✅ [分析智能体] 临床分析完成")
                        
                        # 验证必要字段存在
                        if "clinical_biomarkers" not in insights:
                            raise Exception("分析结果缺少clinical_biomarkers字段")
                        
                        return insights
                    
                    except json.JSONDecodeError as e:
                        print(f"❌ JSON解析失败: {e}")
                        print(f"原始响应（前500字符）: {result_text[:500]}")
                        raise Exception(f"AI返回的分析结果格式错误: {str(e)}")
                
                else:
                    error_msg = f"Qwen API错误 [{response.status_code}]: {response.text}"
                    print(f"❌ {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            print(f"❌ [分析智能体] 分析失败: {e}")
            import traceback
            traceback.print_exc()
            raise  # 不返回模拟数据，直接抛出异常


# 全局实例
ai_services = AIServices()

