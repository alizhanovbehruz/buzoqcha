# Generated by Django 4.2.5 on 2023-09-14 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0014_another_text_share_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='type_quest',
            field=models.TextField(blank=True, null=True),
        ),
    ]
