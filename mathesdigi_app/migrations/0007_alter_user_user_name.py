# Generated by Django 3.2.5 on 2023-01-22 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mathesdigi_app', '0006_auto_20230122_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_name',
            field=models.CharField(max_length=20),
        ),
    ]