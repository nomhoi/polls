# Generated by Django 2.2.10 on 2021-10-19 02:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20211018_0843'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='text',
            new_name='choice',
        ),
    ]
