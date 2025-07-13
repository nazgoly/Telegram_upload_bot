import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8045176855:AAEAry0LD8-Tqm8v7y02As3RqcLklAIj0xU"
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! فیلم مورد نظرت رو برام بفرست، لینک مستقیم برات می‌فرستم.")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video or update.message.document
    if not video:
        await update.message.reply_text("فایل ویدیویی ارسال نکردی، لطفاً فیلم بفرست.")
        return

    file_id = video.file_id
    file = await context.bot.get_file(file_id)
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.mp4")

    await file.download_to_drive(file_path)

    file_url = f"https://your-server-domain.com/{file_id}.mp4"  # این رو بعداً با آدرس واقعی Render جایگزین می‌کنیم
    await update.message.reply_text(f"فیلم شما آپلود شد!\nلینک مستقیم:\n{file_url}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))
    print("ربات شروع به کار کرد...")
    app.run_polling()
