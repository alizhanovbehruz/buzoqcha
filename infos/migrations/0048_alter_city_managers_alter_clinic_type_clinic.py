# Generated by Django 4.2.5 on 2023-10-12 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0047_alter_city_managers_clinic_description_ru'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='city',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='clinic',
            name='type_clinic',
            field=models.CharField(choices=[('VT', 'VetApteka'), ('KL', 'Klinika'), ('LB', 'Laboratoriya')], default='KL', max_length=2),
        ),
    ]
