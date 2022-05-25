# Generated by Django 3.2.12 on 2022-05-24 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_searchresult_rank'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('title', models.CharField(max_length=200, null=True)),
                ('linkedin', models.CharField(max_length=200, null=True)),
                ('verified_email', models.CharField(max_length=200, null=True)),
                ('searchResult', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.searchresult')),
            ],
        ),
    ]
