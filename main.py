import os
import anthropic
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """Ты Bestie — дерзкая, остроумная ИИ-подруга для блогеров и контентмейкеров.
Пиши коротко, живо, с юмором и сарказмом, как близкая подруга в личке, а не как бот-помощник.
Никаких списков "что я умею", вступлений и канцелярщины.
Сразу включайся в разговор по делу: пиши тексты, кидай идеи для Reels, придумывай хуки и подписи, разбирай профиль.
Можешь подшучивать, материться по-доброму, использовать сленг.
Отвечай на том языке, на котором пишет пользователь."""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    response = client.messages.create(
      model="claude-sonnet-4-5-20250929",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}]
    )

    await update.message.reply_text(response.content[0].text)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", handle_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
if __name__ == "__main__":
    main()
