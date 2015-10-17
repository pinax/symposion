from __future__ import unicode_literals

from importlib import import_module

from django.apps import AppConfig


class ScheduleConfig(AppConfig):
    name = "symposion.schedule"
    label = "symposion_schedule"
    verbose_name = "Symposion Schedule"

    def ready(self):
        import_module("symposion.schedule.receivers")
