import datetime
from app import Loc_file_media
from aiogram import types
import re
from handlers.users.start import lang, lang_
from keyboards.inline.deal_ru import City_keyb, Region_keyb, type_cl, truefalse_keyb, let_keyb, add_clinic_keyb, \
    type_vet_clinic
from keyboards.default.menuStart_ru import back_first, back, number, Loc_send
from infos.models import City, Region, Doctor, Users, Admin_bot, clinic
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from states.statesper_ru import doctor_info_, clinic_info_
import os
from aiogram.types import ParseMode

phone_re = """^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"""


@dp.callback_query_handler(text='Vetdoktor_')
async def vetdoktor(msg: types.CallbackQuery, state=FSMContext, ):
    Users.objects.filter(chat_id=msg.from_user.id).update(type_person='DR')
    await doctor_info_.full_name.set()
    await msg.message.delete()
    await msg.message.answer("Напишите свое полное имя!:",
                             reply_markup=back_first)


@dp.message_handler(state=doctor_info_.full_name)
async def full_name(msg: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['full_name'] = msg.text
    await doctor_info_.next()
    await msg.answer("Отправьте свой номер телефона", reply_markup=number)


@dp.message_handler(state=doctor_info_.number_phone, content_types=types.ContentType.CONTACT)
async def pacien_func3_2(msg: types.ContentType, state=FSMContext):
    keyb = back.keyboard
    keyb = [[types.KeyboardButton(text='Нет')]] + keyb
    txt = msg['contact']['phone_number']
    async with state.proxy() as data:
        data['number_phone'] = txt
    await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id - 1)
    await msg.delete()
    await doctor_info_.next()
    await msg.answer("Загрузите свое изображение (напишите «Нет», если не найдено):",
                     reply_markup=types.ReplyKeyboardMarkup(
                         keyboard=keyb, resize_keyboard=True))


@dp.message_handler(state=doctor_info_.number_phone)
async def number_phone(msg: types.Message, state=FSMContext):
    if msg.text == '⬅Назад':
        await doctor_info_.previous()
        await msg.answer("Напишите свое полное имя!:",
                         reply_markup=back_first)
        return
    if not re.match(phone_re, msg.text):
        await msg.answer("Напишите правильный номер телефона!")
        return
    keyb = [[types.KeyboardButton(text='Нет')]] + back.keyboard
    async with state.proxy() as data:
        data['number_phone'] = msg.text
    await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id - 1)
    await msg.delete()
    await doctor_info_.next()
    await msg.answer("Загрузите свое изображение (напишите «Нет», если не найдено):",
                     reply_markup=types.ReplyKeyboardMarkup(
                         keyboard=keyb, resize_keyboard=True))


@dp.message_handler(state=doctor_info_.photo, text='⬅Назад')
async def photo(msg: types.Message, state=FSMContext):
    await doctor_info_.previous()
    await msg.answer("Отправьте свой номер телефона", reply_markup=number)
    return


