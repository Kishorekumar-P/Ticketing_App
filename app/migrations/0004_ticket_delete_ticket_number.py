# Generated by Django 5.1.1 on 2024-09-08 15:04

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_ticket_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adult_count', models.IntegerField()),
                ('children_count', models.IntegerField()),
                ('student_count', models.IntegerField()),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_type', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.DeleteModel(
            name='ticket_number',
        ),
    ]
