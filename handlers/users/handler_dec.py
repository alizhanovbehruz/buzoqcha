import datetime
from app import Loc_file_media
from aiogram import types
import re
from handlers.users.start import lang
from keyboards.inline.deals import City_keyb, Region_keyb, type_cl, truefalse_keyb, let_keyb, add_clinic_keyb, \
    type_vet_clinic
from keyboards.default.menuStart import back_first, back, number, Loc_send
from infos.models import City, Region, Doctor, Users, Admin_bot, clinic
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from states.statesper import doctor_info, clinic_info
import os
from aiogram.types import ParseMode

phone_re = """^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"""


@dp.callback_query_handler(text='Vetdoktor')
async def vetdoktor(msg: types.CallbackQuery, state=FSMContext, ):
    Users.objects.filter(chat_id=msg.from_user.id).update(type_person='DR')
    await doctor_info.full_name.set()
    await msg.message.delete()
    await msg.message.answer("Ism Familiyangizni to'liq yozib qoldiring!:",
                             reply_markup=back_first)


@dp.message_handler(state=doctor_info.full_name)
async def full_name(msg: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['full_name'] = msg.text
    await doctor_info.next()
    await msg.answer("Telefon raqamingizni kiriting:", reply_markup=number)


@dp.message_handler(state=doctor_info.number_phone, content_types=types.ContentType.CONTACT)
async def pacien_func3_2(msg: types.ContentType, state=FSMContext):
    keyb = back.keyboard
    keyb = [[types.KeyboardButton(text='Yoq')]] + keyb
    txt = msg['contact']['phone_number']
    async with state.proxy() as data:
        data['number_phone'] = txt
    await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id - 1)
    await msg.delete()
    await doctor_info.next()
    await msg.answer("Rasmingizni yuklang (bulmasa agar 'Yoq' deb yozing):",
                     reply_markup=types.ReplyKeyboardMarkup(
                         keyboard=keyb, resize_keyboard=True))


@dp.message_handler(state=doctor_info.number_phone)
async def number_phone(msg: types.Message, state=FSMContext):
    if msg.text == '⬅Orqaga':
        await doctor_info.previous()
        await msg.answer("Ism Familiyangizni to'liq yozib qoldiring!:",
                         reply_markup=back_first)
        return
    if not re.match(phone_re, msg.text):
        await msg.answer("Telefon raqamingizni to'g'ri kiriting:")
        return
    keyb = [[types.KeyboardButton(text='Yoq')]] + back.keyboard
    async with state.proxy() as data:
        data['number_phone'] = msg.text
    await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id - 1)
    await msg.delete()
    await doctor_info.next()
    await msg.answer("Rasmingizni yuklang (bulmasa agar 'Yoq' deb yozing):",
                     reply_markup=types.ReplyKeyboardMarkup(
                         keyboard=keyb, resize_keyboard=True))


@dp.message_handler(state=doctor_info.photo, text='⬅Orqaga')
async def photo(msg: types.Message, state=FSMContext):
    await doctor_info.previous()
    await msg.answer("Telefon raqamingizni kiriting:", reply_markup=number)
    return


