# Generated by Django 2.2 on 2019-05-26 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20190513_0030'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='email_is_corporative',
            field=models.BooleanField(default=False, verbose_name='Email Coporativo'),
        ),
        migrations.AddField(
            model_name='employee',
            name='phone_number_is_corporative',
            field=models.BooleanField(default=False, verbose_name='Telefone Coporativo'),
        ),
    ]
