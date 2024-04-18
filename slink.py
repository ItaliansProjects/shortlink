import pyshorteners
from urllib.parse import urlparse
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def generate_short_link(original_url):
    s = pyshorteners.Shortener()
    short_url = s.tinyurl.short(original_url)
    return short_url

def start(update, context):
    update.message.reply_text("Ciao! Inserisci il token del tuo bot Telegram.")

def handle_token(update, context):
    token = update.message.text
    context.user_data['token'] = token
    update.message.reply_text("Ottimo! Ora inviami l'URL che desideri accorciare.")

def handle_message(update, context):
    user_input = update.message.text
    if user_input.lower() == 'exit':
        update.message.reply_text("Grazie per aver utilizzato questo tool.")
    else:
        if is_valid_url(user_input):
            short_url = generate_short_link(user_input)
            update.message.reply_text(f"Ecco il link accorciato: {short_url}")
        else:
            update.message.reply_text("Errore: Inserisci un URL valido.")

def main():
    updater = Updater(input("Inserisci il token del tuo bot Telegram: "))
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command & ~Filters.regex(r'^/[a-zA-Z0-9_]+$'), handle_message))
    dp.add_handler(MessageHandler(Filters.regex(r'^[a-zA-Z0-9_]+$'), handle_token))
    updater.start_polling()
    updater.idle()

if name == 'main':
    main()