@dp.message_handler(state=doctor_info_.photo, text='Нет')
async def photo(msg: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['photo'] = 'Нет'
        data['location_to_serve'] = []
    await doctor_info_.next()
    await msg.answer('Отлично!', reply_markup=back)
    await msg.answer("Выберите вашу регион обслуживания:", reply_markup=City_keyb('citydok11'))


@dp.message_handler(state=doctor_info_.photo, content_types=types.ContentTypes.PHOTO)
async def photo_(msg: types.Message, state=FSMContext, backact=False):
    if backact:
        return await msg.answer("", reply_markup=City_keyb('citydok11'))
    async with state.proxy() as data:
        data['photo'] = msg.photo[-1]
        data['location_to_serve'] = []
    await doctor_info_.next()
    await msg.answer('Отлично!', reply_markup=back)
    await msg.answer("Выберите вашу регион обслуживания:", reply_markup=City_keyb('citydok11'))


"""Tumanlar"""


@dp.message_handler(state=doctor_info_.location_to_serve, text='⬅Назад')
async def deals_func2(msg: types.Message, state=FSMContext):
    keyb = [[types.KeyboardButton(text='Нет')]] + back.keyboard
    await doctor_info_.previous()
    await msg.answer("Загрузите свое изображение (напишите «Нет», если не найдено):",
                     reply_markup=types.ReplyKeyboardMarkup(
                         keyboard=keyb, resize_keyboard=True))
    return


@dp.callback_query_handler(lambda a: 'citydok11_' in a.data, state=doctor_info_.location_to_serve)
async def location_to_serve(msg: types.CallbackQuery, state=FSMContext):
    _, city_id = msg.data.split('_')
    await msg.message.delete()
    async with state.proxy() as data:
        await msg.message.answer("Выберите вашу район обслуживания:",
                                 reply_markup=await Region_keyb(city_id, data['location_to_serve']))


@dp.callback_query_handler(lambda a: 'regiondru_' in a.data, state=doctor_info_.location_to_serve)
async def deals_func3(msg: types.CallbackQuery, state=FSMContext):
    if msg.data == 'regiondru_back':
        await msg.message.delete()
        await photo_(msg.message, backact=True)
    elif msg.data == 'regiondru_save':
        await msg.message.delete()
        await doctor_info_.next()
        await msg.message.answer('У вас есть клиника или Вет аптека?', reply_markup=truefalse_keyb)
    else:
        keyb, remov = await type_cl(msg.data, msg.message.reply_markup)
        if remov:
            async with state.proxy() as data:
                data['location_to_serve'].remove(remov)
            await msg.message.edit_reply_markup(keyb)
        else:
            async with state.proxy() as data:

                data['location_to_serve'].append(msg.data.split('_')[1])
            await msg.message.edit_reply_markup(keyb)


"""End Tumanlar"""


@dp.message_handler(state=doctor_info_.clinic_bool, text='⬅Назад')
async def clinic_bool(msg: types.Message, state=FSMContext):
    await doctor_info_.previous()
    await msg.answer("Выберите вашу регион обслуживания:", reply_markup=City_keyb('citydok11'))


@dp.callback_query_handler(lambda a: 'trueflse_' in a.data, state=doctor_info_.clinic_bool)
async def thereclinic(msg: types.CallbackQuery, state=FSMContext):
    await msg.message.delete()
    if msg.data == 'trueflse_true':
        async with state.proxy() as data:
            data['clinic_bool'] = True
    else:
        async with state.proxy() as data:
            data['clinic_bool'] = False
    await doctor_info_.next()
    await msg.message.answer('Какие услуги вы можете предоставить (напишите о себе):')


@dp.message_handler(state=doctor_info_.specialities)
async def sending_func(msg: types.Message, state=FSMContext):
    if msg.text == '⬅Назад':
        await doctor_info_.previous()
        await msg.answer('У вас есть клиника или Вет аптека?', reply_markup=truefalse_keyb)
        return
    await msg.answer('Ваша информация получена, пожалуйста, подождите! \n'
                     'Ваша заявка будет рассмотрена в течение 24 часов!')
    async with state.proxy() as data:
        file = data['photo']
        print(type(file))
        if file == 'Нет':
            file_path = None
        else:
            date = datetime.datetime.now()
            file_path = f"doctors/{date.year}/{date.month}/{date.day}/{data['photo'].file_id}.jpg"
            await file.download(destination_file=os.path.join(Loc_file_media, file_path))
            print(file_path)
        user_obj = Users.objects.get(chat_id=msg.from_user.id)
        doctor_obj = Doctor.objects.create(user=user_obj, full_name=data['full_name'],
                                           phone=data['number_phone'], photo=file_path, description=msg.text,
                                           clinic_bool=data['clinic_bool'], username=msg.from_user.username)
        doctor_obj.work_region.set(map(lambda a: int(a), data['location_to_serve']))
    for admin in Admin_bot.objects.all():
        await bot.send_message(admin.chat_id, f"Yangi doktor qo'shildi!\n"
                                              f"Ismi: {data['full_name']}\n"
                                              f"Telefon raqami: {data['number_phone']}\n\n"
                                              f"Xizmat qilish hududlari(ID): {data['location_to_serve']}\n\n"
                                              f"Klinika yoki Vet aptekasi bormi: {data['clinic_bool']}\n",
                               reply_markup=let_keyb(msg.from_user.id))
    await state.finish()
    return await lang_(msg)


@dp.callback_query_handler(lambda a: 'letTre||' in a.data)
async def letTrue(msg: types.CallbackQuery):
    _, user_id = msg.data.split('||')
    for admin in Admin_bot.objects.all():
        print(admin.chat_id)
        await bot.send_message(chat_id=int(admin.chat_id),
                               text=f"Админ {msg.from_user.get_mention(as_html=True)} \nDotorlikka rusxat berdi:{user_id} shu odamga")
    await bot.send_message(chat_id=user_id, text=f"Вам дали разрешение на ветеринарию🎉")
    doctor_obj = Doctor.objects.filter(user__chat_id=user_id)
    doctor_obj.update(status=True)
    if doctor_obj.first().clinic_bool:
        await bot.send_message(chat_id=user_id, text=f"Добавьте свою Клинику/ВетАптеку/Лабораторию",
                               reply_markup=add_clinic_keyb)


@dp.callback_query_handler(text='addclinc_')
async def add_clinic(msg: types.CallbackQuery):
    await msg.message.delete()
    await clinic_info_.type_clin.set()
    await msg.message.answer('Отлично!', reply_markup=back_first)
    await msg.message.answer("У вас клиника или Вет Аптека или Лаборатория?:", reply_markup=type_vet_clinic)


@dp.callback_query_handler(lambda a: 'typvetklinru_' in a.data, state=clinic_info_.type_clin)
async def type_clinic(msg: types.CallbackQuery, state=FSMContext):
    _, type_clinic = msg.data.split('_')
    await msg.message.delete()
    async with state.proxy() as data:
        data['type_clinicap'] = type_clinic
    await clinic_info_.next()
    if type_clinic == 'VT':
        s = 'Вет Аптеки'
    elif type_clinic == 'LB':
        s = 'Лаборатории'
    else:
        s = 'Клиники'
    await msg.message.answer(f"Введите название вашей {s}", reply_markup=back)


@dp.message_handler(state=clinic_info_.name)
async def name_clinic(msg: types.Message, state=FSMContext):
    if msg.text == '⬅Назад':
        await clinic_info_.previous()
        await msg.answer("У вас Клиника или Вет Аптека или Лаборатория?:", reply_markup=type_vet_clinic)
        return
    async with state.proxy() as data:
        data['name'] = msg.text
        if data['type_clinicap'] == 'VT':
            s = 'Вет Аптека'
        elif data['type_clinicap'] == 'LB':
            s = 'Лаборатория'
        else:
            s = 'Клиника'
    await msg.delete()
    await clinic_info_.next()
    await msg.answer(f"Где находится ваша {s}:", reply_markup=City_keyb('cityclinc'))


@dp.message_handler(state=clinic_info_.region, text='⬅Назад')
async def region_clinic(msg: types.Message, state=FSMContext):
    await clinic_info_.previous()
    async with state.proxy() as data:
        if data['type_clinicap'] == 'VT':
            s = 'Вет Аптека'
        elif data['type_clinicap'] == 'LB':
            s = 'Лаборатория'
        else:
            s = 'Клиника'
        await msg.answer(f"Введите название вашей {s}:", reply_markup=type_vet_clinic)


@dp.callback_query_handler(lambda a: 'cityclinc_' in a.data, state=clinic_info_.region)
async def locationcity(msg: types.CallbackQuery, state=FSMContext):
    _, city_id = msg.data.split('_')
    await msg.message.delete()
    async with state.proxy() as data:
        data['city'] = city_id
        if data['type_clinicap'] == 'VT':
            s = 'Вет Аптеки'
        elif data['type_clinicap'] == 'LB':
            s = 'Лаборатории'
        else:
            s = 'Клиники'
    await clinic_info_.next()
    await msg.message.answer(f"Отправьте локацию вашей {s}", reply_markup=Loc_send)


@dp.message_handler(state=clinic_info_.location, text='⬅Назад')
async def location_clinic(msg: types.Message, state=FSMContext):
    await clinic_info_.previous()
    async with state.proxy() as data:
        if data['type_clinicap'] == 'VT':
            s = 'Вет Аптека'
        elif data['type_clinicap'] == 'LB':
            s = 'Лаборатория'
        else:
            s = 'Клиника'
    await msg.answer(f"Где находится ваша {s}::", reply_markup=City_keyb('cityclinc'))


@dp.message_handler(state=clinic_info_.location, content_types=types.ContentTypes.LOCATION)
async def location_clinic(msg: types.ContentTypes.LOCATION, state=FSMContext):
    keyb = [[types.KeyboardButton(text='Нет')]] + back.keyboard
    async with state.proxy() as data:
        data['latitude'] = msg.location.latitude
        data['longitude'] = msg.location.longitude
        if data['type_clinicap'] == 'VT':
            s = 'Вет Аптеки'
        elif data['type_clinicap'] == 'LB':
            s = 'Лаборатории'
        else:
            s = 'Клиники'
    await msg.delete()
    await clinic_info_.next()
    await msg.answer(f"Загрузите изображение {s} (напишите «Нет», если не найдено):",
                     reply_markup=types.ReplyKeyboardMarkup(
                         keyboard=keyb, resize_keyboard=True))


@dp.message_handler(state=clinic_info_.photo, text='⬅Назад')
async def photo_clinic(msg: types.Message, state=FSMContext):
    await clinic_info_.previous()
    async with state.proxy() as data:
        if data['type_clinicap'] == 'VT':
            s = 'Вет Аптека'
        elif data['type_clinicap'] == 'LB':
            s = 'Лаборатория'
        else:
            s = 'Клиника'
    await msg.answer(f"Отправьте локацию вашей {s}", reply_markup=Loc_send)


@dp.message_handler(state=clinic_info_.photo, text='Нет')
async def photo_clinic(msg: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['photo'] = 'Нет'
        if data['type_clinicap'] == 'VT':
            s = 'Вет Аптеки'
        elif data['type_clinicap'] == 'LB':
            s = 'Лаборатории'
        else:
            s = 'Клиники'
    await clinic_info_.next()
    await msg.answer(f"Напишите краткое описание вашей {s}:", reply_markup=back)


@dp.message_handler(state=clinic_info_.photo, content_types=types.ContentTypes.PHOTO)
async def photo_clinic(msg: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['photo'] = msg.photo[-1]
        if data['type_clinicap'] == 'VT':
            s = 'Вет Аптеки'
        elif data['type_clinicap'] == 'LB':
            s = 'Лаборатории'
        else:
            s = 'Клиники'
    await clinic_info_.next()
    await msg.answer(f"Напишите краткое описание вашей {s}:", reply_markup=back)


@dp.message_handler(state=clinic_info_.description)
async def description_clinic(msg: types.Message, state=FSMContext):
    async with state.proxy() as data:
        if data['type_clinicap'] == 'VT':
            s = 'Вет Аптеки'
        elif data['type_clinicap'] == 'LB':
            s = 'Лаборатории'
        else:
            s = 'Клиники'
        if msg.text == '⬅Назад':
            await clinic_info_.previous()
            await msg.answer(f"Загрузите изображение {s} (напишите «Нет», если не найдено):",
                             reply_markup=types.ReplyKeyboardMarkup(
                                 keyboard=[[types.KeyboardButton(text='Нет')]] + back.keyboard,
                                 resize_keyboard=True))
            return
        data['description'] = msg.text
        file = data['photo']
        print(type(file))
        if file == 'Нет':
            file_path = None
        else:
            date = datetime.datetime.now()
            file_path = f"clinic/{date.year}/{date.month}/{date.day}/{data['photo'].file_id}.jpg"
            await file.download(destination_file=os.path.join(Loc_file_media, file_path))
            print(file_path)
        doctor_obj = Doctor.objects.get(user__chat_id=msg.from_user.id)
        clinic.objects.create(owner=doctor_obj, name=data['name'],
                              region=City.objects.get(id=data['city']),
                              latitude=data['latitude'], longitude=data['longitude'],
                              photo=file_path, description=data['description'], type_clinic=data['type_clinicap'])
    for admin in Admin_bot.objects.all():
        await bot.send_message(chat_id=admin.chat_id,
                               text=f"Yangi {s} qo'shildi!\n"
                                    f"Nomi: {data['name']}\n"
                                    f"Shaxar: {City.objects.get(id=data['city'])}\n"
                                    f"Lokatsiyasi: https://www.google.com/maps/search/?api=1&query={data['latitude']},{data['longitude']}\n"
                                    f"{s} haqida: {msg.text}\n")
    await state.finish()
    return await lang(msg)
