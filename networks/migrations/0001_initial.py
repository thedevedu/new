# Generated by Django 3.2.5 on 2021-11-19 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('myadmin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Views',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ip', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user_agent', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.CharField(editable=False, max_length=200, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('languages', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myadmin.languages')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
