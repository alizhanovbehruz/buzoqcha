# Generated by Django 4.2.5 on 2023-09-20 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0032_alter_another_text_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment_history',
            name='amount',
            field=models.CharField(default='0', max_length=250, verbose_name='Сумма'),
        ),
        migrations.AlterField(
            model_name='payment_history',
            name='user_id',
            field=models.BigIntegerField(default=511172905),
        ),
    ]
