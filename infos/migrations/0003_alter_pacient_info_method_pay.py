# Generated by Django 4.2.5 on 2023-09-14 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0002_doctors_description_doctors_prof'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pacient_info',
            name='method_pay',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]