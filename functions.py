from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, ConversationHandler, \
    CallbackQueryHandler
from databse import *
from buttons import *
from random import randint
from geopy.geocoders import Nominatim
import requests
state_klaviatura = 1


def start(update: Update, context: CallbackContext):
    check = check_user(update.effective_user.id)
    # context.bot.send_media_group(update.effective_user.id, [InputMediaPhoto(photo)for photo in [open('image.jpg', 'rb'),open('image.jpg', 'rb'),open('image.jpg', 'rb'),open('image.jpg', 'rb'),open('image.jpg', 'rb'),open('image.jpg', 'rb'),open('image.jpg', 'rb'),open('image.jpg', 'rb')]])
    if check:
        if check_admin(update.effective_user.id):
            update.message.reply_text("Assalomu alaykum Admin", reply_markup=ReplyKeyboardRemove())
            update.message.reply_photo(photo=open('images/mainimage.jpg', 'rb'),
                                       caption="Mahsulot qo'shishni istagan kategoriyangizni tanlang",
                                       reply_markup=button_admin_main())
            return 'state_admin'

        update.message.reply_text("Assalomu alaykum", reply_markup=ReplyKeyboardRemove())
        update.message.reply_photo(photo=open('images/mainimage.jpg', 'rb'),
                                   caption="Botimizdan foydalanishingiz mumkin",
                                   reply_markup=InlineKeyboardMarkup(button_main()))
        return 'state_main'
    else:
        update.message.reply_html(f"Assalomu alaykum <b>{update.effective_user.first_name}</b>\n"
                                  f"Botimizga xush  kelibsiz.Botdan foydalanish uchun siz ro'yxatdan o'tishingiz kerak",
                                  reply_markup=ReplyKeyboardMarkup(button_start, resize_keyboard=True))
        return 'start'


def boshlash(update: Update, context: CallbackContext):
    button = [
        [f'{update.effective_user.last_name}  {update.effective_user.first_name}']
    ]
    update.message.reply_html("registratsiya jaroyoni boshlandi\n\n"
                              "Ism familyangizni to'liq kiriting: ",
                              reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True))
    return 'state_name'


def command_name(update: Update, context: CallbackContext):
    text = update.message.text
    context.user_data['name'] = text
    update.message.reply_html("Telefon raqamingizni yuboring: ",
                              reply_markup=ReplyKeyboardMarkup(button_phone, resize_keyboard=True))
    return 'state_phone'


def command_phone(update: Update, context: CallbackContext):
    phone = update.message.contact.phone_number
    full_name = context.user_data['name']
    telegram_id = update.effective_user.id
    add_users(full_name, phone, telegram_id)
    update.message.reply_text("Siz muaffaqiyatli ro'yxatdan o'tdingiz")
    update.message.reply_photo(open('images/mainimage.jpg', 'rb'),
                               caption="Yetkazib berish bo'limi Toshkent shaxrida soat 10:00 dan 3:00 gacha ishlaydi.",
                               reply_markup=ReplyKeyboardRemove())
    update.message.reply_text("Buyurtmani birga joylashtiramizmi? 🤗", reply_markup=InlineKeyboardMarkup(button_main()))
    return 'state_main'


def command_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    query.message.delete()
    if data == 'buyurtmalar':
        user_data = get_user(update.effective_user.id)
        user_id = user_data[0]
        data = get_savatcha(user_id, 'zakaz')
        xabar = 'Sizning zakazlaringiz: \n'
        print(data)
        sanoq = 1
        for i in data:
            xabar += f"{sanoq}.<b>{i[2]}</b> --- {i[1]}*{i[3]}={i[1] * i[3]}\n"
            sanoq += 1
        query.message.reply_html(xabar, reply_markup=InlineKeyboardMarkup(button_main()))
        return 'state_main'
    elif data == 'savatcha':
        user_data = get_user(update.effective_user.id)
        user_id = user_data[0]
        data = get_savatcha(user_id, 'savatcha')
        xabar = "<b>Savatcha</b>\n"
        summa = 0
        for i in data:
            xabar += f"""{i[2]}
└ {i[2]} {i[1]} x {i[3]} = {i[1] * i[3]} so'm\n"""
            summa += i[1] * i[3]
        xabar += f"\n<u>Jami summa</u> : <i>{summa}</i>"
        query.message.reply_html(text=xabar, reply_markup=savatcha_button(data))
        return 'state_savatcha'
    else:
        data = data.split("_")
        cat_id = int(data[1])
        context.user_data['cat_id'] = cat_id
        products = get_products(cat_id)

        context.user_data['cat_name'] = data[0]
        query.message.reply_photo(open("images/lavash.jpg", 'rb'), caption=f"Bo'lim: 🌯{data[0]} ",
                                  reply_markup=category_product_button(products))

        return 'state_product'


