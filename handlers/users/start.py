import datetime
from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.menuStart import language, start_keyboard_vetdoctor, petowner_keyboard
from keyboards.default.menuStart_ru import petowner_keyboard as petowner_keyboard_ru, \
    start_keyboard_vetdoctor as start_keyboard_vetdoctor_ru
from keyboards.inline.admin_keyb import start_admin
from loader import dp, bot
from filters.private_chat import IsPrivate
from keyboards.inline.deals import typework
from keyboards.inline.deal_ru import typework_
from infos.models import Users


@dp.message_handler(IsPrivate(), CommandStart())
async def bot_start(message: types.Message):
    return await message.answer("Muloqot tilini tanlang:\n"
                                "Выберите язык:", reply_markup=language)


@dp.message_handler(IsPrivate(), text=("🇺🇿O'zbekcha", '🇺🇿Сменить язык'))
async def lang(message: types.Message):
    db = Users.objects.filter(chat_id=message.from_user.id)
    if not db:
        Users.objects.create(chat_id=message.from_user.id, full_name=message.from_user.full_name,
                             username=message.from_user.username, time_created=datetime.datetime.now())
        await message.answer(
            f"{message.from_user.full_name}, Siz kim siz?",
            reply_markup=typework)
    elif db.first().type_person == "OE":
        await message.answer("Marhamat, xizmat turini tanlang:", reply_markup=petowner_keyboard)
    elif db.first().type_person == 'DR':
        await message.answer("Marhamat, xizmat turini tanlang:", reply_markup=start_keyboard_vetdoctor)


@dp.message_handler(IsPrivate(), text=("🇷🇺Русский", '🇷🇺Tilni uzgartirish'))
async def lang_(message: types.Message):
    db = Users.objects.filter(chat_id=message.from_user.id)
    if not db:
        Users.objects.create(chat_id=message.from_user.id, full_name=message.from_user.full_name,
                             username=message.from_user.username, time_created=datetime.datetime.now())
        await message.answer(
            f"{message.from_user.full_name}, Вы кто?",
            reply_markup=typework_)
    elif db.first().type_person == "OE":
        await message.answer("Пожалуйста, выберите тип услуги:", reply_markup=petowner_keyboard_ru)
    elif db.first().type_person == 'DR':
        await message.answer("Пожалуйста, выберите тип услуги:", reply_markup=start_keyboard_vetdoctor_ru)


@dp.message_handler(IsPrivate(), text=['/start', '⬅Bosh menyuga qaytish', '⬅Вернуться в главное меню'], state="*")
async def bot(msg: types.Message, state=FSMContext):
    await bot_start(msg)
    await state.finish()


@dp.message_handler(IsPrivate(), text='Adminga murojaat qilish')
async def admin_func(msg: types.Message):
    await msg.answer('<b>Admin bilan bog`lanish:</b>\n'
                     f'📞 +998905042141\n'
                     '@alizhanovbekhruz\n', parse_mode='html')


@dp.message_handler(IsPrivate(), text='Связаться с администратором')
async def admin_func1(msg: types.Message):
    await msg.answer('<b>Связаться с администратором:</b>\n'
                     f'📞 +998905042141\n'
                     '@alizhanovbekhruz\n', parse_mode='html')
