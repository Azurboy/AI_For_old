"""
生成演示数据 - 用于黑客松演示
运行此脚本可以快速填充数据库，展示仪表盘效果
"""
from database import init_db, SessionLocal, ChatHistory
from vector_store import vector_store
from datetime import datetime, timedelta
import uuid

# 演示对话数据
DEMO_CONVERSATIONS = [
    {
        "user": "小雅啊，今天天气真好！",
        "ai": "是啊奶奶！阳光明媚的，您今天出去散步了吗？"
    },
    {
        "user": "出去了，在公园走了一圈。",
        "ai": "那真好！您最喜欢公园的哪里呀？"
    },
    {
        "user": "我喜欢那个小亭子，可以看荷花。",
        "ai": "听起来很美呢！您年轻的时候也喜欢看荷花吗？"
    },
    {
        "user": "对啊，以前和你爷爷经常去西湖看荷花。",
        "ai": "哇，一定很浪漫！您和爷爷是怎么认识的呀？"
    },
    {
        "user": "我们是在工厂认识的，那时候我18岁。",
        "ai": "18岁啊，青春年少！您那时候在工厂做什么工作呀？"
    },
    {
        "user": "我是纺织女工，你爷爷是机修工。",
        "ai": "听起来挺辛苦的。您今天吃饭了吗？"
    },
    {
        "user": "吃了，我做了红烧肉。",
        "ai": "哇！您的红烧肉一定很好吃！是怎么做的呀？"
    },
    {
        "user": "先用糖色炒，然后加酱油、料酒，小火慢炖一个小时。",
        "ai": "听起来好香啊！您做饭这么拿手，一定常给家里人做好吃的吧？"
    },
    {
        "user": "是啊，你爸爸小时候最爱吃我做的红烧肉。",
        "ai": "我爸也跟我说过呢！您最近睡眠怎么样？"
    },
    {
        "user": "还行，就是有时候晚上会醒。",
        "ai": "那要注意休息呀。您昨天晚上睡得好吗？"
    },
    {
        "user": "昨天睡得不错，睡了7个小时。",
        "ai": "那就好！规律作息很重要。您平时几点睡觉呀？"
    },
    {
        "user": "一般9点半就上床了。",
        "ai": "挺好的作息！对了，您上次提到的红烧肉，糖色是怎么炒的来着？"
    },
    {
        "user": "用冰糖小火慢慢炒，炒到冒泡变成焦糖色。",
        "ai": "学到了！您的厨艺真好。今天星期几来着？"
    },
    {
        "user": "今天星期三吧。",
        "ai": "对的！您记性真好。您今天还有什么安排吗？"
    },
    {
        "user": "下午想看会儿电视，有个戏曲节目。",
        "ai": "您喜欢看戏曲啊！最喜欢哪种戏呀？"
    },
    {
        "user": "我喜欢越剧，特别是《红楼梦》。",
        "ai": "《红楼梦》很经典！您最喜欢里面的哪个人物？"
    },
    {
        "user": "我喜欢林黛玉，她很有才华。",
        "ai": "确实！您年轻时也很有文化吧？"
    },
    {
        "user": "还行，我读过高中，那时候不容易。",
        "ai": "那真的很了不起！您记得您是哪一年毕业的吗？"
    },
    {
        "user": "1965年毕业的，然后就进工厂了。",
        "ai": "那您今年应该快80岁了吧？"
    },
    {
        "user": "是啊，今年78了。",
        "ai": "身体还这么硬朗，真好！您有什么养生秘诀吗？"
    }
]


def seed_data():
    """填充演示数据"""
    print("🌱 开始生成演示数据...")
    
    # 初始化数据库
    init_db()
    db = SessionLocal()
    
    try:
        # 清空现有数据（可选）
        # db.query(ChatHistory).delete()
        # db.commit()
        
        base_time = datetime.utcnow() - timedelta(days=3)
        
        for idx, conv in enumerate(DEMO_CONVERSATIONS):
            # 计算时间戳（分散在3天内）
            timestamp = base_time + timedelta(
                hours=idx * 2,
                minutes=idx * 15
            )
            
            # 保存到SQLite
            chat = ChatHistory(
                session_id="demo_elder",
                user_text=conv["user"],
                ai_text=conv["ai"],
                timestamp=timestamp
            )
            db.add(chat)
            
            # 保存到ChromaDB
            conversation_id = f"demo_{uuid.uuid4().hex[:8]}"
            vector_store.add_conversation(
                conversation_id,
                conv["user"],
                conv["ai"]
            )
            
            print(f"   ✓ 对话 {idx + 1}/{len(DEMO_CONVERSATIONS)}")
        
        # 添加一些洞见到向量库
        insights = [
            ("爱好", "老人喜欢看荷花、喜欢越剧《红楼梦》、喜欢林黛玉"),
            ("饮食", "老人擅长做红烧肉，用糖色炒、小火慢炖，儿子小时候爱吃"),
            ("家庭", "老人和老伴在工厂认识，18岁时是纺织女工，老伴是机修工"),
            ("回忆", "年轻时常和老伴去西湖看荷花，很浪漫"),
            ("作息", "晚上9点半睡觉，有时会醒，昨天睡了7小时"),
            ("教育", "1965年高中毕业后进工厂，那时候读高中很不容易"),
            ("认知", "记忆力良好，能记住做菜细节，能准确回忆时间（1965年毕业）"),
        ]
        
        for idx, (category, insight) in enumerate(insights):
            insight_id = f"insight_{uuid.uuid4().hex[:8]}"
            vector_store.add_insight(insight_id, insight, category)
            print(f"   ✓ 洞见 {idx + 1}/{len(insights)}: {category}")
        
        db.commit()
        print(f"\n✅ 成功生成 {len(DEMO_CONVERSATIONS)} 条对话和 {len(insights)} 条洞见")
        print(f"📊 现在可以访问仪表盘查看效果: http://localhost:8080")
        
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()

