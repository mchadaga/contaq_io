# Generated by Django 3.2.12 on 2022-05-31 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_lead'),
    ]

    operations = [
        migrations.AddField(
            model_name='leadlist',
            name='target_num_contacts',
            field=models.IntegerField(default=0),
        ),
    ]
