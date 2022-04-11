from functions import *

conv = ConversationHandler(
    entry_points=[
        MessageHandler(Filters.all, start)
    ],
    states={
        'start': [
            MessageHandler(Filters.regex('^(' + "Boshlash" + ')$'), boshlash)
        ],
        'state_name': [
            MessageHandler(Filters.text, command_name)
        ],
        'state_phone': [
            MessageHandler(Filters.contact, command_phone)
        ],
        'state_main': [
            CallbackQueryHandler(command_callback)
        ],
        'state_product': [
            CallbackQueryHandler(command_callback_product)
        ],
        state_klaviatura: [
            CallbackQueryHandler(command_klaviatura)
        ],
        'state_savatcha': [
            CallbackQueryHandler(command_savatcha)
        ],
        'state_admin': [
            CommandHandler('reklama', command_admin_reklama),
            MessageHandler(Filters.text, command_admin_category),

        ],
        'state_location': [
            MessageHandler(Filters.location, command_location)
        ],
        'state_admin_product': [
            MessageHandler(Filters.text, command_admin_product)
        ],
        'state_admin_product_price': [
            MessageHandler(Filters.text, command_admin_price)
        ],
        'state_admin_product_photo': [
            MessageHandler(Filters.photo, command_admin_image)
        ],
        'state_admin_reklama':[
            MessageHandler(Filters.photo, command_admin_reklama_photo),
            MessageHandler(Filters.text, command_admin_reklama_text)
        ]
    },
    fallbacks=[
        CommandHandler('start', start)
    ]
)

updater = Updater('5101714388:AAG4dFf74I7G0fgnEnhhmMgHLjkkgK_e2lU')

updater.dispatcher.add_handler(conv)
updater.dispatcher.add_handler(CommandHandler('addcat', command_addcat))

updater.start_polling()
updater.idle()
