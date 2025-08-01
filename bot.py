import os
import re
import time
import asyncio
import datetime
from pyrogram import Client, filters
from pyrogram.types import (
    Message, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    CallbackQuery
)
from deep_translator import GoogleTranslator
from edge_tts import Communicate

# Config (Tune Diye Hue Details)
BOT_TOKEN = "7977802802:AAFj6N2VlU4xVv7kIPf7IocaCK72y5agtlg"
OWNER_ID = 7841882010
SUDO_USERS = [7841882010, 8025080923]  # Owner + Sudo Users
START_ANIMATION = "https://telegra.ph/file/1a7a5a3e2a6a8b8b8b8b8.mp4"
START_IMAGE = "https://envs.sh/Quv.jpg"

app = Client(
    "ultra_bot",
    bot_token=BOT_TOKEN,
    api_id=22545644,  # Your API_ID (my.telegram.org)
    api_hash="5b8f3b235407aea5242c04909e38d33d"  # Your API_HASH
)

# ---------------------- START MENU ----------------------
@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    # Animation First
    await message.reply_animation(
        START_ANIMATION,
        caption="⚡ **Ultimate Bot Activated!**"
    )
    await asyncio.sleep(3)
    
    # Main Menu
    await message.reply_photo(
        START_IMAGE,
        caption=f"""
👋 **Welcome to Ultimate Bot!**

✨ **Features:**
- /tts - Hindi Male/Female Voice
- /math - Smart Calculator
- /ping - Check Bot Speed
- /afk - Set AFK Status
- /clone - Create Your Own Bot
- /tr - Auto-Translate
- /spam - Spam Messages (Sudo Only)
- /tagall - Mention All in Group
- /broadcast - (Owner Only)""",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❤️‍🔥 Owner", user_id=OWNER_ID)],
            [InlineKeyboardButton("📜 Help", callback_data="help")],
            [InlineKeyboardButton("⚡ Sudo Panel", callback_data="sudo_panel")]
        ])
    )

# ---------------------- TTS (Hindi Male/Female) ----------------------
@app.on_message(filters.command("tts"))
async def tts(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("❌ Usage: `/tts Hello World`")
    
    text = " ".join(message.command[1:])
    voice = "hi-IN-MadhurNeural"  # Male
    
    if "female" in text.lower():
        voice = "hi-IN-SwaraNeural"  # Female
    
    try:
        communicate = Communicate(text, voice)
        await communicate.save("tts.mp3")
        await message.reply_voice(
            "tts.mp3",
            caption=f"🔊 **TTS Generated**\n\n{text}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔁 Regenerate", callback_data=f"tts_{text}")]
            ])
        )
        os.remove("tts.mp3")
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")

# ---------------------- PING ----------------------
@app.on_message(filters.command("ping"))
async def ping(client: Client, message: Message):
    start = time.time()
    msg = await message.reply("🏓 Pong!")
    end = time.time()
    await msg.edit_text(f"""
⚡ **Bot Status**

⏱ Speed: {(end-start)*1000:.2f}ms
🕒 Uptime: {datetime.datetime.now().strftime('%H:%M:%S')}
❤️‍🔥 Powered by @ll_ZORO_DEFAULTERS_ll""")

# ---------------------- MATH SOLVER ----------------------
@app.on_message(filters.command("math"))
async def math(client: Client, message: Message):
    try:
        expr = " ".join(message.command[1:])
        result = eval(expr)
        await message.reply(f"🧮 Result: `{expr} = {result}`")
    except:
        await message.reply("❌ Usage: `/math 2+2*5`")

# ---------------------- AFK SYSTEM ----------------------
AFK_USERS = {}
@app.on_message(filters.command("afk"))
async def afk(client: Client, message: Message):
    reason = " ".join(message.command[1:]) or "AFK"
    AFK_USERS[message.from_user.id] = {
        "time": time.time(),
        "reason": reason
    }
    await message.reply(f"🚶 {message.from_user.first_name} is now AFK\n💬 Reason: {reason}")

