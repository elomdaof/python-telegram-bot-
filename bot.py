
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL", "@SalmentReports")

if not TOKEN:
    raise ValueError("BOT_TOKEN is missing!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "أهلًا بيك في بوت بلاغات سلامة بلدنا سلمنت 🌿\n\n"
        "البوت مخصص لاستقبال الصور والفيديوهات المتعلقة "
        "بالسلوكيات التي تهدد أمن وسلامة أهالي القرية.\n\n"
        "📩 ابعت صورة أو فيديو، واكتب مكان الواقعة "
        "والتفاصيل في وصف الصورة أو الفيديو.\n\n"
        "📌 المحتوى بيتم إرساله لقناة البلاغات.\n\n"
        "🔒 القناة لا تعرض اسم حسابك للمتابعين، "
        "لكن البوت نفسه يستقبل البلاغ من حسابك.\n\n"
        "⚠️ متعرضش نفسك للخطر أو تدخل في مواجهة. "
        "صور من مكان آمن فقط.\n\n"
        "هدفنا سلامة بلدنا وأهلها."
    )
    await update.message.reply_text(text)

async def receive_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    try:
        await context.bot.copy_message(
            chat_id=CHANNEL,
            from_chat_id=message.chat_id,
            message_id=message.message_id
        )

        await message.reply_text("✅ تم استلام وإرسال المحتوى.")

    except Exception as e:
        await message.reply_text(
            "❌ حصل خطأ أثناء الإرسال، حاول مرة أخرى."
        )
        print("Send error:", e)

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(filters.PHOTO | filters.VIDEO, receive_media)
)

print("Bot is running...")
app.run_polling()
