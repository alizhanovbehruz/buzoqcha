from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from infos.models import City, Region

reg_again = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Qayta ro'yxatdan otish", callback_data='Vetdoktor')
        ],
        [
            InlineKeyboardButton(text='Adminga murojat qilish', url='https://t.me/alizhanovbekhruz')
        ]
    ]
)

add_clinic_keyb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Klinikani yoki Vet Aptekani yoki Laboratoriyani qo`shish', callback_data='addclinic')
        ]
    ]
)


def let_keyb(id):
    keyb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Ijozat berish', callback_data=f'letTrue||{id}')
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
            InlineKeyboardButton(text='Bor', callback_data='truefalse_true'),
            InlineKeyboardButton(text='Yoq', callback_data='truefalse_false')
        ]
    ]
)


async def Region_keyb_petowner(id):
    keyb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=i.name, callback_data=f'reginpetow_{i.id}')
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
                    InlineKeyboardButton(text='✅' + i.name, callback_data=f'regiondok_{i.id}')
                ] if (str(i.id) in list_access) else [
                    InlineKeyboardButton(text=i.name, callback_data=f'regiondok_{i.id}')
                ] for i in Region.objects.filter(city__id=id)
            ]
        )
    else:
        keyb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=i.name, callback_data=f'regiondok_{i.id}')
                ] for i in Region.objects.filter(city__id=id)
            ]
        )
    keyb.inline_keyboard.append([InlineKeyboardButton(text="⬅Orqaga", callback_data="regiondok_back"),
                                 InlineKeyboardButton(text='💾Saqlash💾', callback_data=f'regiondok_save')])
    return keyb


async def Region_keyb_update(id, list_access):
    print(list_access)
    if map(lambda a: a.startswith(id), list_access) or True:
        keyb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='✅' + i.name, callback_data=f'regiondok_{i.id}')
                ] if (i.id in list_access) else [
                    InlineKeyboardButton(text=i.name, callback_data=f'regiondok_{i.id}')
                ] for i in Region.objects.filter(city__id=id)
            ]
        )
    else:
        keyb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=i.name, callback_data=f'regiondok_{i.id}')
                ] for i in Region.objects.filter(city__id=id)
            ]
        )
    keyb.inline_keyboard.append([InlineKeyboardButton(text='💾Saqlash💾', callback_data=f'regiondok_save')])
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


typework = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Veterinar', callback_data='Vetdoktor')
        ],
        [
            InlineKeyboardButton(text='Hayvon egasi', callback_data='Petowner')
        ],
    ]
)

doctor_editing_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='📝Mening malumotlarimni tahrirlash', callback_data='doctorediting_')
        ],
        [
            InlineKeyboardButton(text='📝Klinika malumotlarini tahrirlash', callback_data='clinicediting_')
        ]
    ]
)


def clinic_editing(obj):
    if obj:
        inline_keyboard = [
            [
                InlineKeyboardButton(text=i.name, callback_data=f'anythingddddd'),
                InlineKeyboardButton(text='❌O\'chirish', callback_data=f'cliniceditingdelete_{i.id}'),
                InlineKeyboardButton(text='🔄Tahrirlash', callback_data=f'cliniceditingedit_{i.id}'),
            ] for i in obj
        ]
    else:
        inline_keyboard = [
            [
                InlineKeyboardButton(text='Sizda Klinika yoq', callback_data='anythingddddd'),
            ]
        ]
    inline_keyboard.append([InlineKeyboardButton(text='🆕Qo\'shish', callback_data='cliniceditingadd_')])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


doctor_editing_menu_into = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='📝FIO ni o\'zgartirish', callback_data='doctoreditingfio_')
        ],
        [
            InlineKeyboardButton(text='📝Telefon raqamni o\'zgartirish', callback_data='doctoreditingphone_')
        ],
        [
            InlineKeyboardButton(text='📝Rasmimni o\'zagartirish', callback_data='doctoreditingphoto_')
        ],
        [
            InlineKeyboardButton(text='📝Tafsifni o\'zgartirish', callback_data='doctoreditingdesc_')
        ],
        [
            InlineKeyboardButton(text='📝Xizmat manzilini o\'zgartirish', callback_data='doctoreditinglocation_')
        ],
    ]
)

type_vet_clinic = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='💊Vet Apteka', callback_data='typvetklinik_VT')
        ],
        [
            InlineKeyboardButton(text='🏥Klinika', callback_data='typvetklinik_KL')
        ],
        [
            InlineKeyboardButton(text='🏥Laboratoriya', callback_data='typvetklinik_LB')
        ],
    ]
)


def clinic_editing_menu_into(id_clin):
    keyb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='📝Nomini o\'zgartirish', callback_data=f'cliniceditingname_{id_clin}')
            ],
            [
                InlineKeyboardButton(text='📝Viloyatini o\'zgartirish', callback_data=f'cliniceditingcity_{id_clin}')
            ],
            [
                InlineKeyboardButton(text='📝Manzilini o\'zgartirish', callback_data=f'cliniceditinglocation_{id_clin}')
            ],
            [
                InlineKeyboardButton(text='📝Rasmimni o\'zagartirish', callback_data=f'cliniceditingphoto_{id_clin}')
            ],
            [
                InlineKeyboardButton(text='📝Tafsifni o\'zgartirish', callback_data=f'cliniceditingdesc_{id_clin}')
            ],
        ]
    )
    return keyb
