# Generated by Django 5.0.2 on 2024-03-06 00:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatroom',
            old_name='members',
            new_name='member',
        ),
    ]