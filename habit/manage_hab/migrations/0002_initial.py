# Generated by Django 5.0.4 on 2024-05-21 20:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('manage_hab', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='habit',
            name='habit_group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='manage_hab.habitgroup', verbose_name='Группа привычки'),
        ),
        migrations.AddField(
            model_name='habitprogress',
            name='habit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='manage_hab.habit', verbose_name='Привычка'),
        ),
    ]
