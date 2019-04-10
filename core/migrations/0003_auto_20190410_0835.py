# Generated by Django 2.2 on 2019-04-10 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190409_1053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preparationclass',
            name='frequency',
        ),
        migrations.AddField(
            model_name='preparationclass',
            name='location',
            field=models.CharField(default='local', max_length=100, verbose_name='Local do treinamento'),
            preserve_default=False,
        ),
    ]
