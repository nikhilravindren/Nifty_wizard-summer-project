# Generated by Django 4.2.7 on 2024-06-14 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockuser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocks',
            name='sector',
            field=models.CharField(default=1, max_length=100),
        ),
    ]
