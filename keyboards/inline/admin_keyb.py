from aiogram.types import InlineKeyboardButton ,InlineKeyboardMarkup

start_admin = InlineKeyboardMarkup(
    inline_keyboard=[
           [
            InlineKeyboardButton(text='Управление админом',callback_data='startsett_admin'),
            InlineKeyboardButton(text='Управление группой',callback_data='startsett_group')
        ],
        [
            InlineKeyboardButton(text='Рассылка по пользователям',callback_data='startset_post'),
            InlineKeyboardButton(text='Статистика',callback_data='startsett_statistic')
        ]
    ]
)

admin_set = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Удалить', callback_data='admins_rem'),
            InlineKeyboardButton(text='Добавить', callback_data='admins_add')
        ]
    ]
)

group_set = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Обновить', callback_data='groups_update')
        ]
    ]
)