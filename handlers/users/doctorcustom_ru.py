import datetime
import os

from app import Loc_file_media
from filters import IsPrivate
from handlers.users.handler_dec_ru import vetdoktor,  phone_re, add_clinic
from handlers.users.start import bot_start
from keyboards.inline.deal_ru import doctor_editing_menu, reg_again, doctor_editing_menu_into, City_keyb, \
    Region_keyb, type_cl, Region_keyb_update, clinic_editing, clinic_editing_menu_into
from loader import dp, bot
from aiogram import types
from keyboards.default.menuStart_ru import back, back_first, number_first, Loc_send
from aiogram.dispatcher import FSMContext
from infos.models import Users, Doctor, clinic, City
from states.statesper_ru import doctor_info_, doctor_update_, doctor_updatephone_, doctor_updatephoto_, doctor_updatedecs_, \
    doctor_updatelocation_, clinic_update_, clinic_updatecity_, clinic_updatephoto_, clinic_updatelocation_, \
    clinic_updatedecs_
import re


@dp.message_handler(IsPrivate(), text=['/start', '⬅Вернуться в главное меню'], state="*")
async def botprevius(msg: types.Message, state=FSMContext):
    await bot_start(msg)
    await state.finish()


@dp.message_handler(text='Мой аккаунт')
async def custom_func1(message: types.Message):
    doctor_obj = Doctor.objects.filter(user__chat_id=message.from_user.id)
    if doctor_obj:
        doctor_obj = doctor_obj.first()
        s = ''
        for i in doctor_obj.work_region.all():
            s += f"Область {i.city}, {i.name} \n\n"
        await message.answer('<b>Вы ветеринарный врач!</b>\n\n'
                             f"<b>ФИО:</b> {doctor_obj.full_name}\n\n"
                             f"<b>Ваша номер телефона:</b> {doctor_obj.phone}\n\n"
                             f"<b>Адреса, которые вы можете предоставить услугу:</b>\n"
                             f"{s}\n\n",parse_mode='html')
        if doctor_obj.photo:
            await bot.send_photo(message.chat.id, photo=open(f'media/{doctor_obj.photo}', 'rb'),
                                 caption='<b>Ваша фотография</b>', parse_mode='html')
        else:
            await message.answer('Фото не предоставлено')

        if doctor_obj.clinic_bool:
            await message.answer('Ваши обьекты(Клиники  :')
            clinic_obj = clinic.objects.filter(owner=doctor_obj)
            for i in clinic_obj:
                if i.photo:
                    await bot.send_photo(message.chat.id, photo=open(f'media/{i.photo}', 'rb'),
                                         caption=f'<b>{i.name}</b>\n'
                                                 f'<i>{i.region}</i>\n\n'
                                                 f'{i.description}', parse_mode='html',
                                         reply_markup=types.InlineKeyboardMarkup(
                                             inline_keyboard=[
                                                 [
                                                     types.InlineKeyboardButton(text='Открыть в Google Картах',
                                                                                url=f'https://www.google.com/maps/search/?api=1&query={i.latitude},{i.longitude}')
                                                 ]
                                             ]
                                         ))
                else:
                    await message.answer(f'<b>{i.name}</b>\n'
                                         f'<i>{i.region}</i>\n\n'
                                         f'{i.description}', parse_mode='html',
                                         reply_markup=types.InlineKeyboardMarkup(
                                             inline_keyboard=[
                                                 [
                                                     types.InlineKeyboardButton(text='Открыть в Google Картах',
                                                                                url=f'https://www.google.com/maps/search/?api=1&query={i.latitude},{i.longitude}')
                                                 ]
                                             ]
                                         ))
        else:
            await message.answer('У вас нет клиники')

        await message.answer('Пожалуйста, выберите услугу:', reply_markup=doctor_editing_menu)
    else:
        await message.answer('Отлично', reply_markup=types.ReplyKeyboardRemove())
        await message.answer('Администратор еще не дал вам доступ, или при регистрации произошла ошибка.',
                             reply_markup=reg_again)


