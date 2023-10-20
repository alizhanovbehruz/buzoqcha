from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

language = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🇺🇿O'zbekcha"),
            KeyboardButton(text="🇷🇺Русский "),
        ],
    ],
    resize_keyboard=True
)

Loc_send = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📍Joylashuvni jo'natish", request_location=True),
        ],
        [
            KeyboardButton(text="⬅Orqaga"),
        ],
        [
            KeyboardButton(text="⬅Bosh menyuga qaytish"),
        ]
    ],
    resize_keyboard=True
)

start_keyboard_vetdoctor = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Mening akkauntim"),
        ],
        [
            KeyboardButton(text="Adminga murojaat qilish"),
        ],
    ],
    resize_keyboard=True
)

number_first = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Telefon raqamni jo\'natish', request_contact=True)
        ],
        [
            KeyboardButton(text='⬅Bosh menyuga qaytish')
        ],
    ],
    resize_keyboard=True
)

petowner_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🐶Veterinar topish'),
        ],
        [
            KeyboardButton(text='🏥Klinika yoki VetApteka topish'),
        ],
        [
            KeyboardButton(text='Adminga murojaat qilish'),
        ],
    ],
    resize_keyboard=True
)

number = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Telefon raqamni jo\'natish', request_contact=True)
        ],
        [
            KeyboardButton(text='⬅Orqaga')
        ],
        [
            KeyboardButton(text='⬅Bosh menyuga qaytish')
        ],
    ],
    resize_keyboard=True
)

back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='⬅Orqaga')
        ],
        [
            KeyboardButton(text='⬅Bosh menyuga qaytish')
        ],
    ],
    resize_keyboard=True
)

back_first = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='⬅Bosh menyuga qaytish')
        ],
    ],
    resize_keyboard=True
)
