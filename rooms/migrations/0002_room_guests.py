# Generated by Django 2.2.5 on 2021-09-17 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='guests',
            field=models.IntegerField(default=1),
        ),
    ]