@dp.callback_query_handler(text='doctoreditinru_')
async def custom_func2(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Выберите тип услуги:', reply_markup=doctor_editing_menu_into)


@dp.callback_query_handler(text='doctoreditingfru_')
async def custom_func3(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Введите ваше ФИО:', reply_markup=back_first)
    await doctor_update_.updating.set()


@dp.message_handler(state=doctor_update_.updating)
async def custom_func4(message: types.Message, state=FSMContext):
    Doctor.objects.filter(user__chat_id=message.from_user.id).update(full_name=message.text)
    await message.answer('Ваше имя успешно изменено', reply_markup=doctor_editing_menu_into)
    await state.finish()


@dp.callback_query_handler(text='doctoreditingphoru_')
async def custom_func5(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Введите свой номер телефона:', reply_markup=number_first)
    await doctor_updatephone_.updating.set()


@dp.message_handler(state=doctor_updatephone_.updating)
async def custom_func6(message: types.Message, state=FSMContext):
    if not re.match(phone_re, message.text):
        await message.answer('Вы неправильно ввели номер телефона!!!, введите его правильно:')
        return
    Doctor.objects.filter(user__chat_id=message.from_user.id).update(phone=message.text)
    await message.answer('Ваш номер телефона успешно изменен', reply_markup=doctor_editing_menu_into)
    await state.finish()


@dp.message_handler(state=doctor_updatephone_.updating, content_types=types.ContentTypes.CONTACT)
async def custom_func7(message: types.Message, state=FSMContext):
    Doctor.objects.filter(user__chat_id=message.from_user.id).update(phone=message.contact.phone_number)
    await message.answer('Ваш номер телефона успешно изменен', reply_markup=doctor_editing_menu_into)
    await state.finish()


@dp.callback_query_handler(text='doctoreditingphoru_')
async def custom_func8(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Отправьте фото:', reply_markup=back_first)
    await doctor_updatephoto_.updating.set()


@dp.message_handler(state=doctor_updatephoto_.updating, content_types=types.ContentTypes.PHOTO)
async def custom_func9(message: types.Message, state=FSMContext):
    photo = message.photo[-1]
    date = datetime.datetime.now()
    file_path = f"doctors/{date.year}/{date.month}/{date.day}/{photo.file_id}.jpg"
    await photo.download(destination_file=os.path.join(Loc_file_media, file_path))
    Doctor.objects.filter(user__chat_id=message.from_user.id).update(photo=file_path)
    await message.answer('Фото успешно изменено', reply_markup=doctor_editing_menu_into)
    await state.finish()


@dp.callback_query_handler(text='doctoreditingderu_')
async def custom_func10(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Введите описание:', reply_markup=back_first)
    await doctor_updatedecs_.updating.set()


@dp.message_handler(state=doctor_updatedecs_.updating)
async def custom_func11(message: types.Message, state=FSMContext):
    Doctor.objects.filter(user__chat_id=message.from_user.id).update(description=message.text)
    await message.answer('Описание успешно именён', reply_markup=doctor_editing_menu_into)
    await state.finish()


@dp.callback_query_handler(text='doctoreditinglocatiru_')
async def custom_func12(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Введите адрес:', reply_markup=City_keyb('cityd7k'))
    await doctor_updatelocation_.updating.set()


"""Tumanlar"""


@dp.callback_query_handler(lambda a: 'cityd7k_' in a.data, state=doctor_updatelocation_.updating)
async def location_to_serve(msg: types.CallbackQuery, state=FSMContext):
    _, city_id = msg.data.split('_')
    locat_obj = list(
        Doctor.objects.filter(user__chat_id=msg.from_user.id).first().work_region.all().values_list('id', flat=True))
    async with state.proxy() as data:
        data['location_to_serve'] = locat_obj
    print(locat_obj)
    await msg.message.delete()
    await msg.message.answer("Выберите обслуживаемые районы",
                             reply_markup=await Region_keyb_update(city_id, data['location_to_serve']))


@dp.callback_query_handler(lambda a: 'regiondok_' in a.data, state=doctor_updatelocation_.updating)
async def deals_func3(msg: types.CallbackQuery, state=FSMContext):
    if msg.data == 'regiondok_save':
        await msg.message.delete()
        async with state.proxy() as data:
            print(data['location_to_serve'])
            Doctor.objects.filter(user__chat_id=msg.from_user.id).first().work_region.set(data['location_to_serve'])
        await msg.message.answer('Районы обслуживания успешно изменены',
                                 reply_markup=doctor_editing_menu_into)
        await state.finish()
    else:
        keyb, remov = await type_cl(msg.data, msg.message.reply_markup)
        print(remov)
        if remov:
            async with state.proxy() as data:
                print(data['location_to_serve'])
                data['location_to_serve'].remove(int(remov))
            await msg.message.edit_reply_markup(keyb)
        else:
            async with state.proxy() as data:
                data['location_to_serve'].append(msg.data.split('_')[1])
            await msg.message.edit_reply_markup(keyb)


"""End Tumanlar"""

"""Start custom clinic"""


@dp.callback_query_handler(text='clinicediting_')
async def custom_func13(call: types.CallbackQuery):
    await call.message.delete()
    clinic_obj = clinic.objects.filter(owner__user__chat_id=call.from_user.id)
    await call.message.answer('Пожалуйста выберите тип услуги:', reply_markup=clinic_editing(clinic_obj))


@dp.callback_query_handler(text='cliniceditingaru_')
async def custom_func15(call: types.CallbackQuery):
    await add_clinic(call)


@dp.callback_query_handler(lambda a: 'cliniceditingdeleru_' in a.data)
async def custom_func16(call: types.CallbackQuery):
    _, clinic_id = call.data.split('_')
    clinic_obj = clinic.objects.get(id=clinic_id)
    if clinic_obj.photo:
        os.remove(f'media/{clinic_obj.photo}')
    clinic_obj.delete()
    await call.message.delete()
    await call.answer('Ваша клиника успешно удалена', show_alert=True)
    await call.message.answer('Ваша клиника успешно удалена')
    await bot_start(call.message)


@dp.callback_query_handler(lambda a: 'cliniceditingeru_' in a.data)
async def custom_func17(call: types.CallbackQuery):
    _, clinic_id = call.data.split('_')
    clinic_obj = clinic.objects.get(id=int(clinic_id)).id
    await call.message.delete()
    await call.message.answer('Чего вы хотите изменить:', reply_markup=clinic_editing_menu_into(clinic_obj))


@dp.callback_query_handler(lambda a: 'cliniceditingnameru_' in a.data)
async def custom_func18(call: types.CallbackQuery, state=FSMContext):
    _, clinic_id = call.data.split('_')
    await call.message.delete()
    await state.update_data(clinic_id=clinic_id)
    await call.message.answer('Введите название клиники:', reply_markup=back_first)
    await clinic_update_.updating.set()


@dp.message_handler(state=clinic_update_.updating)
async def custom_func19(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        clinic_id = data['clinic_id']
        clinic_obj = clinic.objects.filter(id=data['clinic_id']).first()
    clinic_obj.name = message.text
    clinic_obj.save()
    await message.answer('Название клиники успешно изменено',
                         reply_markup=clinic_editing_menu_into(clinic_id))
    await state.finish()


@dp.callback_query_handler(lambda a: 'cliniceditingcitru_' in a.data)
async def custom_func20(call: types.CallbackQuery, state=FSMContext):
    _, clinic_id = call.data.split('_')
    await call.message.delete()
    await state.update_data(clinic_id=clinic_id)
    await clinic_updatecity_.updating.set()
    await clinic_updatecity_.updating.set()
    await call.message.answer('Укажите город клиники:', reply_markup=City_keyb('updatecitr'))


@dp.callback_query_handler(state=clinic_updatecity_.updating)
async def custom_func21(call: types.CallbackQuery, state=FSMContext):
    async with state.proxy() as data:
        clinic_id = data['clinic_id']
        clinic_obj = clinic.objects.filter(id=data['clinic_id']).first()
    clinic_obj.region = City.objects.get(id=int(call.data.split('_')[1]))
    clinic_obj.save()
    await call.message.delete()
    await call.message.answer('Успешно изменен регион клиники.',
                              reply_markup=clinic_editing_menu_into(clinic_id))
    await state.finish()


@dp.callback_query_handler(lambda a: 'cliniceditinglocatioru_' in a.data)
async def custom_func22(call: types.CallbackQuery, state=FSMContext):
    _, clinic_id = call.data.split('_')
    await call.message.delete()
    await state.update_data(clinic_id=clinic_id)
    await clinic_updatelocation_.updating.set()
    await call.message.answer('Отправьте локацию клиники:', reply_markup=Loc_send)


@dp.message_handler(state=clinic_updatelocation_.updating, content_types=types.ContentTypes.LOCATION)
async def custom_func23(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        clinic_id = data['clinic_id']
        clinic_obj = clinic.objects.filter(id=data['clinic_id']).first()
    clinic_obj.latitude = message.location.latitude
    clinic_obj.longitude = message.location.longitude
    clinic_obj.save()
    await message.answer('Локация клиники успешно изменён',
                         reply_markup=clinic_editing_menu_into(clinic_id))
    await state.finish()


@dp.callback_query_handler(lambda a: 'cliniceditingphotru_' in a.data)
async def custom_func24(call: types.CallbackQuery, state=FSMContext):
    _, clinic_id = call.data.split('_')
    await call.message.delete()
    await state.update_data(clinic_id=clinic_id)
    await clinic_updatephoto_.updating.set()
    await call.message.answer('Отправьте фото клиники', reply_markup=back_first)


@dp.message_handler(state=clinic_updatephoto_.updating, content_types=types.ContentTypes.PHOTO)
async def custom_func25(message: types.Message, state=FSMContext):
    photo = message.photo[-1]
    date = datetime.datetime.now()
    file_path = f"clinic/{date.year}/{date.month}/{date.day}/{photo.file_id}.jpg"
    await photo.download(destination_file=os.path.join(Loc_file_media, file_path))
    async with state.proxy() as data:
        clinic_id = data['clinic_id']
        clinic_obj = clinic.objects.filter(id=data['clinic_id']).first()
    if clinic_obj.photo:
        os.remove(f'media/{clinic_obj.photo}')
    clinic_obj.photo = file_path
    clinic_obj.save()
    await message.answer('Фото клиники успешно изменён.',
                         reply_markup=clinic_editing_menu_into(clinic_id))
    await state.finish()


@dp.callback_query_handler(lambda a: 'cliniceditingdesru_' in a.data)
async def custom_func26(call: types.CallbackQuery, state=FSMContext):
    _, clinic_id = call.data.split('_')
    await call.message.delete()
    await state.update_data(clinic_id=clinic_id)
    await clinic_updatedecs_.updating.set()
    await call.message.answer('Введите описание вашей клиники:', reply_markup=back_first)


@dp.message_handler(state=clinic_updatedecs_.updating)
async def custom_func27(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        clinic_id = data['clinic_id']
        clinic_obj = clinic.objects.filter(id=data['clinic_id']).first()
    clinic_obj.description = message.text
    clinic_obj.save()
    await message.answer('Описание вашей клиники упешно изменён.',
                         reply_markup=clinic_editing_menu_into(clinic_id))
    await state.finish()


"""End custom clinic"""
