# Generated by Django 4.2.5 on 2023-09-14 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0003_alter_pacient_info_method_pay'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pacient_info',
            name='method_pay',
        ),
    ]
