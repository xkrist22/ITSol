# Generated by Django 4.0.4 on 2022-04-16 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('riskManagement', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='risk',
            old_name='describtion',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='risk',
            name='dateFrom',
        ),
        migrations.RemoveField(
            model_name='risk',
            name='dateTo',
        ),
        migrations.RemoveField(
            model_name='risk',
            name='foreignKeyType',
        ),
        migrations.RemoveField(
            model_name='risk',
            name='price',
        ),
        migrations.RemoveField(
            model_name='risk',
            name='probability',
        ),
        migrations.RemoveField(
            model_name='risk',
            name='state',
        ),
    ]
