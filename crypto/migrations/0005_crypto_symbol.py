# Generated by Django 3.2.10 on 2022-04-20 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0004_crypto_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='crypto',
            name='symbol',
            field=models.CharField(blank=True, max_length=5, null=True, unique=True),
        ),
    ]
