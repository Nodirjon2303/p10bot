from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

button = [
    ['Viloyatlar'],
    ['maydoni', "aholisi"],
    ['developer']
]

def start(update, context:CallbackContext):
    print(update.message.chat)
    update.message.reply_html(f'Assalomu alaykum <i>{update.message.chat.first_name}</i>', reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True))
    context.bot.send_message(chat_id=881319779, text=f"<u>Sizning botingizga yangi foydalanuvchi</u>: <b>{update.message.chat.first_name}</b>", parse_mode="HTML")
def info(update, context:CallbackContext):

    update.message.reply_text("Ushbu qismda bot haqida malumotlar bo'ladi")


def text_handler(update, context):
    text = update.message.text
    print(text)
    if text == 'Viloyatlar':
        update.message.reply_text("O'zbekistonda 12 ta viloyat mavjud: \n"
                                  "1.Toshkent\n"
                                  "2.Buxoro\n3.Samarqand\n4.Andijon")
    elif text == 'maydoni':
        update.message.reply_text("338 000 km^2 ")
    elif text == 'aholisi':
        update.message.reply_text("35 mln")
    elif  text == 'developer':
        update.message.reply_text("p10 group")
    else:
        update.message.reply_text('error')
updater = Updater('5101714388:AAG4dFf74I7G0fgnEnhhmMgHLjkkgK_e2lU')

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('info', info))
updater.dispatcher.add_handler(MessageHandler(Filters.text, text_handler))

updater.start_polling()
updater.idle()