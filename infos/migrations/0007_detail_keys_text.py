# Generated by Django 4.2.5 on 2023-09-14 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0006_alter_about_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='detail',
            name='keys_text',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]