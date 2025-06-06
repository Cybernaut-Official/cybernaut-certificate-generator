# Generated by Django 4.2.20 on 2025-03-17 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('year', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batches', to='programs.program')),
            ],
            options={
                'unique_together': {('program', 'month', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='programs.batch')),
            ],
            options={
                'unique_together': {('batch', 'name')},
            },
        ),
    ]
