from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

import os
from dotenv import load_dotenv

load_dotenv()  # .env fayldan o‘qiydi

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = os.getenv("ADMIN_IDS")

admin_ids = [int(x.strip()) for x in ADMIN_IDS.split(",")]


user_sessions = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"/start bosildi: {update.effective_user.id}")
    await update.message.reply_text("Salom! Xabaringizni yozing, biz sizga tez orada javob beramiz.")


async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    full_name = update.effective_user.full_name
    text = update.message.text

    print(f"Xabar keldi: {user_id} - {text}")
    user_sessions[user_id] = full_name

    for admin_id in ADMIN_IDS:
        msg = f"📩 Yangi xabar:\n👤 {full_name} (ID: {user_id})\n✉️: {text}"
        await context.bot.send_message(chat_id=admin_id, text=msg)

    await update.message.reply_text("✅ Xabaringiz operatorlarga yuborildi. Tez orada javob olasiz.")


async def reply_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("❌ Sizga ruxsat yo‘q.")
        return

    args = context.args
    if len(args) < 2:
        await update.message.reply_text("❗ Format: /reply <user_id> matn")
        return

    target_user_id = int(args[0])
    reply_text = " ".join(args[1:])

    try:
        await context.bot.send_message(chat_id=target_user_id, text=f"💬 Operator javobi:\n{reply_text}")
        await update.message.reply_text("✅ Javob yuborildi.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Xatolik: {e}")



if __name__ == '__main__':
    print("Bot ishga tushmoqda...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reply", reply_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))

    app.run_polling()
