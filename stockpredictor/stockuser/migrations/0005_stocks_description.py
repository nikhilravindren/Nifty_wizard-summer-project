# Generated by Django 4.2.7 on 2024-06-25 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockuser', '0004_predictors'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocks',
            name='description',
            field=models.TextField(default=1, max_length=255),
        ),
    ]
