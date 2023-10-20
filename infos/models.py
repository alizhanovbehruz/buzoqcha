from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, Signal
from django.utils.translation import gettext_lazy


class StatusManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=True)


class Users(models.Model):
    class Type(models.TextChoices):
        DOKTOR = 'DR', 'Doktor'
        OWNER = 'OE', 'Owner'

    chat_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    type_person = models.CharField(max_length=2, choices=Type.choices, default=Type.OWNER)
    status_doc = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return self.username or self.full_name

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'


class City(models.Model):
    name = models.CharField(max_length=100)

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Город'


class Region(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регион'


class Doctor(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='doctor')
    work_region = models.ManyToManyField(Region, related_name='region_set', blank=True, null=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField(upload_to='doctors/%Y/%m/%d', null=True, blank=True)
    status = models.BooleanField(default=False)
    clinic_bool = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    description_ru = models.TextField(null=True, blank=True)

    objects = models.Manager()
    accessed_doc = StatusManager()

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Доктор'
        verbose_name_plural = 'Доктор'


class clinic(models.Model):
    class Type(models.TextChoices):
        VETAPTEKA = 'VT', 'VetApteka'
        KLINIKA = 'KL', 'Klinika'
        LABORATORIYA = 'LB', 'Laboratoriya'

    type_clinic = models.CharField(max_length=2, choices=Type.choices, default=Type.KLINIKA)
    name = models.CharField(max_length=100)
    region = models.ForeignKey(City, on_delete=models.CASCADE)
    longitude = models.FloatField()
    latitude = models.FloatField()
    photo = models.ImageField(upload_to='clinic/%Y/%m/%d', null=True, blank=True)
    owner = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='clinic_set')
    description = models.TextField(null=True, blank=True)
    description_ru = models.TextField(null=True, blank=True)


    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клиника'
        verbose_name_plural = 'Клиника'


class Admin_bot(models.Model):
    name = models.CharField(max_length=100, default='Nurmuxammad')
    chat_id = models.BigIntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['chat_id', ]),
        ]
        verbose_name = "Администраторы"
        verbose_name_plural = "Администраторы"

    def __str__(self):
        return self.name
