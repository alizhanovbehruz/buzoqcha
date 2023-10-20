import datetime
import os

from app import Loc_file_media
from filters import IsPrivate
from handlers.users.handler_dec import vetdoktor,  phone_re, add_clinic
from handlers.users.start import bot_start
from keyboards.inline.deals import doctor_editing_menu, reg_again, doctor_editing_menu_into, City_keyb, \
    Region_keyb, type_cl, Region_keyb_update, clinic_editing, clinic_editing_menu_into
from loader import dp, bot
from aiogram import types
from keyboards.default.menuStart import back, back_first, number_first, Loc_send
from aiogram.dispatcher import FSMContext
from infos.models import Users, Doctor, clinic, City
from states.statesper import doctor_info, doctor_update, doctor_updatephone, doctor_updatephoto, doctor_updatedecs, \
    doctor_updatelocation, clinic_update, clinic_updatecity, clinic_updatephoto, clinic_updatelocation, \
    clinic_updatedecs
import re


@dp.message_handler(IsPrivate(), text=['/start', '⬅Bosh menyuga qaytish'], state="*")
async def botprevius(msg: types.Message, state=FSMContext):
    await bot_start(msg)
    await state.finish()


@dp.message_handler(text='Mening akkauntim')
async def custom_func1(message: types.Message):
    doctor_obj = Doctor.objects.filter(user__chat_id=message.from_user.id)
    if doctor_obj:
        doctor_obj = doctor_obj.first()
        s = ''
        for i in doctor_obj.work_region.all():
            s += f"{i.city} Viloyati, {i.name} \n"
        await message.answer('Siz veterinariya doktor siz:\n'
                             f"Ismingiz: {doctor_obj.full_name}\n"
                             f"Telefon raqamingiz: {doctor_obj.phone}\n"
                             f"Xizmat krusata oladigan manzillaringiz:\n"
                             f"{s}\n\n")
        if doctor_obj.photo:
            await bot.send_photo(message.chat.id, photo=open(f'media/{doctor_obj.photo}', 'rb'),
                                 caption='Sizning rasmingiz')
        else:
            await message.answer('Rasm yuklanmagan')

        if doctor_obj.clinic_bool:
            await message.answer('Sizning klinikangiz:')
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
                                                     types.InlineKeyboardButton(text='Google Xaritalarda ochish',
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
                                                     types.InlineKeyboardButton(text='Google Xaritalarda ochish',
                                                                                url=f'https://www.google.com/maps/search/?api=1&query={i.latitude},{i.longitude}')
                                                 ]
                                             ]
                                         ))
        else:
            await message.answer('Sizning klinikangiz yo\'q')

        await message.answer('Xizmatni tanlang:', reply_markup=doctor_editing_menu)
    else:
        await message.answer('Ajoyib', reply_markup=types.ReplyKeyboardRemove())
        await message.answer('Sizga admin xali ruxsat bermagan yoki siz registratsiyadan otyotkanda xatolik bo\'lgan',
                             reply_markup=reg_again)


