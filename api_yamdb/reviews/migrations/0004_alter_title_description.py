# Generated by Django 3.2 on 2023-04-06 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20230402_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, default=1, verbose_name='Описание произведения'),
            preserve_default=False,
        ),
    ]
