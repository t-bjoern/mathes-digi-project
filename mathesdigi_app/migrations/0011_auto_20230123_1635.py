# Generated by Django 3.2.5 on 2023-01-23 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mathesdigi_app', '0010_user_heft_nr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='heft_nr',
        ),
        migrations.AddField(
            model_name='user',
            name='heft',
            field=models.CharField(default='Mathes2', max_length=50),
            preserve_default=False,
        ),
    ]