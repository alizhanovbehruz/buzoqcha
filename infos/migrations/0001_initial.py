# Generated by Django 4.2.5 on 2023-09-14 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='admin_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField()),
                ('full_name', models.CharField(blank=True, max_length=250, null=True)),
                ('username', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='cat_offline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('sub_desc', models.TextField(null=True)),
                ('photo', models.ImageField(upload_to='%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='doctors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=450)),
                ('full_name', models.CharField(max_length=250)),
                ('work_type', models.TextField(choices=[('online', 'Online'), ('offline', 'Offline'), ('online/offline', 'Online/Offline')], default='online/offline', max_length=150)),
                ('offline_price', models.CharField(max_length=50)),
                ('online_price', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='doctors/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='Head',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='pacient_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cause', models.TextField(verbose_name='Что беспокоит')),
                ('full_name', models.TextField(max_length=250, verbose_name='Фио пациента')),
                ('age', models.TextField(verbose_name='Возраст пациента')),
                ('phone', models.TextField(verbose_name='Номер телефона')),
                ('total', models.CharField(blank=True, max_length=450, null=True)),
                ('type', models.CharField(choices=[('dates', 'Dates'), ('question', 'Question')], default='dates', max_length=50)),
                ('method_pay', models.CharField(blank=True, max_length=50, null=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('type_consult', models.CharField(blank=True, max_length=50, null=True)),
                ('status', models.BooleanField(default=False, verbose_name='Статус оплаты')),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='infos.doctors')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_provider', models.CharField(max_length=250)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='sub_cat_offline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cat_offline_set', to='infos.cat_offline')),
            ],
        ),
        migrations.CreateModel(
            name='recomended_centers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='lab/%Y/%m/%d')),
                ('longit', models.CharField(blank=True, max_length=250, null=True)),
                ('latit', models.CharField(blank=True, max_length=250, null=True)),
                ('head', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_set_recomended_centers', to='infos.head')),
            ],
        ),
        migrations.CreateModel(
            name='questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=250)),
                ('faq_text', models.TextField()),
                ('let_text', models.TextField()),
                ('head', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_set_questions', to='infos.head')),
            ],
        ),
        migrations.CreateModel(
            name='payment_history',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('pacient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='infos.pacient_info')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='infos.payment')),
            ],
        ),
        migrations.CreateModel(
            name='mskt_book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='lab/%Y/%m/%d')),
                ('longit', models.CharField(blank=True, max_length=250, null=True)),
                ('latit', models.CharField(blank=True, max_length=250, null=True)),
                ('head', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_set_mskt_book', to='infos.head')),
            ],
        ),
        migrations.CreateModel(
            name='laboratory_analice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='lab/%Y/%m/%d')),
                ('longit', models.CharField(blank=True, max_length=250, null=True)),
                ('latit', models.CharField(blank=True, max_length=250, null=True)),
                ('head', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_set_lab', to='infos.head')),
            ],
        ),
        migrations.AddField(
            model_name='doctors',
            name='cat_offline',
            field=models.ManyToManyField(related_name='subcat_set', to='infos.sub_cat_offline'),
        ),
        migrations.CreateModel(
            name='detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=250)),
                ('url', models.URLField()),
                ('head', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='head_set', to='infos.head')),
            ],
        ),
        migrations.CreateModel(
            name='connect_admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=250)),
                ('url', models.URLField()),
                ('head', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_set_connect_admin', to='infos.head')),
            ],
        ),
        migrations.AddField(
            model_name='cat_offline',
            name='head',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='head_set_cat_offline', to='infos.head'),
        ),
        migrations.CreateModel(
            name='about',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('head', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='head_set_about', to='infos.head')),
            ],
        ),
    ]
