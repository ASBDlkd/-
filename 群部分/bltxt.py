import asyncio
import os
import botpy
from botpy import logging
from botpy.message import Message
from botpy.types.message import Embed
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, Message

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()
#以下是词库对话功能（已经实现了多样式回复）
class MyClient(botpy.Client):
    keyword_responses = {
        "早": ["早上好哦，巴迪一直都在呢≡ω≡"],
        "你好": ["你好哦，巴迪有什么可以帮助你的吗？"],
        "学习": ["巴迪很喜欢学习，一起进步吧！"],
        "笑话": ["为什么蛇没有朋友？因为蛇太会扯了！"],
        "天气":[ "巴迪不太懂天气，请合理运用搜索引擎哦。"],
        "谢谢": ["不客气，巴迪都不好意思了哦。"],
        "再见": ["再见，巴迪期待下次和你聊天呢！"],
        "喜欢": ["巴迪喜欢和你聊天，你呢？"],
        "吃饭了吗": ["记得按时吃饭哦。"],
        "谢谢":[ "不用客气哦，巴迪随时都在。"],
        "告诉我个秘密": ["巴迪的秘密是... 我喜欢收集有趣的笑话！"],
        "想你": ["我也想你了呢，巴迪每次和你聊天都很开心呢。"],
        "你骂谁呢":[ "巴迪还不会骂人哦"],
        "注意安全": ["别担心，巴迪长得很安全。"],
        "我害怕": ["嗯？你怕什么呀"],
        "放屁":[ "闻一闻十年少。"],
        "你不会了吧": ["这种雕虫小技只有巴迪才会拿出来显摆。"],
        "下班了": ["呜呜呜～巴迪还没有下班呢"],
        "对嘛": ["？那里对了呢，巴迪还不会呢"],
        "躺下": ["地上脏脏，巴迪不要🙉"],
        "我错了": ["呜呜呜～"],
        "当真": ["你觉得巴迪会给你开玩笑么"],
        "果然": ["果然？"],
        "不知道": ["什么都不知道。"],
        "汪汪": ["？汪？"],
        "饿": ["巴迪也饿了呢，你要喂我嘛？"],
        "我生病了": ["不用怕，拯救你的电线杆就在你家出门左拐一百米右转一百二四米处。"],
        "有什么好": ["很多很多很多呢"],
        "拜访":[ "嗯？拜访，你要来我家玩呀🔨"],
        "你有老婆": ["老婆～，呜～"],
        "谁发明的":[ "巴迪也不知道呢"],
        "这么": ["我也觉得有点儿过分了呢。"],
        "在哪工作": ["在你心里💘"],
        "你会说话吗":[ "你要@我并且发送指令哦"],
        "跟我回家": ["巴迪还不认识路，要你着巴迪的手～"],
        "不后悔":["你确定吗？"],
        "有什么好": ["只可意会，不可言传哦。"],
        "有真人没":[ "没有🌚，反正巴迪是个机器人🌚"],
        "女朋友": ["你有女朋友了吗？"],
        "你几岁了":[ "你猜猜看","22"],
        "你多大":["偷偷告诉你巴迪姐姐22了哦。"],
        "结果呢": ["结果巴迪成为了一个机器人，呜～"],
        "你有病": ["有病了巴迪就不会理你了呢[/害羞]"],
        "我喜欢你":[ "［害羞、害羞］真的吗"],
        "行":[ "我看刑"],
        "四川": ["辣妹子辣，辣妹子辣，辣妹子辣妹子辣辣辣~"],
        "烧饼": ["还没烧好呢"],
        "不行了吧":[ "还行吧……"],
        "那你不": ["？你在说什么啊，巴迪不懂🙉"],
        "我美吗": ["你问问巴迪姐姐同不同意💕"],
        "你是谁": ["一个努力奔赴未来的巴迪呢～"],
        "你嘎": ["不要呢～，呜呜呜～"],
        "晚安": ["晚安，晚安💕", "梦里见哦(•̶̑ ૄ •̶̑)","好的呢，晚安安","晚安，晚安，梦里是要想巴迪么？"],
        "午":["中午好呀，今天已经过去一半了哦，下午继续加油哦"],
        "群主": ["巴迪偷偷告诉你个秘密，群主最帅哦‘=͟͟͞͞(･∇･ ‧̣̥̇)"],
        "日历":["日历？，想想就好💔"]
        # 添加更多关键词和回复
    }
    last_responses_index = {}
      #屏蔽以下关键词回复反馈
    special_commands = ["动漫","壁纸", "风景", "百变图", "素描头像", "美女图片",
                        "每日一言", "我的头像", "情感一言", "伤感文案",
                        "笑一笑", "搞笑文案", "二次元", "心灵鸡汤", "毒鸡汤",
                        "菜单","测试"
                        ]
                        
    async def on_ready(self):
        _log.info(f"Robot 「{self.robot.name}」 on_ready!")
        #以下是频道端发送信息代码
    async def on_at_message_create(self, message: Message):
        user_id = message.author.id
        user_message = message.content
        for keyword, responses in self.keyword_responses.items():
            if keyword in user_message:
                last_index = self.last_responses_index.get(keyword, -1)
                new_index = (last_index + 1) % len(responses)
                response = responses[new_index]
                self.last_responses_index[keyword] = new_index
                await message.reply(content=f"<@{user_id}> {response}")
                return
        if any(command in user_message for command in self.special_commands):
            return
        bot_reply = generate_intelligent_reply(user_message)
        await message.reply(content=f"<@{user_id}> {bot_reply}")
        #以下是QQ群聊端发送代码
    async def on_group_at_message_create(self, message: GroupMessage):
        user_openid = message.author.member_openid  # 使用 member_openid 作为用户唯一标识
        user_message = message.content
        for keyword, responses in self.keyword_responses.items():
            if keyword in user_message:
                last_index = self.last_responses_index.get(keyword, -1)
                new_index = (last_index + 1) % len(responses)
                response = responses[new_index]
                self.last_responses_index[keyword] = new_index
                messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0, 
                msg_id=message.id,
                content=f"{response}")
                return
        if any(command in user_message for command in self.special_commands):
            return
        bot_reply = generate_intelligent_reply(user_message)
        await message.reply(content=f"{bot_reply}")
        #以下是@机器人发送不正确指令回复内容
def generate_intelligent_reply(user_message):
    return "\n抱歉，巴迪还在学习中，暂时无法处理这个问题，\n请使用“@阿斯巴迪 /菜单”\n这个功能来查看现在可用功能。"
    #其他端指令发送，请参考官方botpy事件监听文档
if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道（监听频道的事件通道）
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道（公域机器人所以监听权限）
    intents = botpy.Intents.default()
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])