# Generated by Django 4.2.19 on 2025-04-14 02:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0004_votingotp'),
    ]

    operations = [
        migrations.DeleteModel(
            name='VotingOTP',
        ),
    ]