# ---------------------- CLONE BOT SYSTEM ----------------------
@app.on_message(filters.command("clone"))
async def clone(client: Client, message: Message):
    await message.reply(
        "🤖 **Bot Clone System**\n\n"
        "1. Create bot via @BotFather\n"
        "2. Send token here\n"
        "3. I'll deploy it for you!\n\n"
        "⚠️ Reply with /cancel to abort",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎥 Tutorial", url="t.me/ll_ZORO_DEFAULTERS_ll")]
        ])
    )
    
    try:
        token_msg = await message.chat.await_message(
            message.from_user.id,
            filters.text,
            timeout=300
        )
        
        if token_msg.text == "/cancel":
            return await token_msg.reply("🚫 Clone cancelled!")
            
        if not re.match(r"\d+:[a-zA-Z0-9_-]+", token_msg.text):
            return await token_msg.reply("❌ Invalid token format!")
        
        await token_msg.reply(
            "✅ **Token Saved!**\n\n"
            "Deploy Steps:\n"
            "1. Fork this repo\n"
            "2. Add token in Render env\n"
            "3. Deploy!\n\n"
            "Need help? Contact owner!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🚀 Deploy Now", url="https://render.com")]
            ])
        )
    except asyncio.TimeoutError:
        await message.reply("⌛ Timeout! Try again.")

# ---------------------- TRANSLATE ----------------------
@app.on_message(filters.command("tr"))
async def translate(client: Client, message: Message):
    try:
        _, lang, text = message.text.split("|", 2)
        translated = GoogleTranslator(source='auto', target=lang).translate(text)
        await message.reply(f"""
🌐 **Translation:**
{text} → {lang}
{translated}""")
    except:
        await message.reply("❌ Usage: `/tr en|नमस्ते`")

# ---------------------- SPAM (SUDO ONLY) ----------------------
@app.on_message(filters.command("spam") & filters.user(SUDO_USERS))
async def spam(client: Client, message: Message):
    if len(message.command) < 3:
        return await message.reply("❌ Usage: `/spam 10 Hello World`")
    
    try:
        count = int(message.command[1])
        text = " ".join(message.command[2:])
        
        for i in range(count):
            await message.reply_text(f"🔊 {text} ({i+1}/{count})")
            await asyncio.sleep(0.5)  # Anti-ban delay
    except:
        await message.reply("❌ Usage: `/spam 5 Spam Message`")

# ---------------------- TAG ALL (GROUPS) ----------------------
@app.on_message(filters.command("tagall") & filters.group)
async def tagall(client: Client, message: Message):
    members = []
    async for member in client.get_chat_members(message.chat.id):
        members.append(member.user.mention)
    
    await message.reply(
        "👥 **Tagging All Members:**\n\n" + "\n".join(members),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Close", callback_data="close")]
        ])
    )

# ---------------------- BROADCAST (OWNER ONLY) ----------------------
@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("❌ Usage: `/broadcast Your Message`")
    
    text = message.text.split(None, 1)[1]
    users = [user async for user in client.get_chat_members("me")]
    
    sent = 0
    for user in users:
        try:
            await client.send_message(user.user.id, text)
            sent += 1
        except:
            continue
    
    await message.reply(f"📢 Broadcast sent to {sent} users!")

# ---------------------- HELP MENU ----------------------
@app.on_callback_query(filters.regex("^help$"))
async def help_menu(client: Client, query: CallbackQuery):
    await query.edit_message_caption("""
📚 **All Commands:**

• /start - Main menu
• /ping - Check speed
• /math - Calculate
• /tr - Translate
• /afk - Set AFK
• /tts - Text-to-Speech (Male/Female)
• /clone - Create your own bot
• /spam - Spam messages (Sudo)
• /tagall - Mention all in group
• /broadcast - (Owner only)""",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
        ])
    )

# ---------------------- RUN BOT ----------------------
print("✨ Ultimate Bot Started!")
app.run()
