# Generated by Django 2.2 on 2019-04-06 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_customuser_association'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='preparation_classes',
            field=models.ManyToManyField(related_name='employees', to='core.PreparationClass'),
        ),
    ]
