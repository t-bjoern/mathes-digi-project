# Generated by Django 3.2.5 on 2023-03-08 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mathesdigi_app', '0004_auto_20230223_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='teilaufgaben',
            name='beschreibung',
            field=models.CharField(default='', max_length=30),
        ),
    ]