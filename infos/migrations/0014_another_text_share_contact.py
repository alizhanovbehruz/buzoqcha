# Generated by Django 4.2.5 on 2023-09-14 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0013_another_text_ask_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='another_text',
            name='share_contact',
            field=models.CharField(default='Поделиться номер телефоном', max_length=250),
        ),
    ]