from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from infos.models import City, Region

reg_again = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Зарегистрироваться снова", callback_data='Vetdoktor_')
        ],
        [
            InlineKeyboardButton(text='Связаться с администратором', url='https://t.me/alizhanovbekhruz')
        ]
    ]
)

add_clinic_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Добавить Клинику/ВетАптеку/Лабораторию', callback_data='addclinc_')
        ]
    ]
)


def let_keyb(id):
    keyb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Ijozat berish', callback_data=f'letTre||{id}')
            ]
        ]
    )
    return keyb


def City_keyb(call_data):
    keyb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=i.name, callback_data=f'{call_data}_{i.id}')
            ] for i in City.objects.all()
        ]
    )
    return keyb


truefalse_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да', callback_data='trueflse_true'),
            InlineKeyboardButton(text='Нет', callback_data='trueflse_false')
        ]
    ]
)


async def Region_keyb_petowner(id):
    keyb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=i.name, callback_data=f'reginpetru_{i.id}')
            ] for i in Region.objects.filter(city__id=id)
        ]
    )
    return keyb


async def Region_keyb(id, list_access):
    print(list_access)
    if map(lambda a: a.startswith(id), list_access) or True:
        keyb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='✅' + i.name, callback_data=f'regiondru_{i.id}')
                ] if (str(i.id) in list_access) else [
                    InlineKeyboardButton(text=i.name, callback_data=f'regiondru_{i.id}')
                ] for i in Region.objects.filter(city__id=id)
            ]
        )
    else:
        keyb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=i.name, callback_data=f'regiondru_{i.id}')
                ] for i in Region.objects.filter(city__id=id)
            ]
        )
    keyb.inline_keyboard.append([InlineKeyboardButton(text="⬅Назад", callback_data="regiondru_back"),
                                 InlineKeyboardButton(text='💾Сохранить💾', callback_data=f'regiondru_save')])
    return keyb


async def Region_keyb_update(id, list_access):
    print(list_access)
    if map(lambda a: a.startswith(id), list_access) or True:
        keyb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='✅' + i.name, callback_data=f'regiondru_{i.id}')
                ] if (i.id in list_access) else [
                    InlineKeyboardButton(text=i.name, callback_data=f'regiondru_{i.id}')
                ] for i in Region.objects.filter(city__id=id)
            ]
        )
    else:
        keyb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=i.name, callback_data=f'regiondru_{i.id}')
                ] for i in Region.objects.filter(city__id=id)
            ]
        )
    keyb.inline_keyboard.append([InlineKeyboardButton(text='💾Сохранить💾', callback_data=f'regiondru_save')])
    return keyb


async def type_cl(data, reply_keyb):
    list_inlin = reply_keyb['inline_keyboard']
    remove_list = False
    for keyb in range(len(list_inlin)):
        if list_inlin[keyb][0]['callback_data'] == data:
            if list_inlin[keyb][0]['text'].startswith('✅'):
                remove_list = list_inlin[keyb][0]['callback_data'].split('_')[1]
                list_inlin[keyb][0]['text'] = list_inlin[keyb][0]['text'][1:]
            else:
                list_inlin[keyb][0]['text'] = '✅' + list_inlin[keyb][0]['text']
            break
    return (InlineKeyboardMarkup(inline_keyboard=list_inlin), remove_list)


typework_ = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Ветеринар', callback_data='Vetdoktor_')
        ],
        [
            InlineKeyboardButton(text='Владелец животного', callback_data='Petowner_')
        ],
    ],
)

doctor_editing_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='📝Изменить мои данные', callback_data='doctoreditinru_')
        ],
        [
            InlineKeyboardButton(text='📝Изменить данные клиники или Вет аптеки', callback_da0ta='cliniceditinru_')
        ]
    ]
)


def clinic_editing(obj):
    if obj:
        inline_keyboard = [
            [
                InlineKeyboardButton(text=i.name, callback_data=f'anythingddddd'),
                InlineKeyboardButton(text='❌Удалить', callback_data=f'cliniceditingdeleru_{i.id}'),
                InlineKeyboardButton(text='🔄Изменить', callback_data=f'cliniceditingeru_{i.id}'),
            ] for i in obj
        ]
    else:
        inline_keyboard = [
            [
                InlineKeyboardButton(text='Sizda Klinika yoq', callback_data='anythingddddd'),
            ]
        ]
    inline_keyboard.append([InlineKeyboardButton(text='🆕Qo\'shish', callback_data='cliniceditingaru_')])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


doctor_editing_menu_into = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='📝ФИО', callback_data='doctoreditingfru_')
        ],
        [
            InlineKeyboardButton(text='📝Номер телефона', callback_data='doctoreditingphoru_')
        ],
        [
            InlineKeyboardButton(text='📝Фотографию', callback_data='doctoreditingphoru_')
        ],
        [
            InlineKeyboardButton(text='📝Описание', callback_data='doctoreditingderu_')
        ],
        [
            InlineKeyboardButton(text='📝Изменить адреса сервиса:', callback_data='doctoreditinglocatiru_')
        ],
    ]
)

type_vet_clinic = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='💊Вет Аптека', callback_data='typvetklinru_VT')
        ],
        [
            InlineKeyboardButton(text='🏥Клиника', callback_data='typvetklinru_KL')
        ],
        [
            InlineKeyboardButton(text='🏥Лаборатория', callback_data='typvetklinru_LB')
        ],
    ]
)


def clinic_editing_menu_into(id_clin):
    keyb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='📝Название ', callback_data=f'cliniceditingnamru_{id_clin}')
            ],
            [
                InlineKeyboardButton(text='📝Область', callback_data=f'cliniceditingcitru_{id_clin}')
            ],
            [
                InlineKeyboardButton(text='📝Адрес', callback_data=f'cliniceditinglocatioru_{id_clin}')
            ],
            [
                InlineKeyboardButton(text='📝Фото', callback_data=f'cliniceditingphotru_{id_clin}')
            ],
            [
                InlineKeyboardButton(text='📝Описание', callback_data=f'cliniceditingdesru_{id_clin}')
            ],
        ]
    )
    return keyb
