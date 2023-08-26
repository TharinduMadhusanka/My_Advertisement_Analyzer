from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update

from webScraper import extract_article_info

from typing import Final
key = "6282341763:AAG3tlKhNp_KSAFbgDXmJTZJhTjg46afluI"
BOT_USERNAME = "AdScanBot"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, world!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I'll help you!")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("man danne na ane...")

def handle_response(text: str) -> str:
    results = extract_article_info(text)
    response: str = "🆁🅴🆂🆄🅻🆃\n\n"

    response += "______𝐓𝐢𝐭𝐥𝐞______" + "\n\n"
    response += results[0] + "\n\n"

    response += "______𝐭𝐞𝐱𝐭______" + "\n\n"
    response += results[1] + "\n\n"

    response += "______𝐬𝐮𝐦𝐦𝐚𝐫𝐲______" + "\n\n"
    response += results[2] + "\n\n"

    response += "______𝐤𝐞𝐲𝐰𝐨𝐫𝐝𝐬______" + "\n\n"
    for item in results[3]:
        response += item + "\n"

    # response += "______𝐜𝐚𝐭𝐨𝐠𝐨𝐫𝐲______" + "\n\n"
    # response += results[4] + "\n\n"

    # response += "______𝐩𝐫𝐢𝐜𝐞______" + "\n\n"
    # response += results[5] + "\n\n"

    # response += "______𝐜𝐨𝐧𝐭𝐚𝐜𝐭______" + "\n\n"
    # for item in results[6]:
    #     response += item + "\n"
    
    # response += "______𝐥𝐨𝐜𝐚𝐭𝐢𝐨𝐧𝐬______" + "\n\n"
    # response += results[7] + "\n\n"
    # for item in results[7]:
    #     response += item + "\n"

    return response

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text: str = update.message.text

    print(f'User {update.message.chat.id} in {message_type}: {text}')

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print("Bot:", response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    app = Application.builder().token(key).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)

