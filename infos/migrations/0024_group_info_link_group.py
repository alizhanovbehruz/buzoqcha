# Generated by Django 4.2.5 on 2023-09-18 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0023_group_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='group_info',
            name='link_group',
            field=models.CharField(default='https://t.me/+q1L8DFcf0UplZWVi', max_length=350),
        ),
    ]
