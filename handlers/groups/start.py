from loader import dp, bot
from aiogram import types
from filters.group_filter import IsGroup


@dp.message_handler(IsGroup(), commands=['id_group'])
async def id_group(msg: types.Message):
    await msg.answer(msg.chat.id)


@dp.message_handler(IsGroup(), content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def new_member(msg: types.Message):
    await msg.answer(f'Привет {msg.from_user.full_name}! Добро пожаловать в чат!')
    db_group = Group_info.objects.get(group_id=int(msg.chat.id))
    if str(msg.from_user.id) not in str(db_group.users_id):
        if db_group.users_id is not None:
            db_group.users_id= f"{db_group.users_id} {msg.from_user.id}"
        else:
            db_group.users_id = msg.from_user.id
    db_group.save()
    if (db_group.pacient_userid in db_group.users_id) and (db_group.doctor_user_id in db_group.users_id):
        await msg.answer(db_group.description)


@dp.message_handler(IsGroup(), commands=['endourchat'])
async def exo(msg: types.Message):
    db_group = Group_info.objects.get(group_id=msg.chat.id)
    for users in db_group.users_id.split():
        await bot.kick_chat_member(msg.chat.id, user_id=int(users))
    db_group.status_working = False
    db_group.doctor_user_id = None
    db_group.pacient_userid = None
    db_group.users_id = None
    db_group.save()