# Generated by Django 4.2.5 on 2023-10-04 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0037_alter_doctor_work_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='work_region',
            field=models.ManyToManyField(blank=True, null=True, related_name='region_set', to='infos.region'),
        ),
    ]
