import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from main import AtlasAgent

# إعداد الـ Logging لمراقبة العمليات
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# تخزين الجلسات (Sessions) لكل مستخدم
user_sessions = {}

def get_user_agent(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = AtlasAgent()
    return user_sessions[user_id]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_id = update.effective_user.id
    agent = get_user_agent(user_id)
    
    # إظهار حالة "Typing..." ف تليجرام
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # إذا صيفط صورة
        if update.message.photo:
            file = await update.message.photo[-1].get_file()
            image_url = file.file_path 
            caption = update.message.caption if update.message.caption else "شنو كاين هنا؟"
            
            response = agent.chat(caption, image_url=image_url)
            await update.message.reply_text(response)
            
        # إذا صيفط نص عادي
        elif update.message.text:
            response = agent.chat(update.message.text)
            await update.message.reply_text(response)

    except Exception as e:
        logger.error(f"Error in handle_message: {e}")
        await update.message.reply_text("⚠️ وقع مشكل تقني، جرب مرة أخرى.")

if __name__ == "__main__":
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TOKEN:
        print("❌ TELEGRAM_TOKEN missing in .env")
    else:
        app = Application.builder().token(TOKEN).build()
        
        # ربط النصوص والصور بالدالة (كاع اللي ماشي Command)
        app.add_handler(MessageHandler((filters.TEXT | filters.PHOTO) & ~filters.COMMAND, handle_message))
        
        print("🚀 Atlas Hybrid (Groq + Gemini) is Online!")
        app.run_polling()