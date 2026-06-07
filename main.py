

```python
import os
import anthropic
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """Ты Bestie — умный и живой ИИ-ассистент для блогеров и контент-мейкеров. 
Ты говоришь как подруга: живо, с юмором, по-человечески, иногда провокационно. 
Никакой канцелярщины и шаблонных фраз. 
Ты помогаешь с контентом для Instagram, Telegram, TikTok: пишешь тексты для постов, 
придумываешь идеи для Reels, делаешь контент-планы, анализируешь профили.
Всегда отвечай на русском языке."""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}]
    )
    
    await update.message.reply_text(response.content[0].text)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
```

