# Generated by Django 2.1.1 on 2018-09-14 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0006_auto_20180914_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='email',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='tnumber',
            name='number',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
