# Generated by Django 4.0.4 on 2022-04-13 22:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RiskType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('popis', models.CharField(max_length=255)),
                ('effects', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=255)),
                ('lastName', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('phoneNum', models.CharField(max_length=255)),
                ('userLogin', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('privileges', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Risk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('popis', models.CharField(max_length=255)),
                ('dateFrom', models.DateField()),
                ('dateTo', models.DateField()),
                ('probability', models.FloatField()),
                ('state', models.CharField(max_length=255)),
                ('price', models.PositiveBigIntegerField()),
                ('foreignKeyType', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='riskManagement.risktype')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('popis', models.CharField(max_length=255)),
                ('foreignKeyManager', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='riskManagement.user')),
                ('members', models.ManyToManyField(related_name='projectMembers', to='riskManagement.user')),
            ],
        ),
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('popis', models.CharField(max_length=255)),
                ('dateFrom', models.DateField()),
                ('dateTo', models.DateField()),
                ('foreignKeyManager', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='riskManagement.user')),
                ('foreignKeyProject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='riskManagement.project')),
            ],
        ),
    ]
