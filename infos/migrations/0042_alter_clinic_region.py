# Generated by Django 4.2.5 on 2023-10-05 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0041_rename_user_id_users_chat_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinic',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='infos.city'),
        ),
    ]
