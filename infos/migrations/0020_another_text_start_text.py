# Generated by Django 4.2.5 on 2023-09-15 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0019_alter_detail_description_alter_users_language_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='another_text',
            name='start_text',
            field=models.TextField(default='Приветствуем в боте проекта TezShifo!\nМы за то, чтобы качественная медицинская помощь была доступна каждому.'),
        ),
    ]
