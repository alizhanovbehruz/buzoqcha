# Generated by Django 4.2.5 on 2023-09-14 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctors',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='doctors',
            name='prof',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