@dp.callback_query_handler(text='doctorediting_')
async def custom_func2(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Xizmatni tanlang:', reply_markup=doctor_editing_menu_into)


@dp.callback_query_handler(text='doctoreditingfio_')
async def custom_func3(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Ismingizni kiriting:', reply_markup=back_first)
    await doctor_update.updating.set()


@dp.message_handler(state=doctor_update.updating)
async def custom_func4(message: types.Message, state=FSMContext):
    Doctor.objects.filter(user__chat_id=message.from_user.id).update(full_name=message.text)
    await message.answer('Ismingiz muvaffaqiyatli o\'zgartirildi', reply_markup=doctor_editing_menu_into)
    await state.finish()


@dp.callback_query_handler(text='doctoreditingphone_')
async def custom_func5(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Telefon raqamingizni kiriting:', reply_markup=number_first)
    await doctor_updatephone.updating.set()


@dp.message_handler(state=doctor_updatephone.updating)
async def custom_func6(message: types.Message, state=FSMContext):
    if not re.match(phone_re, message.text):
        await message.answer('Telefon raqamingizni noto\'g\'ri kiritdingiz!!!, To\'gri kiriting::')
        return
    Doctor.objects.filter(user__chat_id=message.from_user.id).update(phone=message.text)
    await message.answer('Telefon raqamingiz muvaffaqiyatli o\'zgartirildi', reply_markup=doctor_editing_menu_into)
    await state.finish()


@dp.message_handler(state=doctor_updatephone.updating, content_types=types.ContentTypes.CONTACT)
async def custom_func7(message: types.Message, state=FSMContext):
    Doctor.objects.filter(user__chat_id=message.from_user.id).update(phone=message.contact.phone_number)
    await message.answer('Telefon raqamingiz muvaffaqiyatli o\'zgartirildi', reply_markup=doctor_editing_menu_into)
    await state.finish()


@dp.callback_query_handler(text='doctoreditingphoto_')
async def custom_func8(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Rasm yuboring:', reply_markup=back_first)
    await doctor_updatephoto.updating.set()


@dp.message_handler(state=doctor_updatephoto.updating, content_types=types.ContentTypes.PHOTO)
async def custom_func9(message: types.Message, state=FSMContext):
    photo = message.photo[-1]
    date = datetime.datetime.now()
    file_path = f"doctors/{date.year}/{date.month}/{date.day}/{photo.file_id}.jpg"
    await photo.download(destination_file=os.path.join(Loc_file_media, file_path))
    Doctor.objects.filter(user__chat_id=message.from_user.id).update(photo=file_path)
    await message.answer('Rasm muvaffaqiyatli o\'zgartirildi', reply_markup=doctor_editing_menu_into)
    await state.finish()


@dp.callback_query_handler(text='doctoreditingdesc_')
async def custom_func10(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Ma\'lumotni kiriting:', reply_markup=back_first)
    await doctor_updatedecs.updating.set()


@dp.message_handler(state=doctor_updatedecs.updating)
async def custom_func11(message: types.Message, state=FSMContext):
    Doctor.objects.filter(user__chat_id=message.from_user.id).update(description=message.text)
    await message.answer('Ma\'lumot muvaffaqiyatli o\'zgartirildi', reply_markup=doctor_editing_menu_into)
    await state.finish()


@dp.callback_query_handler(text='doctoreditinglocation_')
async def custom_func12(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Manzilni kiriting:', reply_markup=City_keyb('citydok'))
    await doctor_updatelocation.updating.set()


"""Tumanlar"""


@dp.callback_query_handler(lambda a: 'citydok_' in a.data, state=doctor_updatelocation.updating)
async def location_to_serve(msg: types.CallbackQuery, state=FSMContext):
    _, city_id = msg.data.split('_')
    locat_obj = list(
        Doctor.objects.filter(user__chat_id=msg.from_user.id).first().work_region.all().values_list('id', flat=True))
    async with state.proxy() as data:
        data['location_to_serve'] = locat_obj
    print(locat_obj)
    await msg.message.delete()
    await msg.message.answer("Xizmat ko'rsatadigan tumanlarni tanlang",
                             reply_markup=await Region_keyb_update(city_id, data['location_to_serve']))


@dp.callback_query_handler(lambda a: 'regiondok_' in a.data, state=doctor_updatelocation.updating)
async def deals_func3(msg: types.CallbackQuery, state=FSMContext):
    if msg.data == 'regiondok_save':
        await msg.message.delete()
        async with state.proxy() as data:
            print(data['location_to_serve'])
            Doctor.objects.filter(user__chat_id=msg.from_user.id).first().work_region.set(data['location_to_serve'])
        await msg.message.answer('Xizmat ko\'rsatadigan tumanlar muvaffaqiyatli o\'zgartirildi',
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
    await call.message.answer('Xizmatni tanlang:', reply_markup=clinic_editing(clinic_obj))


@dp.callback_query_handler(text='cliniceditingadd_')
async def custom_func15(call: types.CallbackQuery):
    await add_clinic(call)


@dp.callback_query_handler(lambda a: 'cliniceditingdelete_' in a.data)
async def custom_func16(call: types.CallbackQuery):
    _, clinic_id = call.data.split('_')
    clinic_obj = clinic.objects.get(id=clinic_id)
    if clinic_obj.photo:
        os.remove(f'media/{clinic_obj.photo}')
    clinic_obj.delete()
    await call.message.delete()
    await call.answer('Klinikangiz muvaffaqiyatli o\'chirildi', show_alert=True)
    await call.message.answer('Klinikangiz muvaffaqiyatli o\'chirildi')
    await bot_start(call.message)


@dp.callback_query_handler(lambda a: 'cliniceditingedit_' in a.data)
async def custom_func17(call: types.CallbackQuery):
    _, clinic_id = call.data.split('_')
    clinic_obj = clinic.objects.get(id=int(clinic_id)).id
    await call.message.delete()
    await call.message.answer('Xizmatni tanlang:', reply_markup=clinic_editing_menu_into(clinic_obj))


@dp.callback_query_handler(lambda a: 'cliniceditingname_' in a.data)
async def custom_func18(call: types.CallbackQuery, state=FSMContext):
    _, clinic_id = call.data.split('_')
    await call.message.delete()
    await state.update_data(clinic_id=clinic_id)
    await call.message.answer('Klinikaning nomini kiriting:', reply_markup=back_first)
    await clinic_update.updating.set()


@dp.message_handler(state=clinic_update.updating)
async def custom_func19(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        clinic_id = data['clinic_id']
        clinic_obj = clinic.objects.filter(id=data['clinic_id']).first()
    clinic_obj.name = message.text
    clinic_obj.save()
    await message.answer('Klinikaning nomi muvaffaqiyatli o\'zgartirildi',
                         reply_markup=clinic_editing_menu_into(clinic_id))
    await state.finish()


@dp.callback_query_handler(lambda a: 'cliniceditingcity_' in a.data)
async def custom_func20(call: types.CallbackQuery, state=FSMContext):
    _, clinic_id = call.data.split('_')
    await call.message.delete()
    await state.update_data(clinic_id=clinic_id)
    await call.message.answer('Klinikaning shaharini kiriting:', reply_markup=City_keyb('updatecity'))
    await clinic_updatecity.updating.set()


@dp.callback_query_handler(state=clinic_updatecity.updating)
async def custom_func21(call: types.CallbackQuery, state=FSMContext):
    async with state.proxy() as data:
        clinic_id = data['clinic_id']
        clinic_obj = clinic.objects.filter(id=data['clinic_id']).first()
    clinic_obj.region = City.objects.get(id=int(call.data.split('_')[1]))
    clinic_obj.save()
    await call.message.delete()
    await call.message.answer('Klinikaning viloyati muvaffaqiyatli o\'zgartirildi',
                              reply_markup=clinic_editing_menu_into(clinic_id))
    await state.finish()


@dp.callback_query_handler(lambda a: 'cliniceditinglocation_' in a.data)
async def custom_func22(call: types.CallbackQuery, state=FSMContext):
    _, clinic_id = call.data.split('_')
    await call.message.delete()
    await state.update_data(clinic_id=clinic_id)
    await call.message.answer('Klinikaning manzilini kiriting:', reply_markup=Loc_send)
    await clinic_updatelocation.updating.set()


@dp.message_handler(state=clinic_updatelocation.updating, content_types=types.ContentTypes.LOCATION)
async def custom_func23(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        clinic_id = data['clinic_id']
        clinic_obj = clinic.objects.filter(id=data['clinic_id']).first()
    clinic_obj.latitude = message.location.latitude
    clinic_obj.longitude = message.location.longitude
    clinic_obj.save()
    await message.answer('Klinikaning manzili muvaffaqiyatli o\'zgartirildi',
                         reply_markup=clinic_editing_menu_into(clinic_id))
    await state.finish()


@dp.callback_query_handler(lambda a: 'cliniceditingphoto_' in a.data)
async def custom_func24(call: types.CallbackQuery, state=FSMContext):
    _, clinic_id = call.data.split('_')
    await call.message.delete()
    await state.update_data(clinic_id=clinic_id)
    await call.message.answer('Klinikaning rasmini yuboring:', reply_markup=back_first)
    await clinic_updatephoto.updating.set()


@dp.message_handler(state=clinic_updatephoto.updating, content_types=types.ContentTypes.PHOTO)
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
    await message.answer('Klinikaning rasmi muvaffaqiyatli o\'zgartirildi',
                         reply_markup=clinic_editing_menu_into(clinic_id))
    await state.finish()


@dp.callback_query_handler(lambda a: 'cliniceditingdesc_' in a.data)
async def custom_func26(call: types.CallbackQuery, state=FSMContext):
    _, clinic_id = call.data.split('_')
    await call.message.delete()
    await state.update_data(clinic_id=clinic_id)
    await call.message.answer('Klinikaning ma\'lumotini kiriting:', reply_markup=back_first)
    await clinic_updatedecs.updating.set()


@dp.message_handler(state=clinic_updatedecs.updating)
async def custom_func27(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        clinic_id = data['clinic_id']
        clinic_obj = clinic.objects.filter(id=data['clinic_id']).first()
    clinic_obj.description = message.text
    clinic_obj.save()
    await message.answer('Klinikaning ma\'lumoti muvaffaqiyatli o\'zgartirildi',
                         reply_markup=clinic_editing_menu_into(clinic_id))
    await state.finish()


"""End custom clinic"""
