# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def resave_slots(apps, schema_editor):
    ScheduleSlot = apps.get_model("symposion_schedule", "slot")
    for slot in ScheduleSlot.objects.all():
        slot.save()


class Migration(migrations.Migration):

    dependencies = [
        ('symposion_schedule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='name',
            field=models.CharField(default='', max_length=100, editable=False),
            preserve_default=False,
        ),
        migrations.RunPython(resave_slots, migrations.RunPython.noop),
    ]
