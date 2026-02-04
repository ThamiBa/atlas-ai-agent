import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from main import AtlasAgent # استيراد الماكينة ديالك

# إعداد الـ Logging باش نعرفو شنو واقع في السيرفر
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

load_dotenv()

# إنشاء نسخة من البوت
atlas = AtlasAgent()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """الجواب على أمر /start"""
    user = update.effective_user
    await update.message.reply_html(f"أهلاً <b>{user.first_name}</b>! أنا أطلس، مساعدك الذكي بالدارجة. شنو بغيتي تعرف اليوم؟")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """استقبال الميساجات وصيفطهم لـ Groq"""
    user_input = update.message.text
    
    # إظهار أن البوت "يكتب..." (Typing action)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # عيطنا للدالة  main.py
    # ملاحظة: دابا غنحتاجو الدالة ترجع لينا نص (Return) ماشي غير تطبعو
    response = atlas.chat(user_input)
    
    if response:
        await update.message.reply_text(response)
    else:
        await update.message.reply_text("سمح ليا، وقع مشكل في الاتصال. جرب مرة أخرى.")

if __name__ == "__main__":
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    
    # بناء التطبيق
    application = Application.builder().token(TOKEN).build()
    
    # ربط الأوامر والميساجات بالدوال
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🚀 Atlas Bot is starting on Telegram...")
    application.run_polling()