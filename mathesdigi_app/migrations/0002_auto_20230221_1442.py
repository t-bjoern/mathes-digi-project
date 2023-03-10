# Generated by Django 3.2.5 on 2023-02-21 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mathesdigi_app', '0001_squashed_0008_auto_20230221_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='heft',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='wertung',
            name='end_day',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='wertung',
            name='end_month',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='wertung',
            name='start_day',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='wertung',
            name='start_month',
            field=models.IntegerField(),
        ),
    ]
