from handlers.users.start import bot_start
from loader import dp, bot
from aiogram import types
from keyboards.default.menuStart import petowner_keyboard, back_first
from keyboards.inline.deals import City_keyb, Region_keyb_petowner, type_vet_clinic
from infos.models import Doctor, Users, Region, clinic
from states.statesper import petowner_clinic


@dp.callback_query_handler(text='Petowner')
async def petowner_func1(msg: types.CallbackQuery):
    Users.objects.filter(chat_id=msg.from_user.id).update(type_person='OE')
    await msg.message.delete()
    await msg.message.answer('Marxamat xizmatni tanlang:', reply_markup=petowner_keyboard)


@dp.message_handler(text='🐶Veterinar topish')
async def petowner_func2(msg: types.Message):
    await msg.answer('Ajoyib:', reply_markup=back_first)
    await msg.delete()
    await msg.answer('Marxamat viloyatingizni tanlang:', reply_markup=City_keyb('citclinvet'))


@dp.callback_query_handler(lambda a: 'citclinvet_' in a.data)
async def petowner_func3(msg: types.CallbackQuery):
    await msg.message.delete()
    await msg.message.answer('Marxamat shahringizni tanlang:',
                             reply_markup=await Region_keyb_petowner(msg.data.split('_')[1]))


@dp.callback_query_handler(lambda a: 'reginpetow_' in a.data)
async def petowner_func4(msg: types.CallbackQuery):
    _, region = msg.data.split('_')
    await msg.message.delete()
    doctors_obj = Doctor.accessed_doc.filter(work_region__in=[region])
    if doctors_obj:
        for obj in doctors_obj:
            if not obj.username:
                s = f'<b>Veterinar:</b> {obj.username}\n'
            else:
                s = ''
            if obj.photo:
                await bot.send_photo(chat_id=msg.from_user.id, photo=open(f'media/{obj.photo}', 'rb'),
                                     caption=f"<b>Veterinar</b>\n"
                                             f"<b>Ismi:</b> {obj.full_name}\n\n"
                                             f"{obj.description}\n\n"
                                             f"<b>Telefon raqami:</b> {obj.phone}\n{s}",
                                     parse_mode='html')
            else:
                await msg.message.answer(f"<b>Veterinar</b>\n"
                                         f"<b>Ismi:</b> {obj.full_name}\n\n"
                                         f"{obj.description}\n\n"
                                         f"<b>Telefon raqami:</b> {obj.phone}\n{s}", parse_mode='html')
    else:
        await msg.message.answer('Kechirasiz, sizning hududingizda veterinarlar mavjud emas!')


@dp.message_handler(text='🏥Klinika yoki VetApteka topish')
async def petowner_func5(msg: types.Message):
    await msg.answer('Ajoyib:', reply_markup=back_first)
    await msg.delete()
    await petowner_clinic.type_clin.set()
    await msg.answer('Siz nima qidiryapsiz?', reply_markup=type_vet_clinic)


@dp.callback_query_handler(lambda a: 'typvetklinik_' in a.data, state=petowner_clinic.type_clin)
async def petowner_func6(msg: types.CallbackQuery, state=petowner_clinic.type_clin):
    await msg.message.delete()
    async with state.proxy() as data:
        data['type_clinic'] = msg.data.split('_')[1]
    await petowner_clinic.next()
    await msg.message.answer('Marxamat viloyatingizni tanlang:', reply_markup=City_keyb('citclinvet'))


@dp.callback_query_handler(lambda a: 'citclinvet_' in a.data, state=petowner_clinic.city)
async def petowner_func7(msg: types.CallbackQuery, state=petowner_clinic.city):
    await msg.message.delete()
    async with state.proxy() as data:
        data['city'] = msg.data.split('_')[1]
    await petowner_clinic.next()
    clinic_or_apteka_obj = clinic.objects.filter(region__id=int(data['city']), type_clinic=data['type_clinic'])
    if clinic_or_apteka_obj:
        for obj in clinic_or_apteka_obj:
            if obj.photo:
                await msg.message.answer_photo(photo=obj.photo, caption=f"<b>{obj.type_clinic}:</b> {obj.name}\n\n"
                                                                        f"<b>Manzili:</b> {obj.region}\n\n"
                                                                        f"{obj.description}\n\n",
                                               reply_markup=types.InlineKeyboardMarkup(
                                                   inline_keyboard=[
                                                       [
                                                           types.InlineKeyboardButton(text='Google Xaritalarda ochish',
                                                                                      url=f'https://www.google.com/maps/search/?api=1&query={obj.latitude},{obj.longitude}')
                                                       ]
                                                   ]
                                               ), parse_mode='html')
            else:
                await msg.message.answer(f"<b>{obj.type_clinic}:</b> {obj.name}\n\n"
                                         f"<b>Manzili:</b> {obj.region}\n\n"
                                         f"{obj.description}\n\n",
                                         parse_mode='html', reply_markup=types.InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                types.InlineKeyboardButton(text='Google Xaritalarda ochish',
                                                           url=f'https://www.google.com/maps/search/?api=1&query={obj.latitude},{obj.longitude}')
                            ]
                        ]
                    ))
    else:
        await msg.message.answer(f"Kechirasiz, sizning hududingizda hali mavjud emas!")
    await state.finish()
    await bot_start(msg.message)
