# Generated by Django 2.0 on 2018-01-08 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evrytesttools', '0015_auto_20180108_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='endtoendrecord',
            name='linuxinstanceID',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
