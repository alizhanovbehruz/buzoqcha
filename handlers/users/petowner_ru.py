from handlers.users.start import  lang_
from loader import dp, bot
from aiogram import types
from keyboards.default.menuStart_ru import petowner_keyboard, back_first, petowner_keyboard
from keyboards.inline.deal_ru import City_keyb, type_vet_clinic, \
    Region_keyb_petowner
from infos.models import Doctor, Users, Region, clinic
from states.statesper_ru import petowner_clinic_


@dp.callback_query_handler(text='Petowner_')
async def petowner_func1(msg: types.CallbackQuery):
    Users.objects.filter(chat_id=msg.from_user.id).update(type_person='OE')
    await msg.message.delete()
    await msg.message.answer('Пожалуйста, выберите услугу:', reply_markup=petowner_keyboard)


@dp.message_handler(text='🐶Найти ветеринара')
async def petowner_func2(msg: types.Message):
    await msg.answer('Отлино', reply_markup=back_first)
    await msg.delete()
    await msg.answer('Пожалуйста, введите город', reply_markup=City_keyb('citclinvru'))


@dp.callback_query_handler(lambda a: 'citclinvru_' in a.data)
async def petowner_func3(msg: types.CallbackQuery):
    await msg.message.delete()
    await msg.message.answer('Пожалуйста, выберите свой район:',
                             reply_markup=await Region_keyb_petowner(msg.data.split('_')[1]))


@dp.callback_query_handler(lambda a: 'reginpetru_' in a.data)
async def petowner_func4(msg: types.CallbackQuery):
    _, region = msg.data.split('_')
    await msg.message.delete()
    doctors_obj = Doctor.accessed_doc.filter(work_region__in=[region])
    if doctors_obj:
        for obj in doctors_obj:
            if not obj.username:
                s = f'<b>Ветеринар:</b> {obj.username}\n'
            else:
                s = ''
            if obj.photo:
                await bot.send_photo(chat_id=msg.from_user.id, photo=obj.photo, caption=f"<b>Ветеринар</b>\n"
                                                                                        f"<b>ФИО:</b> {obj.full_name}\n\n"
                                                                                        f"{obj.description_ru}\n\n"
                                                                                        f"<b>Номер телефона:</b> {obj.phone}\n{s}",
                                     parse_mode='html')
            else:
                await msg.message.answer(f"<b>Ветеринар</b>\n"
                                         f"<b>ФИО:</b> {obj.full_name}\n\n"
                                         f"{obj.description_ru}\n\n"
                                         f"<b>Номер телефона:</b> {obj.phone}\n{s}", parse_mode='html')
    else:
        await msg.message.answer('К сожалению, в вашем районе нет ветеринаров!')
        await lang_(msg.message)


@dp.message_handler(text='🏥Найти клинику или ветаптеку')
async def petowner_func5(msg: types.Message):
    await msg.answer('Отлмчно', reply_markup=back_first)
    await msg.delete()
    await petowner_clinic_.type_clin.set()
    await msg.answer('Что Вы ищете??', reply_markup=type_vet_clinic)


@dp.callback_query_handler(lambda a: 'typvetklinru_' in a.data, state=petowner_clinic_.type_clin)
async def petowner_func6(msg: types.CallbackQuery, state=petowner_clinic_.type_clin):
    await msg.message.delete()
    async with state.proxy() as data:
        data['type_clinic'] = msg.data.split('_')[1]
    await petowner_clinic_.next()
    await msg.message.answer('Пожалуйста, выберите ваш регион:', reply_markup=City_keyb('citcliru'))


@dp.callback_query_handler(lambda a: 'citcliru_' in a.data, state=petowner_clinic_.city)
async def petowner_func7(msg: types.CallbackQuery, state=petowner_clinic_.city):
    await msg.message.delete()
    async with state.proxy() as data:
        data['city'] = msg.data.split('_')[1]
    await petowner_clinic_.next()
    clinic_or_apteka_obj = clinic.objects.filter(region__id=int(data['city']), type_clinic=data['type_clinic'])
    if clinic_or_apteka_obj:
        for obj in clinic_or_apteka_obj:
            if obj.photo:
                await msg.message.answer_photo(photo=obj.photo, caption=f"<b>{obj.type_clinic.name}:</b> {obj.name}\n\n"
                                                                        f"<b>Адрес:</b> {obj.region}\n\n"
                                                                        f"{obj.description_ru}\n\n"
                                                                        f"<b>Номер телефона:</b> {obj.phone}",
                                               reply_markup=types.InlineKeyboardMarkup(
                                                   inline_keyboard=[
                                                       [
                                                           types.InlineKeyboardButton(text='Открыть в Google Картах',
                                                                                      url=f'https://www.google.com/maps/search/?api=1&query={obj.latitude},{obj.longitude}')
                                                       ]
                                                   ]
                                               ), parse_mode='html')
            else:
                await msg.message.answer(f"<b>{obj.type_clinic.name}:</b> {obj.name}\n\n"
                                         f"<b>Адрес:</b> {obj.region}\n\n"
                                         f"{obj.description_ru}\n\n"
                                         f"<b>Номер телефона:</b> {obj.phone}",
                                         reply_markup=types.InlineKeyboardMarkup(
                                             inline_keyboard=[
                                                 [
                                                     types.InlineKeyboardButton(text='Открыть в Google Картах',
                                                                                url=f'https://www.google.com/maps/search/?api=1&query={obj.latitude},{obj.longitude}')
                                                 ]
                                             ]
                                         ), parse_mode='html')
    else:
        await msg.message.answer(f"К сожалению, пока недоступно в вашем регионе!")
    await state.finish()
    await lang_(msg.message)
