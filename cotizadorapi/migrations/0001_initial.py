# Generated by Django 5.0.3 on 2024-03-07 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TR2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Age', models.IntegerField()),
                ('DX', models.DecimalField(decimal_places=25, max_digits=30)),
                ('CX', models.DecimalField(decimal_places=25, max_digits=30)),
            ],
        ),
    ]