# class Head(models.Model):
#     name = models.CharField(max_length=250)
#     description = models.TextField(null=True, blank=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'Главный меню'
#         verbose_name_plural = 'Главный меню'
#
#
# class detail(models.Model):
#     head = models.ForeignKey(Head, on_delete=models.CASCADE, related_name='head_set')
#     keys_text = models.CharField(max_length=250, null=True, blank=True, verbose_name='Текст кнопки')
#     description = models.TextField(null=True, blank=True, verbose_name='Описание')
#     url = models.URLField(verbose_name='Ссылка')
#
#     def __str__(self):
#         return self.description
#
#     class Meta:
#         verbose_name = 'Подробное читать'
#         verbose_name_plural = 'Подробное читать'
#
#
# class about(models.Model):
#     head = models.ForeignKey(Head, on_delete=models.CASCADE, related_name='head_set_about')
#     name = models.CharField(max_length=250, verbose_name='Название')
#     description = models.TextField(null=True, blank=True, verbose_name='Описание')
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'О проекте'
#         verbose_name_plural = 'О проекте'
#
#
# class questions(models.Model):
#     head = models.ForeignKey(Head, on_delete=models.CASCADE, related_name='head_set_questions', null=True, blank=True)
#     description = models.CharField(max_length=250, verbose_name='Название')
#     faq_text = models.TextField(verbose_name='Часто задаваемые вопросы')
#     let_text = models.TextField('запрос текст')
#     doctors_ques = models.TextField(null=True, blank=True, verbose_name='Другие тексты')
#     keyb_quest = models.TextField(null=True, blank=True, verbose_name='Текст кнопки')
#
#     def __str__(self):
#         return self.description
#
#     class Meta:
#         verbose_name = 'Вопросы'
#         verbose_name_plural = 'Вопросы'
#
#
# class cat_offline(models.Model):
#     head = models.ForeignKey(Head, on_delete=models.CASCADE, related_name='head_set_cat_offline', null=True, blank=True)
#     name = models.CharField(max_length=250, verbose_name='Название (кнопки)')
#     description = models.TextField(verbose_name='Описание')
#     sub_desc = models.TextField(null=True, verbose_name='Под описание')
#     photo = models.ImageField(upload_to=f'%Y/%m/%d')
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'Консультация'
#         verbose_name_plural = 'Консультация'
#
#
# class sub_cat_offline(models.Model):
#     cat = models.ForeignKey(cat_offline, on_delete=models.CASCADE, related_name='cat_offline_set')
#     name = models.CharField(max_length=250, verbose_name='Название (кнопки)')
#
#     def __str__(self):
#         return self.cat.name + ' : ' + self.name
#
#     class Meta:
#         verbose_name = 'Подкатегория консультации'
#         verbose_name_plural = 'Подкатегория консультации'
#
#
# class doctors(models.Model):
#     choise_type = (
#         ('online', 'Online'),
#         ('offline', 'Offline'),
#         ('online/offline', 'Online/Offline'),
#     )
#     choise_consult = (
#         ('calls', 'Calls'),
#         ('chat', 'Chat'),
#         ('calls/chat', 'Calls/Chat'),
#     )
#     prof = models.CharField(max_length=150, null=True, verbose_name='Профессия')
#     user_id = models.BigIntegerField(default=511172905)
#     description = models.TextField(verbose_name='Описание')
#     location = models.CharField(max_length=450, verbose_name='Адрес', null=True, blank=True)
#     cat_offline = models.ManyToManyField(sub_cat_offline, related_name='subcat_set',
#                                          verbose_name='Категории консультации')
#     full_name = models.CharField(max_length=250, verbose_name='ФИО')
#     work_type = models.TextField(max_length=150, choices=choise_type, default='online/offline',
#                                  verbose_name='Тип работы')
#     consult_type = models.TextField(max_length=150, choices=choise_consult, default='calls/chat',
#                                     verbose_name='Тип консультации')
#     offline_price = models.CharField(max_length=250, verbose_name='Цена консультации(оффлайн)', null=True, blank=True)
#     calls_price = models.CharField(max_length=350, verbose_name='Цена консультации(звонок/видео)', null=True,
#                                    blank=True,
#                                    default='💻 Онлайн консультация (звонок/видео) – 20$⌛️30 минут^^^💻 Onlayn maslahat (qo\'ng\'iroq/video) – 20$⌛️30 daqiqa')
#     chat_price = models.CharField(max_length=350, default="💬 Консультация в чате – 14$ ^^^💬 Chatda maslahat – $14",
#                                   verbose_name='Цена консультации(чат)', null=True, blank=True)
#     online_price = models.CharField(max_length=250, verbose_name='Цена консультации(онлайн)', null=True, blank=True)
#     image = models.ImageField(upload_to='doctors/%Y/%m/%d')
#
#     def __str__(self):
#         return self.full_name
#
#     class Meta:
#         verbose_name = 'Доктора'
#         verbose_name_plural = 'Доктора'
#
#
# class Payment(models.Model):
#     name_provider = models.CharField(max_length=250, verbose_name='Название платежной системы')
#     token = models.CharField(max_length=250, verbose_name='Токен')
#
#     def __str__(self):
#         return self.name_provider
#
#     class Meta:
#         verbose_name = 'Платежные системы'
#         verbose_name_plural = 'Платежные системы'
#
#
# class admin_info(models.Model):
#     user_id = models.BigIntegerField()
#     full_name = models.CharField(max_length=250, null=True, blank=True, verbose_name='ФИО')
#     username = models.CharField(max_length=250, null=True, blank=True)
#
#     def __str__(self):
#         return self.full_name
#
#     class Meta:
#         verbose_name = 'Администраторы'
#         verbose_name_plural = 'Администраторы'
#
#
# class pacient_info(models.Model):
#     choises = (
#         ('dates', 'Dates'),
#         ('question', 'Question')
#     )
#     doctor = models.ForeignKey(doctors, on_delete=models.PROTECT, null=True, blank=True)
#     cause = models.TextField(verbose_name='Что беспокоит')
#     full_name = models.TextField(max_length=250, verbose_name='Фио пациента')
#     age = models.TextField(verbose_name='Возраст пациента')
#     phone = models.TextField(verbose_name='Номер телефона')
#     total = models.TextField(null=True, blank=True, verbose_name='Всего')
#     type = models.CharField(max_length=50, choices=choises, default='dates', verbose_name='Тип данных')
#     time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
#     type_consult = models.CharField(max_length=50, null=True, blank=True, verbose_name='Тип консультации')
#     status = models.BooleanField(verbose_name='Статус оплаты', default=False)
#
#     def __str__(self):
#         return self.type + ' ' + str(self.doctor)
#
#     class Meta:
#         verbose_name = 'Пациенты'
#         verbose_name_plural = 'Пациенты'
#
#
# class payment_history(models.Model):
#     user_id = models.BigIntegerField(default=511172905)
#     amount = models.CharField(default='0',
#                               max_length=250, verbose_name='Сумма')
#     status = models.BooleanField(default=False, verbose_name='Статус оплаты')
#     time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
#
#     def __str__(self):
#         return f"{self.amount}, {self.user_id}"
#
#     class Meta:
#         verbose_name = 'История оплаты'
#         verbose_name_plural = 'История оплаты'
#
#
# class laboratory_analice(models.Model):
#     head = models.ForeignKey(Head, on_delete=models.CASCADE, related_name='head_set_lab', null=True, blank=True)
#     name = models.CharField(max_length=250, verbose_name='Название')
#     description = models.TextField(verbose_name='Описание')
#     photo = models.ImageField(upload_to='lab/%Y/%m/%d', null=True, blank=True)
#     keyb_text = models.CharField(max_length=250, verbose_name="Текст кнопки",
#                                  null=True, blank=True, default='Открыть в Google Maps')
#     longit = models.CharField(max_length=250, null=True, blank=True)
#     latit = models.CharField(max_length=250, null=True, blank=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'Лаборатория'
#         verbose_name_plural = 'Лаборатория'
#
#
# class recomended_centers(models.Model):
#     head = models.ForeignKey(Head, on_delete=models.CASCADE, related_name='head_set_recomended_centers', null=True,
#                              blank=True)
#     name = models.CharField(max_length=250, verbose_name='Название')
#     description = models.TextField(verbose_name='Описание')
#     photo = models.ImageField(upload_to='lab/%Y/%m/%d', null=True, blank=True)
#     keyb_text = models.CharField(max_length=250, null=True, verbose_name="Текст кнопки",
#                                  blank=True, default='Открыть в Google Maps')
#     longit = models.CharField(max_length=250, null=True, blank=True)
#     latit = models.CharField(max_length=250, null=True, blank=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'Рекомендуемые центры'
#         verbose_name_plural = 'Рекомендуемые центры'
#
#
# class mskt_book(models.Model):
#     head = models.ForeignKey(Head, on_delete=models.CASCADE, related_name='head_set_mskt_book', null=True,
#                              blank=True)
#     name = models.CharField(max_length=250, verbose_name='Название')
#     description = models.TextField(verbose_name='Описание')
#     photo = models.ImageField(upload_to='lab/%Y/%m/%d', null=True, blank=True)
#     keyb_text = models.CharField(max_length=250, verbose_name="Текст кнопки",
#                                  null=True, blank=True, default='Открыть в Google Maps')
#     longit = models.CharField(max_length=250, null=True, blank=True)
#     latit = models.CharField(max_length=250, null=True, blank=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'МСКТ'
#         verbose_name_plural = 'МСКТ'
#
#
# class connect_admin(models.Model):
#     head = models.ForeignKey(Head, on_delete=models.CASCADE, related_name='head_set_connect_admin', null=True,
#                              blank=True)
#     description = models.CharField(max_length=250, verbose_name='Описание')
#     url = models.URLField()
#     keyb_text = models.CharField(max_length=250, null=True, blank=True, verbose_name='Текст кнопки')
#
#     class Meta:
#         verbose_name = 'Связаться с администратором'
#         verbose_name_plural = 'Связаться с администратором'
#
#
# class another_text(models.Model):
#     start_text = models.TextField(default='Приветствуем в боте проекта TezShifo!\n'
#                                           'Мы за то, чтобы качественная медицинская помощь была доступна каждому.',
#                                   verbose_name='Текст стартового сообщения')
#     back = models.CharField(max_length=250, verbose_name='Вернуться назад')
#     previous = models.CharField(max_length=250, verbose_name='Назад')
#     select_doctor = models.CharField(max_length=250)
#     ask_question = models.CharField(max_length=250, verbose_name='Задать вопрос',
#                                     default='Задать вопрос')
#     share_contact = models.CharField(max_length=250, default='Поделиться номер телефоном',
#                                      verbose_name='Поделиться номер телефоном')
#     warning_text = models.TextField(default=f"вы начали заполнять заявку, но так и не оформили консультацию "
#                                             f"нашего специалиста. Что вас остановило? "
#                                             f"Вы могли бы написать оператору в чем проблема?"
#                                             f"^^^siz arizani to'ldirishni boshladingiz, lekin hech qachon "
#                                             f"biz bilan maslahatlashmagan mutaxassis Sizni nima to'xtatdi?"
#                                             f" Siz Bu haqda operatorga yoza olasizmi? muammo?",
#                                     verbose_name='Текст предупреждения')
#     warning_keyb = models.TextField(
#         default='Написать оператору\nОтмена заявки^^^Operatorga yozish\nArizani bekor qilish',
#         verbose_name='Кнопки предупреждения')
#
#     class Meta:
#         verbose_name = 'Другие тексты'
#         verbose_name_plural = 'Другие тексты'
#
#
# class Group_info(models.Model):
#     name = models.CharField(max_length=250, verbose_name='Название группы')
#     group_id = models.BigIntegerField(verbose_name='ID группы')
#     link_group = models.CharField(max_length=350, verbose_name='Ссылка на группу',
#                                   default='https://t.me/+q1L8DFcf0UplZWVi')
#     time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
#     status_working = models.BooleanField(default=False, verbose_name='Статус работы')
#     doctor_user_id = models.CharField(max_length=250, null=True, blank=True, verbose_name='ID доктора')
#     pacient_userid = models.CharField(max_length=250, null=True, blank=True, verbose_name='ID пациента')
#     users_id = models.CharField(max_length=250, null=True, blank=True, verbose_name='ID пользователей')
#     description = models.TextField(null=True, blank=True, default='админ добавь!!!', verbose_name='Инструкция')
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'Группы'
#         verbose_name_plural = 'Группы'
