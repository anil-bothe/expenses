# Generated by Django 5.0.1 on 2024-01-11 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_expense_shares'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='shares',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]