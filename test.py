from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.utils.request import Request
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = os.getenv("ADMIN_IDS")

admin_ids = [int(x.strip()) for x in ADMIN_IDS.split(",")]


request = Request(connect_timeout=10, read_timeout=10)
updater = Updater(token=BOT_TOKEN, request_kwargs={'connect_timeout': 10, 'read_timeout': 10})

dispatcher = updater.dispatcher



main_buttons = [
    [KeyboardButton(text="Kitoblar", ), KeyboardButton(text="Telefonlar")],
    [KeyboardButton(text="Kiyimlar"), KeyboardButton(text="Mashinalar")],
]


def start_command(update, context):

    update.message.reply_text(
        text="Menu",  #### resize_keyboard razmirini togrilagani
        reply_markup=ReplyKeyboardMarkup(main_buttons, resize_keyboard=True)
    )


def message_handler(update, context):
    print(update.message.text)
    message=update.message.text
    buttons1 = [
        [
            InlineKeyboardButton(text="Apple", callback_data="ap1"),
            InlineKeyboardButton(text="Sumsung", callback_data="ap2"),
            InlineKeyboardButton(text="Nokia", callback_data="ap3"),
            InlineKeyboardButton(text="Xiomi", callback_data="ap4"),
        ],
        [
            InlineKeyboardButton(text="⬅️back", callback_data="end1")
        ]
    ]

    buttons2  = [
        [
            InlineKeyboardButton(text="Diniy kitoblar", callback_data="ap1")
        ],
        [
                InlineKeyboardButton(text="Ertak kitoblar", callback_data="ap2")
        ],
        [
            InlineKeyboardButton(text="G'azal kitoblar", callback_data="ap3")
        ],
        [
            InlineKeyboardButton(text="Matem kitoblar", callback_data="ap4")
        ],

        [
            InlineKeyboardButton(text="⬅️back", callback_data="end1")
        ]
    ]
    if message == "Telefonlar":
        update.message.reply_text(
            text="Tanlang:",
            reply_markup=InlineKeyboardMarkup(buttons1)
                                  )

    elif message == "Kitoblar":
        update.message.reply_text(
            text="Tanlang:",
            reply_markup=InlineKeyboardMarkup(buttons2)
        )


def inline_buttons(update, context):
    query = update.callback_query


    if query.data == 'end1':
        query.message.reply_text(reply_markup=ReplyKeyboardMarkup(main_buttons))




dispatcher.add_handler(CommandHandler("start", start_command)) ### shu yerga start deb yozsak camandamz start boladi

dispatcher.add_handler(MessageHandler(Filters.text, message_handler)) ### command  bolsa userga yozgani qaytarmidi
dispatcher.add_handler(CallbackQueryHandler(inline_buttons))

updater.start_polling()