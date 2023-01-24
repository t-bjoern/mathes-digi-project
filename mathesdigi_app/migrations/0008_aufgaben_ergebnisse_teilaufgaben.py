# Generated by Django 3.2.5 on 2023-01-22 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mathesdigi_app', '0007_alter_user_user_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aufgaben',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aufgaben_nr', models.IntegerField()),
                ('heft_nr', models.IntegerField()),
                ('bezeichnung', models.CharField(max_length=200)),
                ('punktzahl', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Teilaufgaben',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teilaufgaben_id', models.CharField(max_length=5)),
                ('aufgabe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mathesdigi_app.aufgaben')),
            ],
        ),
        migrations.CreateModel(
            name='Ergebnisse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eingabe', models.CharField(max_length=200)),
                ('wertung', models.BooleanField()),
                ('teilaufgabe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mathesdigi_app.teilaufgaben')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mathesdigi_app.user')),
            ],
        ),
    ]