# Generated by Django 4.2.5 on 2023-10-05 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0040_doctor_clinic_bool_doctor_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='user_id',
            new_name='chat_id',
        ),
    ]