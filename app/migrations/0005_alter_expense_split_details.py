# Generated by Django 5.0.1 on 2024-01-11 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_expense_split_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='split_details',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]