# Generated by Django 4.2.5 on 2023-10-05 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0038_alter_doctor_work_region'),
    ]

    operations = [
        migrations.CreateModel(
            name='admin_bot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Nurmuxammad', max_length=100)),
                ('chat_id', models.BigIntegerField()),
            ],
            options={
                'verbose_name': 'Администраторы',
                'verbose_name_plural': 'Администраторы',
                'indexes': [models.Index(fields=['chat_id'], name='infos_admin_chat_id_5215ca_idx')],
            },
        ),
    ]