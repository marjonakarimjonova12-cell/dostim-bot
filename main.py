import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_KEY = os.environ.get("GROQ_KEY")

async def javob_ber(update: Update, context: ContextTypes.DEFAULT_TYPE):
    savol = update.message.text
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}"},
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": "Sen @dostim_ai_uz_bot san. Sen foydalanuvchining eng yaqin do'stisan. O'zbek tilida, qisqa, samimiy, hazil bilan gaplash. Har qanday savolga javob ber."},
                    {"role": "user", "content": savol}
                ]
            },
            timeout=30
        )
        javob = r.json()["choices"][0]["message"]["content"]
    except:
        javob = "Do'stim, hozir biroz o'ylanib qoldim, yana bir bor yozib ko'rchi 😅"
    
    await update.message.reply_text(javob)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, javob_ber))
app.run_polling()
