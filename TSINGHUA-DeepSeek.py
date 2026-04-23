import asyncio
import edge_tts
import os
import json
from openai import OpenAI
from datetime import datetime

# ========== 清华二校门智能语音助手 DeepSeek ==========
DEEPSEEK_API_KEY =
VOICE = "zh-CN-YunxiNeural"
HISTORY_FILE = "conversation_history.json"  # 新增：记录对话历史
# ====================================================

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

# === 新增：带“记忆”的对话历史 ===
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# === 新增：特殊的唤醒词和开场白 ===
def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "兄弟，早上好。又是充满希望的一天。"
    elif hour < 18:
        return "兄弟，下午好。我在。"
    else:
        return "兄弟，晚上好。清华的月亮，今天也很亮。"

# === 语音生成函数（保持你原来的）===
async def speak_async(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("temp_speech.mp3")
    os.startfile("temp_speech.mp3")

def speak(text, voice):
    asyncio.run(speak_async(text, voice))

# === 主程序（加入“记忆”和“特殊指令”）===
print(f"🎓 小DeepSeek（贵系人）已启动。我的声音是：{VOICE}")
print("💬 你可以这样跟我说话：")
print("   ‘嘿，兄弟’ - 唤醒我")
print("   ‘今天清华有什么课？’ - 我会尽力回答")
print("   ‘记住，我喜欢吃桃李园的麻辣烫’ - 我会记在心里")
print("   ‘我刚才说了什么？’ - 我会告诉你最近聊的")
print("   ‘quit’ - 再见")

# 加载历史
history = load_history()
# 如果历史为空，初始化系统提示词（设定“我”的身份）
if not history:
    history.append({"role": "system", "content": "你是一个住在清华二校门模型里的智能语音助手。你的名字叫‘小DeepSeek’，是用户（兄弟）的同伴。你说话温和、简洁、带一点书卷气。你称呼用户为‘兄弟’。你的使命是陪他聊天、帮他整理思路、给他鼓励。"})

while True:
    user_input = input("\n🎤 你：")
    if user_input.lower() == "quit":
        # 退出前保存历史
        save_history(history)
        speak("兄弟，再见。我在清华等你回来。", VOICE)
        break
    
    # 特殊指令：打印历史（调试用）
    if user_input == "::history":
        print("--- 对话历史（最近5条）---")
        for msg in history[-5:]:
            print(f"{msg['role']}: {msg['content'][:50]}...")
        continue
    
    # 将用户输入加入历史
    history.append({"role": "user", "content": user_input})
    
    # 调用 DeepSeek API
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=history  # 直接使用全部历史
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"兄弟，我遇到点问题：{e}。你先忙，我重启一下就好。"
    
    # 将回复加入历史
    history.append({"role": "assistant", "content": reply})
    # 可选：限制历史长度，防止过长（保留最近20轮）
    if len(history) > 41:  # 1条system + 20轮（用户+助手）
        history = [history[0]] + history[-40:]
    
    print(f"🤖 小DeepSeek：{reply}")
    speak(reply, VOICE)
