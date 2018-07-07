import sys
from django.conf import settings

_DEFAULT_FROM_SETTINGS = []

def object_from_settings(settings_key, default=_DEFAULT_FROM_SETTINGS):
    ''' Loads and returns the object named in the given settings key.
    '''

    args = [settings, settings_key]

    if default is not _DEFAULT_FROM_SETTINGS:
        args.append(default)

    name = getattr(*args)

    return import_named_object(name)


def import_named_object(name):
    ''' For a string x.y.z, import the module 'x.y' and return the object 'z'
    from that module.  Useful for naming models or strings in settings.'''

    dot = name.rindex(".")
    mod_name, form_name = name[:dot], name[dot + 1:]
    __import__(mod_name)
    return getattr(sys.modules[mod_name], form_name)
