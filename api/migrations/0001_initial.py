# Generated by Django 4.0.1 on 2022-05-29 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(default='', max_length=20)),
                ('day', models.IntegerField()),
                ('fact', models.CharField(default='', max_length=256)),
                ('popularity', models.IntegerField(default=0)),
            ],
            options={
                'unique_together': {('month', 'day')},
            },
        ),
    ]
