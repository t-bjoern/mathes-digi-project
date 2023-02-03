# Generated by Django 3.2.5 on 2023-02-03 08:26

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mathesdigi_app', '0002_auto_20230201_2003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wertung',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='wertung',
            name='start_time',
        ),
        migrations.AddField(
            model_name='wertung',
            name='end_month',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wertung',
            name='start_month',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 3, 8, 26, 39, 317238, tzinfo=utc)),
        ),
    ]