@dp.message_handler(state=doctor_info.photo, text='Yoq')
async def photo(msg: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['photo'] = 'Yoq'
        data['location_to_serve'] = []
    await doctor_info.next()
    await msg.answer('Ajoyib', reply_markup=back)
    await msg.answer("Xizmat ko'rsata oladigan hududingizni tanlang:", reply_markup=City_keyb('citydok'))


@dp.message_handler(state=doctor_info.photo, content_types=types.ContentTypes.PHOTO)
async def photo_(msg: types.Message, state=FSMContext, backact=False):
    if backact:
        return await msg.answer("Xizmat ko'rsata oladigan hududingizni tanlang:", reply_markup=City_keyb('citydok'))
    async with state.proxy() as data:
        data['photo'] = msg.photo[-1]
        data['location_to_serve'] = []
    await doctor_info.next()
    await msg.answer('Ajoyib', reply_markup=back)
    await msg.answer("Xizmat ko'rsata oladigan hududingizni tanlang:", reply_markup=City_keyb('citydok'))


"""Tumanlar"""


@dp.message_handler(state=doctor_info.location_to_serve, text='⬅Orqaga')
async def deals_func2(msg: types.Message, state=FSMContext):
    keyb = [[types.KeyboardButton(text='Yoq')]] + back.keyboard
    await doctor_info.previous()
    await msg.answer("Rasmingizni yuklang (bulmasa agar 'Yoq' deb yozing):",
                     reply_markup=types.ReplyKeyboardMarkup(
                         keyboard=keyb, resize_keyboard=True))
    return


@dp.callback_query_handler(lambda a: 'citydok_' in a.data, state=doctor_info.location_to_serve)
async def location_to_serve(msg: types.CallbackQuery, state=FSMContext):
    _, city_id = msg.data.split('_')
    await msg.message.delete()
    async with state.proxy() as data:
        await msg.message.answer("Xizmat ko'rsatadigan tumanlarni tanlang",
                                 reply_markup=await Region_keyb(city_id, data['location_to_serve']))


@dp.callback_query_handler(lambda a: 'regiondok_' in a.data, state=doctor_info.location_to_serve)
async def deals_func3(msg: types.CallbackQuery, state=FSMContext):
    if msg.data == 'regiondok_back':
        await msg.message.delete()
        await photo_(msg.message, backact=True)
    elif msg.data == 'regiondok_save':
        await msg.message.delete()
        await doctor_info.next()
        await msg.message.answer('Sizning klinikangiz yoki Vet Aptekangiz bormi?', reply_markup=truefalse_keyb)
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


@dp.message_handler(state=doctor_info.clinic_bool, text='⬅Orqaga')
async def clinic_bool(msg: types.Message, state=FSMContext):
    await doctor_info.previous()
    await msg.answer("Xizmat ko'rsata oladigan hududingizni tanlang:", reply_markup=City_keyb('citydok'))
    return


@dp.callback_query_handler(lambda a: 'truefalse_' in a.data, state=doctor_info.clinic_bool)
async def thereclinic(msg: types.CallbackQuery, state=FSMContext):
    await msg.message.delete()
    if msg.data == 'truefalse_true':
        async with state.proxy() as data:
            data['clinic_bool'] = True
    else:
        async with state.proxy() as data:
            data['clinic_bool'] = False
    await doctor_info.next()
    await msg.message.answer('Qanaqa xizmatlar kursata olasiz(O\'ziz haqinginda yozing):')


@dp.message_handler(state=doctor_info.specialities)
async def sending_func(msg: types.Message, state=FSMContext):
    if msg.text == '⬅Orqaga':
        await doctor_info.previous()
        await msg.answer('Sizning klinikangiz yoki Vet Aptekangiz bormi?', reply_markup=truefalse_keyb)
        return
    await msg.answer('Sizning ma\'lumotlaringiz qabul qilindi, iltimos kuting! \n'
                     'Sizning ma\'lumotlaringizni tekshirib chiqib sizga javob qaytaramiz!')
    async with state.proxy() as data:
        file = data['photo']
        print(type(file))
        if file == 'Yoq':
            file_path = None
        else:
            date = datetime.datetime.now()
            file_path = f"doctors/{date.year}/{date.month}/{date.day}/{data['photo'].file_id}.jpg"
            await file.download(destination_file=os.path.join(Loc_file_media, file_path))
            print(file_path)
        user_obj = Users.objects.get(chat_id=msg.from_user.id)
        doctor_obj = Doctor.objects.create(user=user_obj, full_name=data['full_name'],
                                           phone=data['number_phone'], photo=file_path,
                                           clinic_bool=data['clinic_bool'], description=msg.text,
                                           username=msg.from_user.username)
        doctor_obj.work_region.set(map(lambda a: int(a), data['location_to_serve']))
    for admin in Admin_bot.objects.all():
        await bot.send_message(admin.chat_id, f"Yangi doktor qo'shildi!\n"
                                              f"{data['full_name']}\n"
                                              f"{data['number_phone']}\n"
                                              f"{data['location_to_serve']}\n"
                                              f"{data['clinic_bool']}\n", reply_markup=let_keyb(msg.from_user.id))
    await state.finish()
    return await lang(msg)


@dp.callback_query_handler(lambda a: 'letTrue||' in a.data)
async def letTrue(msg: types.CallbackQuery):
    _, user_id = msg.data.split('||')
    for admin in Admin_bot.objects.all():
        print(admin.chat_id)
        await bot.send_message(chat_id=int(admin.chat_id),
                               text=f"admin {msg.from_user.get_mention(as_html=True)} \nDotorlikka rusxat berdi:{user_id} shu odamga")
    await bot.send_message(chat_id=user_id, text=f"Sizga vetenarlikka ruxsat berildi🎉")
    doctor_obj = Doctor.objects.filter(user__chat_id=user_id)
    doctor_obj.update(status=True)
    if doctor_obj.first().clinic_bool:
        await bot.send_message(chat_id=user_id, text=f"Klinika/VetApteka/Laboratoriyani qo'shing",
                               reply_markup=add_clinic_keyb)


@dp.callback_query_handler(text='addclinic')
async def add_clinic(msg: types.CallbackQuery):
    await msg.message.delete()
    await clinic_info.type_clin.set()
    await msg.message.answer('Ajoyib!', reply_markup=back_first)
    await msg.message.answer("Sizda klinikami yoki Vet Apteka yoki Laboratoriyami?", reply_markup=type_vet_clinic)


@dp.callback_query_handler(lambda a: 'typvetklinik_' in a.data, state=clinic_info.type_clin)
async def type_clinic(msg: types.CallbackQuery, state=FSMContext):
    _, type_clinic = msg.data.split('_')
    await msg.message.delete()
    async with state.proxy() as data:
        data['type_clinicap'] = type_clinic
    await clinic_info.next()
    if type_clinic == 'VT':
        s = 'Vet Apteka'
    elif type_clinic == 'LB':
        s = 'Laboratoriya'
    else:
        s = 'Klinika'
    await msg.message.answer(f"{s}ngiz nomini kiriting:", reply_markup=back)


@dp.message_handler(state=clinic_info.name)
async def name_clinic(msg: types.Message, state=FSMContext):
    if msg.text == '⬅Orqaga':
        await clinic_info.previous()
        await msg.answer("Sizda klinikami yoki Vet Apteka yoki Laboratoriyami?", reply_markup=type_vet_clinic)
        return
    async with state.proxy() as data:
        data['name'] = msg.text
        if data['type_clinicap'] == 'VT':
            s = 'Vet Apteka'
        elif type_clinic == 'LB':
            s = 'Laboratoriya'
        else:
            s = 'Klinika'
    await msg.delete()
    await clinic_info.next()
    await msg.answer(f"{s}ngiz joylashgan hududni tanlang:", reply_markup=City_keyb('cityclinic'))


@dp.message_handler(state=clinic_info.region, text='⬅Orqaga')
async def region_clinic(msg: types.Message, state=FSMContext):
    await clinic_info.previous()
    async with state.proxy() as data:
        if data['type_clinicap'] == 'VT':
            s = 'Vet Apteka'
        elif type_clinic == 'LB':
            s = 'Laboratoriya'
        else:
            s = 'Klinika'
    await msg.answer(f"{s}ngiz nomini kiriting:", reply_markup=back)


@dp.callback_query_handler(lambda a: 'cityclinic_' in a.data, state=clinic_info.region)
async def locationcity(msg: types.CallbackQuery, state=FSMContext):
    _, city_id = msg.data.split('_')
    await msg.message.delete()
    async with state.proxy() as data:
        data['city'] = city_id
        if data['type_clinicap'] == 'VT':
            s = 'Vet Apteka'
        elif type_clinic == 'LB':
            s = 'Laboratoriya'
        else:
            s = 'Klinika'
    await clinic_info.next()
    await msg.message.answer(f"{s}ngizni lokatsiyasini jo'nating!", reply_markup=Loc_send)


@dp.message_handler(state=clinic_info.location, text='⬅Orqaga')
async def location_clinic(msg: types.Message, state=FSMContext):
    await clinic_info.previous()
    async with state.proxy() as data:
        if data['type_clinicap'] == 'VT':
            s = 'Vet Apteka'
        elif type_clinic == 'LB':
            s = 'Laboratoriya'
        else:
            s = 'Klinika'
    await msg.answer(f"{s}ngiz joylashgan hududni tanlang:", reply_markup=City_keyb('cityclinic'))


@dp.message_handler(state=clinic_info.location, content_types=types.ContentTypes.LOCATION)
async def location_clinic(msg: types.ContentTypes.LOCATION, state=FSMContext):
    keyb = [[types.KeyboardButton(text='Yoq')]] + back.keyboard
    async with state.proxy() as data:
        data['latitude'] = msg.location.latitude
        data['longitude'] = msg.location.longitude
        if data['type_clinicap'] == 'VT':
            s = 'Vet Apteka'
        elif type_clinic == 'LB':
            s = 'Laboratoriya'
        else:
            s = 'Klinika'
    await msg.delete()
    await clinic_info.next()
    await msg.answer(f"{s}ngiz rasmini jo'nating (agar yo'q bo'lsa 'Yoq' deb yozing):",
                     reply_markup=types.ReplyKeyboardMarkup(
                         keyboard=keyb, resize_keyboard=True))


@dp.message_handler(state=clinic_info.photo, text='⬅Orqaga')
async def photo_clinic(msg: types.Message, state=FSMContext):
    await clinic_info.previous()
    async with state.proxy() as data:
        if data['type_clinicap'] == 'VT':
            s = 'Vet Apteka'
        elif type_clinic == 'LB':
            s = 'Laboratoriya'
        else:
            s = 'Klinika'
    await msg.answer(f"{s}ngizni lokatsiyasini jo'nating!", reply_markup=Loc_send)


@dp.message_handler(state=clinic_info.photo, text='Yoq')
async def photo_clinic(msg: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['photo'] = 'Yoq'
        if data['type_clinicap'] == 'VT':
            s = 'Vet Apteka'
        elif type_clinic == 'LB':
            s = 'Laboratoriya'
        else:
            s = 'Klinika'
    await clinic_info.next()
    await msg.answer(f"{s}ngiz haqida qisqacha ma'lumot yozing:", reply_markup=back)


@dp.message_handler(state=clinic_info.photo, content_types=types.ContentTypes.PHOTO)
async def photo_clinic(msg: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['photo'] = msg.photo[-1]
        if data['type_clinicap'] == 'VT':
            s = 'Vet Apteka'
        elif type_clinic == 'LB':
            s = 'Laboratoriya'
        else:
            s = 'Klinika'
    await clinic_info.next()
    await msg.answer(f"{s}ngiz haqida qisqacha ma'lumot yozing:")


@dp.message_handler(state=clinic_info.description)
async def description_clinic(msg: types.Message, state=FSMContext):
    async with state.proxy() as data:
        if data['type_clinicap'] == 'VT':
            s = 'Vet Apteka'
        elif type_clinic == 'LB':
            s = 'Laboratoriya'
        else:
            s = 'Klinika'
        if msg.text == '⬅Orqaga':
            await clinic_info.previous()
            await msg.answer(f"{s}ngizni rasmini jo'nating (agar yo'q bo'lsa 'Yoq' deb yozing):",
                             reply_markup=types.ReplyKeyboardMarkup(
                                 keyboard=[[types.KeyboardButton(text='Нет')]] + back.keyboard, resize_keyboard=True))
            return
        data['description'] = msg.text
        file = data['photo']
        print(type(file))
        if file == 'Yoq':
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
