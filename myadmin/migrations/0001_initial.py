# Generated by Django 3.2.5 on 2021-11-19 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Languages',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('languages', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('region', models.CharField(max_length=30)),
            ],
        ),
    ]