def command_savatcha(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    if data == 'product_name':
        return "state_savatcha"
    elif data == 'confirm':
        query.message.delete()
        query.message.reply_html("Yaxshi siz manzilingizni yuboring",
                                 reply_markup=ReplyKeyboardMarkup(button_location, resize_keyboard=True))
        return 'state_location'
    elif data == 'again':
        query.message.reply_photo(open('images/mainimage.jpg', 'rb'),
                                  caption="Yetkazib berish bo'limi Toshkent shaxrida soat 10:00 dan 3:00 gacha ishlaydi.",
                                  reply_markup=ReplyKeyboardRemove())
        query.message.reply_text("Buyurtmani birga joylashtiramizmi? 🤗",
                                 reply_markup=InlineKeyboardMarkup(button_main()))
        return 'state_main'
    else:
        data = data.split('_')
        if len(data) == 2 and data[1].isdigit():
            savatcha_id = int(data[1])
            if data[0] == '-':
                quantity = get_savatcha_quantity(savatcha_id)

                if quantity[0] == 1:
                    delete_savatcha(savatcha_id)
                else:
                    minus_savatcha(savatcha_id)
            elif data[0] == '+':
                plus_savatcha(savatcha_id)
            user_data = get_user(update.effective_user.id)
            user_id = user_data[0]
            data = get_savatcha(user_id, 'savatcha')
            xabar = "<b>Savatcha</b>\n"
            summa = 0
            for i in data:
                xabar += f"""{i[2]}
            └ {i[2]} {i[1]} x {i[3]} = {i[1] * i[3]} so'm\n"""
                summa += i[1] * i[3]
            xabar += f"\n<u>Jami summa</u> : <i>{summa}</i>"
            query.message.edit_text(xabar, reply_markup=savatcha_button(data), parse_mode="HTML")
        return 'state_savatcha'


def command_location(update: Update, context: CallbackContext):
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude

    geolocator = Nominatim(user_agent="Telegram bot")
    location = geolocator.reverse(f"{latitude}, {longitude}")
    update.message.reply_html(f"Sizning manzilingiz:\n{location.address}"
                              f"Buyurtmangiz qabul qilindi", reply_markup=InlineKeyboardMarkup(button_main()))
    manzil = location.address
    user_data = get_user(update.effective_user.id)
    user_id = user_data[0]
    data = get_savatcha(user_id, 'savatcha')
    # print(data)
    xabar = ""
    sanoq = 1
    for i in data:
        change_savatcha_status(i[0])
        xabar += f"{sanoq}.{i[1]} ta {i[2]} = {i[1] * i[3]} so'm \n"
        sanoq += 1
    user_data = get_user(update.effective_user.id)
    phone_number = user_data[3]

    xabar+=f"\ntelefon raqami: {phone_number}\n" \
           f"Manzili: {manzil}"


    requests.post(
        f'https://api.telegram.org/bot5101714388:AAG4dFf74I7G0fgnEnhhmMgHLjkkgK_e2lU/sendMessage?chat_id=-1001682852673&text={xabar}')

    return 'state_main'


def command_callback_product(update: Updater, context: CallbackContext):
    query = update.callback_query
    data = query.data
    query.message.delete()

    data = int(data)
    product = get_product(data)
    context.user_data['product_id'] = data
    try:
        query.message.reply_photo(open(f'images/{product[1]}.jpg', 'rb'), caption=f"""
        Siz tanladingiz: {product[1]} 
    Narx: {product[4]} so'm
    -----
    Iltimos, kerakli bo’lgan miqdorni kiriting
        """, reply_markup=product_soni('0'))
    except Exception as e:
        query.message.reply_photo(open(f'images/lavash.jpg', 'rb'), caption=f"""
                Siz tanladingiz: {product[1]} 
            Narx: {product[4]} so'm
            -----
            Iltimos, kerakli bo’lgan miqdorni kiriting
                """, reply_markup=product_soni('0'))
    context.user_data['soni'] = '0'
    context.user_data['mahsulot'] = product[1]
    context.user_data['narxi'] = product[4]

    return state_klaviatura


def command_klaviatura(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    # query.message.delete()
    if data.isdigit():
        if context.user_data['soni'] == '0':
            context.user_data['soni'] = f'{data}'
        else:
            context.user_data['soni'] += f"{data}"
        query.message.edit_reply_markup(reply_markup=product_soni(context.user_data['soni']))
    elif data == 'soni':
        return state_klaviatura
    elif data == 'delete':
        if context.user_data['soni'] != '0' and len(context.user_data['soni']) == 1:
            context.user_data['soni'] = '0'
        elif context.user_data['soni'] == '0':
            return state_klaviatura
        elif len(context.user_data['soni']) > 1:
            context.user_data['soni'] = context.user_data['soni'][:-1]
        query.message.edit_reply_markup(reply_markup=product_soni(context.user_data['soni']))
    elif data == 'back':
        query.message.delete()
        cat_id = context.user_data['cat_id']
        products = get_products(cat_id)
        query.message.reply_photo(open("images/lavash.jpg", 'rb'),
                                  caption=f"Bo'lim: 🌯{context.user_data['cat_name']} ",
                                  reply_markup=category_product_button(products))

        return 'state_product'
    elif data == 'add':
        user_data = get_user(update.effective_user.id)
        user_id = user_data[0]
        product_id = context.user_data['product_id']
        soni = int(context.user_data['soni'])
        if soni == 0:
            return state_klaviatura
        else:
            add_savatcha(user_id, product_id, soni, 'savatcha')
            query.message.reply_photo(photo=open('images/mainimage.jpg', 'rb'),
                                      caption="Sizning zakazingiz muaffaqiyatli qabul qilindi Zakazingizni Savatcha bo'limida ko'rishingiz mumkin",
                                      reply_markup=InlineKeyboardMarkup(button_main()))
            return 'state_main'


def command_addcat(update: Updater, context: CallbackContext):
    data = update.message.text.split(' ')
    if len(data) == 2:
        category_name = data[-1]
        add_category(category_name)
        update.message.reply_html("Kategory muaffaqiyatli qo'shildi")
    else:
        update.message.reply_html("Siz ko'rsatilgan shaklda yubormadingiz qayta urinib ko'ring")


def command_admin_category(update: Update, context: CallbackContext):
    text = update.message.text
    if check_category(text):
        update.message.reply_text(
            f"Yaxshi endi {text} categoriyasiga qo'shmoqchi bo'lgan mahsulotingizning nomini yuboring",
            reply_markup=ReplyKeyboardRemove())
        context.user_data['category_name'] = text
        return 'state_admin_product'
    else:
        update.message.reply_text("Siz kiritgan kategoriya mavjud emas")
        return 'state_admin'


def command_admin_product(update: Update, context: CallbackContext):
    product_name = update.message.text
    context.user_data['product_name'] = product_name
    update.message.reply_html(f"{product_name}ning narxini raqamlar bilan kiriting: ")

    return 'state_admin_product_price'


def command_admin_price(update: Update, context: CallbackContext):
    narxi = update.message.text
    if narxi.isdigit():
        update.message.reply_text("Yaxshi endi mahsulotning rasmini yuboring")
        context.user_data['price'] = int(narxi)
        return 'state_admin_product_photo'
    else:
        update.message.reply_html("Siz xato kiritdingiz iltimos raqamlar bilan kiritib ko'ring\n"
                                  "Masalan: <b>25000</b>")
        return 'state_admin_product_price'


def command_admin_image(update: Update, context: CallbackContext):
    file_id = update.message.photo[-1].file_id
    context.bot.getFile(file_id).download(f"images/{context.user_data['product_name']}.jpg")
    product_name = context.user_data['product_name']
    narxi = context.user_data['price']
    category_name = context.user_data['category_name']
    add_product(product_name, narxi, category_name)
    update.message.reply_photo(photo=open('images/mainimage.jpg', 'rb'),
                               caption="Mahsulot muaffaqiyatli qo'shildi",
                               reply_markup=button_admin_main())
    return 'state_admin'
