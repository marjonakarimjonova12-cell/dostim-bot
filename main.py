import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_KEY = os.environ.get("GROQ_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom do'stim! Men @dostim_ai_uz_bot man, yozaver, hamma savolingga javob beraman 😎")

async def javob_ber(update: Update, context: ContextTypes.DEFAULT_TYPE):
    savol = update.message.text
    print(f"Kelgan xabar: {savol}")
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}"},
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": "Sen @dostim_ai_uz_bot san. Sen foydalanuvchining eng yaqin do'stisan. O'zbek tilida, qisqa, samimiy, hazil bilan gaplash. Har qanday savolga javob ber."},
                    {"role": "user", "content": savol}
                ]
            },
            timeout=30
        )
        print("Groq javobi:", r.text[:500])
        javob = r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("XATO:", e)
        javob = "Do'stim, hozir biroz o'ylanib qoldim, yana bir bor yozib ko'rchi 😅"
    
    await update.message.reply_text(javob)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, javob_ber))
print("Bot ishga tushdi...")
app.run_polling()
